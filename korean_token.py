from konlpy.tag import Kkma
from konlpy.tag import Hannanum
from konlpy.tag import Okt
from progressbar import *
import time
from konlpy.utils import pprint
import string
import os
import codecs
import re
from threading import Thread
import multiprocessing
import jpype

lines = []
#hannanum = Hannanum()
#p1 = re.compile(r'<*?')
#p2 = re.compile(r"[｜《》”‘’〈〉·•“（）]")
#print(stopwords)

def do_concurrent_tagging(input_file,process_no,start, end,lines):
    #input_file 输入文件路径+文件名
    #process_no 进程号
    #start 开始处理的行号  end  结束处理的行号
    # lines  文件内容列表
    # 根据当前进程处理开始和结束行号的内容，并将结果存入的文件
    stopwords = {}.fromkeys([line.rstrip() for line in codecs.open('stopwords_ko.txt', 'r', 'utf-8-sig')])
#    print(input_file+'token_nopunc'+str(thread_no))
#    print('thread_no : %d start %d end %d '%(process_no,start,end))
    okt = Okt()
    result = ''
    resultlist= []
    jpype.attachThreadToJVM()

    widgets = ['Progress: '+str(process_no), Percentage(), ' ', Bar('#'), ' ', Timer(),' ', ETA(), ' ', FileTransferSpeed()]
    pbar = progressbar.ProgressBar(widgets=widgets, maxval=10 * (end-start)).start()
    for i in range(start, end):
        if not lines[i].strip():
            continue
        if re.match(r'.*?<.*?>', lines[i]):
            continue
        table = lines[i].maketrans(' ', ' ', string.punctuation)  # 去除标点转化表
        linestr = lines[i].translate(table)
        try:
            linelist = okt.pos(linestr)
            pbar.update(10*(i-start) + 1)
        except BaseException as e:
            print(e)
            print(i)
            result = ''
            print('at %lino is token erroe,reinit tonken object' %i)
            okt = Okt()
            continue
        else:
            if len(linelist) >= 1:
                for s_tup in linelist:
                    if s_tup[0] not in stopwords:
                        result = result + " " + s_tup[0]
            else:
                result = ''
                continue
            result = result + '\n'
            try:
                resultlist.append(result)
                result = ''
                continue
            except BaseException as e:
                print(e)
                print(linestr)
                result = ''
                continue
    pbar.finish()
    outfile = codecs.open(input_file + 'token_nopunc' + str(process_no), 'w', 'utf-8')
    outfile.write('\n'.join(resultlist))
    outfile.close()
    return

def myfun(input_file,thread_num):#  input 输入文件路径和名称  thread_num 线程数量
    global lines
    #取得整个文件行数
    file=codecs.open(input_file, 'r', 'utf-8')
    for count, line in enumerate(file):
        lines.append(line)
    nlines=count+1
    print(nlines)
    file.close()
    #取得每个线程处理的起始点
    lineindex= list(range(1,nlines,int(nlines/thread_num)))
    print(lineindex)

    sharelist = multiprocessing.Manager().list(lines)



    #创建多进程
    thread_list=[]
    for thread_no in range(1,thread_num+1) :
    #    t= Thread(target=do_concurrent_tagging, args=(input_file,thread_no,lineindex[thread_no-1],lineindex[thread_no]))
        t= multiprocessing.Process(target=do_concurrent_tagging, args=(input_file,thread_no,lineindex[thread_no-1],lineindex[thread_no],sharelist))
        thread_list.append(t)
        t.start()
    #检测直至所有进程停止
    for t in thread_list:
        t.join()
    #合并文件

    newfile = codecs.open(input_file+'token_nopunc', 'w', 'utf-8')
    for item in [input_file+'token_nopunc'+str(no) for no in range(1,thread_num+1)]:
        for txt in codecs.open(item,'r','utf-8'):
            newfile.write(txt)
    newfile.close()
    print("退出主线程")
d = os.getcwd()
myfun(d + '//wiki_00clean',10)