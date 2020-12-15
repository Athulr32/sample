from pyrogram import Client,emoji,filters
from pyrogram.types import ChatPermissions,ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import os
import time
import shutil
app = Client(
    "my_account",
    api_id= "",
    api_hash="",
    bot_token=""
)

TARGET = "Group/channel_name"
@app.on_message(filters.command(["start"]))
def start(client,message):
    client.send_message(chat_id=message.chat.id ,text="Hi there! Iam a BOT Maintained by Group FILMCORNER", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Group", url="https://t.me/filmcorner_FCGroup")], [InlineKeyboardButton("Channel", url="https://t.me/film_corner_channel")]]))

"""@app.on_message(filters.text)
def echo(client, message):
    if message.text=="Lucifer":
        message.reply_text("ok")"""
#pin a chat
@app.on_message(filters.reply & filters.chat(TARGET) & filters.command(["pin"]))
def fun1(client,message):
    print(message)
    client.pin_chat_message(chat_id=message.chat.id, message_id=message.reply_to_message.message_id)

#unpin a chat
@app.on_message(filters.text & filters.chat(TARGET) & filters.command(["unpin"]))
def unpin(client,message):
    client.unpin_chat_message(chat_id=message.chat.id)

#kick a chat member
@app.on_message(filters.reply & filters.chat(TARGET) & filters.command(["kick"]))
def kick(client,message):
    try:
        client.kick_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)
        message.reply_text("Successfully kicked")
    except:
       message.reply_text("You are not an admin")





TARGET = ""  
MENTION = "[{}](tg://user?id={})"  
MESSAGE = "{} Welcome to  {}!"




@app.on_message(filters.chat(TARGET) & filters.new_chat_members)
def welcome(client, message):
   
    new_members = [u.mention for u in message.new_chat_members]

    
    text = MESSAGE.format(emoji.SPARKLES, ", ".join(new_members))

    message.reply_text(text, disable_web_page_preview=True)

@app.on_message(filters.reply & filters.chat("Athul_Rithu"))
def rename(client,message):
    repl=client.send_message(chat_id=message.chat.id, text="Downloading")
    temp_dir= os.path.join("./download",str(message.chat.id))
    if not os.path.isdir(temp_dir):
        os.makedirs(temp_dir)
    new_name,cap=message.text.split(",")
    file_path=os.path.join(temp_dir, new_name)
    file_path=client.download_media(message=message.reply_to_message, file_name=file_path)

    time.sleep(2)
    repl.edit("Uploading to channel")

    client.send_document(document=file_path, chat_id="channel_name", caption=cap)
    shutil.rmtree(temp_dir, ignore_errors=True)

app.run()
