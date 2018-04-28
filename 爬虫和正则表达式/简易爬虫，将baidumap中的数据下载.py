# encoding='utf-8'  
import urllib.request
import codecs
import re
#import time
def getHtml(url):
    try:
            page = urllib.request.urlopen(url,timeout=0.3)
    except Exception:
            page = urllib.request.urlopen(url,timeout=1)
    html = page.read()
    page.close()
    return html

opena=open('D:\\dcl\\a.txt','r',encoding='ISO-8859-1')
ef=open('D:\\dcl\\ef.txt','a',encoding='ISO-8859-1')
while True:
    line_a=opena.readline()
    if line_a:
        print (line_a)
        line_a=line_a.rstrip()
        temp=re.split(',',line_a)
        print (temp[0])
        w='武汉'
        ww=urllib.parse.quote(w)
        x='http://api.map.baidu.com/direction/v1?mode='+temp[6]+'&origin='+temp[4]+','+temp[3]+'&destination='+temp[2]+','+temp[1]+'&origin_region='+ww
        x=x+'&destination_region='+ww+'&output=xml&ak=FfC4hlg7le9q06BkEvZ9z7kZZyBzKyzc'
        try:
            page = urllib.request.urlopen(x,timeout=0.3)
            html = page.read()
            page.close()
            html = html.decode()
            html1 = re.sub(r'&lt;', '<', html)
            html2 = re.sub(r'&gt;', '>',html1)
            f = codecs.open('D:\\dcl\\result\\'+temp[0]+'.txt','w')
            f.write(html2)
            f.close()
        except Exception:
            try:
                page = urllib.request.urlopen(x,timeout=1)
                html = page.read()
                page.close()
                html = html.decode()
                html1 = re.sub(r'&lt;', '<', html)
                html2 = re.sub(r'&gt;', '>',html1)
                f = codecs.open('D:\\dcl\\result\\'+temp[0]+'.txt','w')
                f.write(html2)
                f.close()
            except Exception:
                ef.write('\n'+line_a)
                pass

        #time.sleep(2)
    else:
        break
opena.close()
ef.close()



