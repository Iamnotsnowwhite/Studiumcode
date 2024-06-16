#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <dirent.h>
#include <sys/stat.h>
#include <omp.h>
#include "weather.h"

#define ANSI_COLOR_RED     "\x1b[31m"
#define ANSI_COLOR_GREEN   "\x1b[32m"
#define ANSI_COLOR_RESET   "\x1b[0m"

// All the data required about a single station to simulate its local weather
typedef struct
{
    // ID of station as provided by file name (i.e. 2 for "02_Gatow_...")
    int id;
    // Index of the air_temperature column, starting at 1
    int temperature_column_index;
    // ID of neighboring stations
    int neighbor_ids[4];
    int neighbor_count;
} station_config;

// Global station config
station_config config[] = {
    {2, 9, {14, 18, 12}, 3},
    {4, 9, {15, 18}, 2},
    {6, 11, {13}, 1},
    {7, 9, {17}, 1},
    {12, 9, {2, 4}, 2},
    {13, 13, {6, 21}, 2},
    {14, 11, {16, 12, 2}, 3},
    {15, 9, {4, 18}, 2},
    {16, 11, {17, 21, 18, 14}, 4},
    {17, 19, {7, 16}, 2},
    {18, 9, {4, 15}, 2},
    {19, 15, {6, 18}, 2},
    {21, 9, {17, 13, 15, 16}, 4}
};

int config_index_from_station_id(int station_id)
{
    int station_amount = sizeof(config) / sizeof(station_config);
    for(int i = 0; i < station_amount; i++)
    {
        if(config[i].id == station_id)
            return i;
    }
}

int filter(const struct dirent* name)
{
    return 1;
}

// Return file pointer to csv file for a given station id
FILE* get_file_for_station(int station_id)
{
    // Read all file entires in the "input" directory
    struct dirent **namelist;
    int entries = scandir("./input", &namelist, filter, alphasort);
    if(entries == -1)
    {
        perror("scandir");
        exit(EXIT_FAILURE);
    }

    // Filter through each until the correct file is found#
    char number_prefix[3];
    for(int i = 0; i < entries; i++)
    {
        char* file_name = namelist[i]->d_name;
        
        int number = atoi(strncpy(number_prefix, file_name, 2));

        if(number == station_id) {
            char file_path[64];
            snprintf(file_path, 64, "input/%s", file_name);
            FILE* file = fopen(file_path, "r");
            return file;
        }
    }

    return NULL;
}

// Struct for a (converted) line of data from a csv file
typedef struct
{
    int month;
    int day;
    int hour;
    int minute;
    double air_temperature;
    bool is_valid;
} measurement_data;

// Retrieve next measurement from file into data for a specific station. Returns -1 if there is no data left
int get_next_measurement(FILE* file, measurement_data* data, int config_index)
{
    // Read first line that doesn't start with #
    char* line_contents = (char*) malloc(128 * sizeof(char));
    int rc = fscanf(file, "%[^\n] ", line_contents);
    while(line_contents[0] == '#' && rc != EOF)
    {
        rc = fscanf(file, "%[^\n] ", line_contents);
    }
    if(rc == EOF)
    {
        free(line_contents);
        return -1;
    }

    // Separate arguments by spaces
    char* token; // Current column
    char* rest = line_contents;
    int column = 1;
    while((token = strtok_r(rest, "	", &rest)))
    {
        // Interpret date arguments and write them into struct
        switch(column)
        {
            case 2:
                data->month = atoi(token);
                break;
            case 3:
                data->day = atoi(token);
                break;
            case 4:
                data->hour = atoi(token);
                break;
            case 5:
                data->minute = atoi(token);
                break;
            default:
                break;
        }
        // Write air_temperature argument and its validity into struct
        if(column == config[config_index].temperature_column_index)
        {
            data->air_temperature = atof(token);
        }
        else if(column == config[config_index].temperature_column_index + 1)
        {
            if(token[0] == 'm' || token[0] == 's')
                data->is_valid = false;
            else
                data->is_valid = true;
        }

        column++;
    }

    free(line_contents);

    return 0;
}

// Write a comment line into the file explaining what each column stands for
void write_measurement_file_header(FILE* target)
{
    char* header = (char*) malloc(128 * sizeof(char));
    snprintf(header, 128, "# Jahr	Monat	Tag	Stunde	Minute	Lufttemperatur\n");
    fprintf(target, header);

    free(header);
}

// Write measurement data to a new line in the specified file
void write_measurement_to_file(FILE* target, measurement_data* data)
{
    char* new_line = (char*) malloc(128 * sizeof(char));
    snprintf(new_line, 128, "2022	%.2d	%.2d	%.2d	%.2d	%.1f\n",
    data->month, data->day, data->hour, data->minute, data->air_temperature);
    fprintf(target, new_line);

    free(new_line);
}

// Utility struct to summarize measurement data for a station
typedef struct
{
    measurement_data previous;
    measurement_data current;
} station_measurements;

