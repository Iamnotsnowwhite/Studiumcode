#include <stdio.h>
#include <stdlib.h>

#include "weather.h"

void prompt_program_input(int* program)
{
    printf("Please select which program you would like to run ('1' for task #1 or '2' for task #2): ");
    
    if(scanf("%d", program) < 1)
    {
        printf("scanf() matched less than one argument.\n");
        exit(EXIT_FAILURE);
    }
}

int main(int argc, char* argv[])
{
    int program = 0;
    // Try to read the first command line input as program index
    if(argc > 1)
    {
        program = atoi(argv[1]);
    }
    // If that fails, prompt the user to input the value
    if(program == 0)
    {
        prompt_program_input(&program);
    }
    
    // Try to execute one of the programs, if possible
    if(program == 1)
    {
        main1();
    }
    else if(program == 2)
    {
        main2();
    }
    else
    {
        printf("Invalid input.\n");
        exit(EXIT_SUCCESS);
    }
}
