#用于指定列表的下载
#!/usr/bin/python3
#encoding:utf-8
import requests,os
if os.path.exists("美女图片"):
    os.chdir("美女图片")
else:
    try:
        os.mkdir("美女图片")
        os.chdir("美女图片")
    except:
        print("文件夹无法创建")
def mm131():
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36","Referer":"https://m.mm131.net/xinggan/"}  
    d=1
    http="https://img1.hnllsy.com/pic/"#我无法保证这个不会改变，你需要去他的网站看看他的url变了没。另外他们的请求头可能需要随时调整，例如加入referer、UserAgent等。
    http22=list(range(3200,4000))
    #http3="/"
    filename=0
    for http2 in http22:
        while d<50:
            httpz=http+str(http2)+"/"+str(d)+".jpg"
            response=requests.get(httpz,headers=headers)
            print(httpz)
            filename=filename+1
            fn=str(filename)+".jpg"
            with open(fn,"wb")as f:
                f.write(response.content)
                xinxi=os.stat(fn)
            if xinxi.st_size<=1024:#太小了可能就是废图片
                os.remove(fn)
                filename=filename-1
            d=d+1
        d=1    

mm131()
