#!/usr/bin/python
#coding=utf-8
import re
import sys
import codecs
from os import path

def myfun(input_file):
    p1 = re.compile(r'-\{.*[\u1100-\u11FF\u3130-\u318F\uAC00-\uD7AF]+:([^;]*?)(;.*?)?\}-')
    p2 = re.compile(r'[（\(][.，；。？！\s]*[）\)]')
    p3 = re.compile(r'[「『]')
    p4 = re.compile(r'[」』]')
    outfile = codecs.open(input_file+'clean', 'w', 'utf-8')
    with codecs.open(input_file, 'r', 'utf-8') as myfile:
        for line in myfile:
            print(line)
            line = p1.sub(r'\2', line)
            line = p2.sub(r'', line)
            line = p3.sub(r'“', line)
            line = p4.sub(r'”', line)
            print(line)
            outfile.write(line)
        outfile.close()
if __name__ == '__main__':
    if len(sys.argv) != 1:
        print("Usage: python script.py inputfile")
        sys.exit()
    d = path.dirname(__file__)
    print(d)
    myfun(d+'\\wiki_00')