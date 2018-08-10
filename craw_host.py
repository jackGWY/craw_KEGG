import os
from lxml import etree
import requests
import urllib
import time
import pymysql

headers={'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    # proxie={"http":host_list[count_host]}
    # if count_host>host_list_len-1:
    #     count_host=0
    # else:count_host=count_host+1

f=open('proxy.txt','a')
for i in range(1,400):
    url='https://www.kuaidaili.com/free/inha/'+str(i)+'/'
    data = requests.get(url, headers=headers).text
    s = etree.HTML(data)
    for j in range(1,13):
        ip=s.xpath('//*[@id="list"]/table/tbody/tr['+str(j)+']/td[1]/text()')
        if ip==None or ip==[]:
            break
        ip=ip[0].strip()
        port=s.xpath('//*[@id="list"]/table/tbody/tr['+str(j)+']/td[2]/text()')
        port=port[0].strip()
        print(ip)
        print(port)
        f.writelines(ip+":"+port+"\n")

f.close()


