import rpyc
import argparse
from collections import Counter
import re

fp = open('/Users/guoguo/Desktop/Studium/4.Semeter/Alp4_Code/Übung9/Gutenberg_eBook.txt','r')
file = fp

@rpyc.service
class WordCountService(rpyc.Service):
    @rpyc.exposed
    def count_words(lines):
        wordcount = {}
        for line in lines:
            words = line.lower()
            # 将行文本分割为单词
            words = line.split()
            for word in words:
                if word.isalnum():
                    if word in wordcount:
                        wordcount[word] += 1
                    else:
                        wordcount[word] = 1
        #print(wordcount["the"])
        return wordcount

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    t1 = ThreadedServer(MyService, port=18861)
    t2 = ThreadedServer(MyService, port= 18862)
    t1.start()
    t2.statr()

# print(remove_space(file))
print(WordCountService.count_words(file))
file.close()