// 'Simulates' the weather for a given config entry and writes the results into a csv file
void simulate_weather(int config_index)
{
    int station_id = config[config_index].id;

    // Open station files and target file
    FILE* station_file = get_file_for_station(station_id);
    if(!station_file) {
        perror("station_file");
        exit(EXIT_FAILURE);
    }

    // Open the file for each neighboring station
    int neighbor_count = config[config_index].neighbor_count;
    FILE* neighbor_files[neighbor_count];
    for(int i = 0; i < neighbor_count; i++)
    {
        neighbor_files[i] = get_file_for_station(config[config_index].neighbor_ids[i]);
        if(!neighbor_files[i])
        {
            perror("neighbor_file");
            exit(EXIT_FAILURE);
        }
    }

    // Create output folder with read/write/execute permissions
    const char* output_folder = "output";
    mkdir(output_folder, S_IRWXU);

    // Construct target file path (format: "output/{station_id}.csv")
    char* target_file_name = (char*) malloc(20 * sizeof(char));
    snprintf(target_file_name, 20, "output/%d.csv", station_id);

    FILE* target_file = fopen(target_file_name, "w");
    if(!target_file)
    {
        perror("target_file");
        exit(EXIT_FAILURE);
    }

    // Allocate data for all station measurements
    station_measurements measurement_station;
    station_measurements measurement_neighbor[neighbor_count];
    measurement_data result;

    // Get first measurement for each station, doesn't account for invalid data in the first row
    get_next_measurement(station_file, &measurement_station.current, config_index);
    for(int i = 0; i < neighbor_count; i++)
    {
        int neighbor_index = config_index_from_station_id(config[config_index].neighbor_ids[i]);
        get_next_measurement(neighbor_files[i], &measurement_neighbor[i].current, neighbor_index);
    }

    write_measurement_file_header(target_file);

    while(1)
    {
        // Set current measurements as previous ones
        measurement_station.previous = measurement_station.current;
        for(int i = 0; i < neighbor_count; i++)
        {
            measurement_neighbor[i].previous = measurement_neighbor[i].current;
        }

        // Read next lines into memory and convert them into usable data. Stop if there is no more data
        int rc = get_next_measurement(station_file, &measurement_station.current, config_index);
        if(rc == -1) break;
        // If air temperature isn't available, use existing data from previous measurement
        if(!measurement_station.current.is_valid)
            measurement_station.current.air_temperature = measurement_station.previous.air_temperature;

        // Same procedure for neighbor stations
        for(int i = 0; i < neighbor_count; i++)
        {
            int neighbor_index = config_index_from_station_id(config[config_index].neighbor_ids[i]);
            rc = get_next_measurement(neighbor_files[i], &measurement_neighbor[i].current, neighbor_index);
            if(rc == -1) break;
            if(!measurement_neighbor[i].current.is_valid)
                measurement_neighbor[i].current.air_temperature = measurement_neighbor[i].previous.air_temperature;
        }

        // Write date data
        result.month = measurement_station.current.month;
        result.day = measurement_station.current.day;
        result.hour = measurement_station.current.hour;
        result.minute = measurement_station.current.minute;

        // 'Simulate' air temperature via difference for each station and do some median stuff
        double average_temperature = measurement_station.current.air_temperature - measurement_station.previous.air_temperature;
        for(int i = 0; i < neighbor_count; i++)
        {
            average_temperature += measurement_neighbor[i].current.air_temperature;
        }
        average_temperature /= neighbor_count + 1;
        result.air_temperature = average_temperature;

        // Write result in target file
        write_measurement_to_file(target_file, &result);
    }
    
    // Close all file handles (if valid) once simulation is complete
    // This causes the multi-threaded version to crash, so it's commented out
    /*
    fclose(station_file);

    fclose(target_file);

    for(int i = 0; i < neighbor_count; i++)
    {
        fclose(neighbor_files[i]);
    }
    */
}

int main1()
{
    int station_amount = sizeof(config) / sizeof(station_config);
    for(int i = 0; i < station_amount; i++)
    {
        int station_id = config[i].id;
        printf(ANSI_COLOR_RED "Simulating weather for station %d..." ANSI_COLOR_RESET "\n", station_id);
        simulate_weather(i);
        printf(ANSI_COLOR_GREEN "Weather simulation for station %d complete!" ANSI_COLOR_RESET "\n", station_id);
    }
    return 0;
}

int main2()
{
    int station_amount = sizeof(config) / sizeof(station_config);
    #pragma omp parallel for
    for(int i = 0; i < station_amount; i++)
    {
        int thread_id = omp_get_thread_num();
        int station_id = config[i].id;
        printf(ANSI_COLOR_RED "Thread %d simulating weather for station %d..." ANSI_COLOR_RESET "\n", thread_id, station_id);
        simulate_weather(i);
        printf(ANSI_COLOR_GREEN "Weather simulation for station %d complete!" ANSI_COLOR_RESET "\n", station_id);
    }
    return 0;
}