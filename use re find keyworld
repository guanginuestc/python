# encoding='ISO-8859-1'

import re


def whatisdis(lines):
    dis_temp = re.findall(r'<distance>(\d+?)</distance>',lines)
    dis_temp0 = dis_temp[0]
    return dis_temp0

def getdur(lines):
    dur_temp=re.findall(r'<duration>(\d+?)</duration>',lines)
    return dur_temp[0]

def getpath(lines):
    path_temp=re.findall(r'<path>(.+?)</path>',lines)
    return path_temp

def getprice(lines):
    price_temp=re.findall(r'<total_price>(\d+?)</total_price>',lines)
    return price_temp

def write_file(txtname,dis,dur,price,path):
    tot_price=0;
    for p in price:
        tot_price = tot_price+int(p)
    res=txtname+';'+dis+';'+dur+';'+str(tot_price)
    for per in path:
        res=res+';'+per
    res=res+'\n'
    f.write(res)

num=1
f=open('D:\\dcl\\second\\result.txt','w')
while num<4855:
    txtname=str(num)
    lines=open('D:\\dcl\\result\\'+txtname+'.txt').read()
    dis=whatisdis(lines)
    dur=getdur(lines)
    path=getpath(lines)
    price=getprice(lines)
    write_file(txtname,dis,dur,price,path)
    print(num)
    num=num+1
f.close()
