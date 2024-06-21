import rpyc
import argparse
from collections import Counter
import re

with open('/Users/guoguo/Desktop/Studium/4.Semeter/Alp4_Code/Übung9/Gutenberg_eBook.txt','r') as file:
    content = file.read()


c = rpyc.connect("mapreduceserver",18861)
d = rpyc.connect("mapreduceserver",18862)
c.root.count_words
d.root.count_words

myfunc_async = async_(conn.root.count_words)
res = myfunc_async(1,2,3)

def Zeilen_Aufteilen(content):
    lines = content.splitlines()
    num_lines = len(lines)
    taskgrupp_einheit = num_lines // 2
    task1 = lines[:taskgrupp_einheit] 
    task2 = lines[taskgrupp_einheit:]
    return

# print(Zeilen_Aufteilen(content))

file.close()

