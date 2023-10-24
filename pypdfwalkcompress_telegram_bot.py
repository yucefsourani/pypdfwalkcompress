#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
#
# Requires :
#    pyTelegramBotAPI
#    pypdf
#
import telebot
import tempfile
from io import BytesIO
import os
from pypdf import PdfReader, PdfWriter
from telebot.types import InputFile

MAGIC_USER      = "all" #add user with magic user  make bot public for all # default for ADMIN_USER only 
ADMIN_USER      = "yucef" #your telegram user name
telegram_token  = "" #your telegram bot token
MAX_SIZE        = 10*1000*1000 # max PDF file size accepted 10MB
DEFAUTL_QUALITY = 80 # Default image quality (Between 1 and 100) low number better compress less image quality


bot             = telebot.TeleBot(telegram_token)
allowed_users   = [ADMIN_USER] 


def image_compress_pdf_file(file_o,quality,message,file_name):
    file_to_save = str(quality)+"_"+file_name
    try:
        reader = PdfReader(file_o)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)
        writer.add_metadata(reader.metadata)
        for page in writer.pages:
            for img in page.images:
                img.replace(img.image, quality=quality)
        
        with tempfile.TemporaryDirectory()  as tmpd:
            file_location_to_save = os.path.join(tmpd,file_to_save)
            with open(file_location_to_save, "wb") as f:
                writer.write(f)

            with open(file_location_to_save, "rb") as f:
                bot.send_document(chat_id=message.chat.id,document=InputFile(f),disable_content_type_detection=True)
                
    except Exception as e:
        print(e)
        bot.reply_to(message,"Write {}==========>{} Failed.".format(file_name,file_to_save))
    finally:
        file_o.close()


     
@bot.message_handler(func=lambda message: True,content_types=['document'])
def handle__document(message):
    quality = message.caption
    if  quality:
        if not quality.isdigit():
            quality = DEFAUTL_QUALITY
        else:
            quality = int(quality)
        if quality > 100:
            quality = 100
        elif quality <= 0:
            quality = DEFAUTL_QUALITY
    else:
        quality = DEFAUTL_QUALITY
        
    if message.content_type == "document" and (message.from_user.username in allowed_users  or MAGIC_USER in allowed_users )  :
        file_info = bot.get_file(message.document.file_id)
        if file_info.file_path.lower().endswith(".pdf"):
            if file_info.file_size <= MAX_SIZE:
                file_data = bot.download_file(file_info.file_path)
                if file_data[1:10].startswith(b"PDF-"):
                    file_s = BytesIO()
                    file_s.write(file_data)
                    del file_data
                    file_location_to_save = image_compress_pdf_file(file_s,quality,message,message.document.file_name)
                else:
                    del file_data
                    bot.send_message(message.chat.id, 'PDF File Only')
            else:
                bot.send_message(message.chat.id, 'max file size is {}B'.format(MAX_SIZE))
        else:
            bot.send_message(message.chat.id, 'PDF File Only')


@bot.message_handler(commands=['addu'])
def addu(message):
    if message.from_user.username == ADMIN_USER:
        msg  = telebot.util.extract_arguments(message.text)
        if msg:
            msg = msg.split()[0]
            if msg == ADMIN_USER:
                bot.reply_to(message, "Permission denied")
                return
            if not msg in  allowed_users:
                allowed_users.append(msg)   # To Do make sqlite or json file to get/add/remove users from database
                bot.reply_to(message, "Add '{}' Done.".format(msg))
            else:
                bot.reply_to(message, "{} already exists".format(msg))
        else:
            bot.reply_to(message, "Enter user name to add")
    else:
        bot.reply_to(message, "Permission denied")

@bot.message_handler(commands=['removeu'])
def removeu(message):
    if message.from_user.username == ADMIN_USER:
        msg  = telebot.util.extract_arguments(message.text)
        if msg:
            msg = msg.split()[0]
            if msg == ADMIN_USER:
                bot.reply_to(message, "Permission denied")
                return
            if  msg in  allowed_users:
                allowed_users.remove(msg) # To Do make sqlite or json file to get/add/remove users from database
                bot.reply_to(message, "Remove '{}' Done.".format(msg))
            else:
                bot.reply_to(message, "{} not exists".format(msg))
        else:
            bot.reply_to(message, "Enter user name to remove")
    else:
        bot.reply_to(message, "Permission denied")

@bot.message_handler(commands=['getusers'])
def getusers(message):
    if message.from_user.username == ADMIN_USER:
        users = " - ".join(allowed_users) # To Do make sqlite or json file to get/add/remove users from database
        bot.reply_to(message, users)
    else:
        bot.reply_to(message, "Permission denied")
        
bot.infinity_polling()
