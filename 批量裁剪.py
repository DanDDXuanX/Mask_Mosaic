#! /usr/bin/env python
# coding: utf-8


import os
import sys
from PIL import Image

def main(I_path,O_path,size):
    pic_list=os.listdir(I_path)
    for pic in pic_list:
        print(pic)
        pic_this=Image.open(I_path+'\\'+pic)
        (w,h)=pic_this.size
        if pic_this.mode!='RGB':
            pic_this=pic_this.convert('RGB')
        if w/h>1:
            pic_this=pic_this.resize((round(300*w/h),300))
            pic_this=pic_this.crop((int(300*w/h/2-150),0,int(300*w/h/2+150),300))
        else:
            pic_this=pic_this.resize((300,round(300*h/w)))
            pic_this=pic_this.crop((0,int(300*h/w/2-150),300,int(300*h/w/2+150)))
        pic_this.save(O_path+'\\'+pic.split('.')[0]+'.jpg',format='JPEG',quality=75,subsampling=0)

if __name__ == '__main__':
    I_path=sys.argv[1]
    O_path=sys.argv[2]
    try:
        size=sys.argv[3]
    except:
        size=300
    main(I_path,O_path,size)