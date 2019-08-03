#! /usr/bin/env python
# coding: utf-8

from PIL import Image
import os
from math import ceil
import numpy as np
import sys


def generating_mesh(w,h,mesh_size):
    I=ceil(w/mesh_size)
    J=ceil(h/mesh_size)
    mesh_list={}
    for i in range(0,I):
        for j in range(0,J):
            mesh_list[(i*mesh_size,j*mesh_size,(i+1)*mesh_size,(j+1)*mesh_size)]=-1
    return mesh_list

if __name__ == '__main__':
    I_path=sys.argv[1]
    O_path=sys.argv[2]
    Mask=sys.argv[3]
    
    pic_list=os.listdir(I_path)
    Mask_obj=Image.open(Mask)
    Mask_array=np.asarray(Mask_obj.convert('1'))

    min_sqr_size=int((sum(sum(Mask_array))/len(pic_list))**0.5)

    while 1:
        w,h=Mask_obj.size
        mesh_list=generating_mesh(w,h,min_sqr_size)
        for mesh in mesh_list:
            b1,a1,b2,a2=mesh
            Coverage=sum(sum(Mask_array[a1:a2,b1:b2]))/(min_sqr_size**2)
            mesh_list[mesh]=Coverage
        if sum(np.asarray(list(mesh_list.values()))>0.2)>len(pic_list):
            min_sqr_size+=1
        else:
            break

    canvas=Image.new("RGBA",(w,h),'white')

    i=0
    for mesh in mesh_list:
        std_white=Image.new("RGB",(min_sqr_size,min_sqr_size),'white')
        if mesh_list[mesh]==0:
            continue
        elif mesh_list[mesh]<=0.2:
            canvas.paste(std_white,mesh)
        else:
            pic_this=Image.open(I_path+pic_list[i])
            pic_this=pic_this.resize((min_sqr_size,min_sqr_size))
            canvas.paste(pic_this,mesh)
            i+=1

    canvas.putalpha(Mask_obj.convert('1'))

    canvas.save(O_path+'merge.png',format='PNG')

