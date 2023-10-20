#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  pypdfwalkcompress.py
#  
#  Copyright 2023 yucef sourani <youssef.m.sourani@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  Require pypdf (pip3 install pypdf)
import argparse
import os
import math
from pypdf import PdfReader, PdfWriter


def is_pdf(file_location):
    ispdf = False
    try:
        with open(file_location,"rb") as mf:
            if mf.read(5).decode("utf-8")[1:] == "PDF-":
                ispdf = True
    except Exception as e:
        print(e)
    return ispdf
    
def image_compress_pdf_file(file_location,quality):
    file_location_to_save = os.path.join(os.path.dirname(file_location),"image_compressed_"+os.path.basename(file_location))
    try:
        reader = PdfReader(file_location)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)
        writer.add_metadata(reader.metadata)
        for page in writer.pages:
            for img in page.images:
                img.replace(img.image, quality=quality)
        
        
        with open(file_location_to_save, "wb") as f:
            writer.write(f)
        print("Write {}==========>{} Done.".format(file_location,file_location_to_save))
    except Exception as e:
        print(e)
        print("Write {}==========>{} Failed.".format(file_location,file_location_to_save))
        
def image_compress_pdf_files(location,quality):
    for l in os.listdir(location):
        file_location = os.path.join(location,l)
        if os.path.isfile(file_location) and is_pdf(file_location):
            image_compress_pdf_file(file_location,quality)
            
def image_walk_and_compress_pdf_files(location,quality):
    for dirname,folders,files in os.walk(location):
        for file_ in files:
            file_location = os.path.join(dirname,file_)
            if os.path.isfile(file_location) and is_pdf(file_location):
                image_compress_pdf_file(file_location,quality)
            

def image_main_commpress_pdf(location,quality,walk):
    if quality > 100:
        quality = 100
    elif quality <= 0:
        quality = 1
    if os.path.isdir(location):
        if walk:
            image_walk_and_compress_pdf_files(location,quality)
        else:
            image_compress_pdf_files(location,quality)
    elif os.path.isfile(location):
        if is_pdf(location) :
            image_compress_pdf_file(location,quality)

                


def compress_pdf_file(file_location,quality):
    file_location_to_save = os.path.join(os.path.dirname(file_location),"compressed_"+os.path.basename(file_location))
    try:
        reader = PdfReader(file_location)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)
        writer.add_metadata(reader.metadata)
        for page in writer.pages:
            page.compress_content_streams(level=quality)
        
        
        with open(file_location_to_save, "wb") as f:
            writer.write(f)
        print("Write {}==========>{} Done.".format(file_location,file_location_to_save))
    except Exception as e:
        print(e)
        print("Write {}==========>{} Failed.".format(file_location,file_location_to_save))
        
def compress_pdf_files(location,quality):
    for l in os.listdir(location):
        file_location = os.path.join(location,l)
        if os.path.isfile(file_location) and is_pdf(file_location):
            compress_pdf_file(file_location,quality)
            
def compress_walk_and_compress_pdf_files(location,quality):
    for dirname,folders,files in os.walk(location):
        for file_ in files:
            file_location = os.path.join(dirname,file_)
            if os.path.isfile(file_location) and is_pdf(file_location):
                compress_pdf_file(file_location,quality)

def compress_main_commpress_pdf(location,quality,walk):
    if quality > 100:
        quality = 100
    elif quality <= 0:
        quality = 10
    quality = 10-math.ceil(quality/10)
    if os.path.isdir(location):
        if walk:
            compress_walk_and_compress_pdf_files(location,quality)
        else:
            compress_pdf_files(location,quality)
    elif os.path.isfile(location):
        if is_pdf(location):
            compress_pdf_file(location,quality)

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Script To Reduce PDF Files Size.")
    parser.version = "1.0"
    parser.add_argument("-v","--version",action="version")
    parser.add_argument("-t","--type",default="image",choices=["image","compression"],action="store",type=str,metavar="Reduce PDF Size Type (image|compression) ,Default image.")
    parser.add_argument("-l","--location",required=True,action="store",type=str,metavar="Folder|File Location")
    parser.add_argument("-q","--quality",type=int,default=80,choices=range(1,101),action="store",metavar="Quality range 1--->100 ,Default 80'(%)'")
    parser.add_argument("-r","--recursive",action="store_true",help="Get PDF files from directories and their contents recursively, Default False.")
    args = parser.parse_args()

    type_     = args.type
    location  = args.location
    quality   = args.quality
    recursive = args.recursive
    if type_ == "image":
        image_main_commpress_pdf(location,quality,recursive)
    else :
        compress_main_commpress_pdf(location,quality,recursive)


