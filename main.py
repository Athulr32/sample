from pyrogram import Client,emoji,filters
from pyrogram.types import ChatPermissions,ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from firebase import firebase
from gcloud import storage
import os
import time
import shutil

app = Client(
    "my_account",
    api_id= "",
    api_hash="",
    bot_token=""
)

TARGET = ""
@app.on_message(filters.command(["start"]))
def start(client,message):
    client.send_message(chat_id=message.chat.id ,text="Hi there!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Group", url="")], [InlineKeyboardButton("Channel", url="https://t.me/film_corner_channel")]]))

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


@app.on_message(filters.reply & filters.chat(TARGET) & filters.command(["title"]))
def title(client,message):
    client.set_administrator_title(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id, title="Fc_Bot")
#@app.on_message(filters.reply & filters.command(["restrict"]))
"""def restrict(client,message):
    client.restrict_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id, ChatPermissions = ChatPermissions(can_send_messages=True),time=int(time() + 86400))"""
"""@app.on_message(filters.text & filters.command(["permissions"]))"""
"""def perm(client,message):
    client.set_chat_permissions(chat_id=message.chat.id, ChatPermissions(
        can_send_messages=True"""

   # )
#)"""


TARGET = "filmcorner_FCGroup"  
MENTION = "[{}](tg://user?id={})"  
MESSAGE = "{} Welcome to  {}!"



# Filter in only new_chat_members updates generated in TARGET chat
@app.on_message(filters.chat(TARGET) & filters.new_chat_members)
def welcome(client, message):
   
    new_members = [u.mention for u in message.new_chat_members]

    
    text = MESSAGE.format(emoji.SPARKLES, ", ".join(new_members))

    message.reply_text(text, disable_web_page_preview=True)

firebase = firebase.FirebaseApplication("")
@app.on_message(filters.reply & filters.chat("Athul_Rithu"))
def rename(client,message):
    repl=client.send_message(chat_id=message.chat.id, text="Downloading")
    temp_dir= os.path.join("./download",str(message.chat.id))
    if not os.path.isdir(temp_dir):
        os.makedirs(temp_dir)
    new_name,cap,name=message.text.split(",")
    new_name=new_name.lower()
    
    
    file_path=os.path.join(temp_dir, new_name)
    file_path=client.download_media(message=message.reply_to_message, file_name=file_path)

    time.sleep(2)
    repl.edit("Uploading to channel")
    send=client.send_document(document=file_path, chat_id="", caption=message.text)
    time.sleep(2)
   
    data={"movie":new_name,
          "id":send.link}
    firebase.put('/movies',name,data)

    shutil.rmtree(temp_dir, ignore_errors=True)
@app.on_message(filters.text & filters.chat(""))
def new(client,message):
    txt=message.text
    txt=txt.lower()
    rslt=firebase.get('/movies',txt)

    if rslt is not None:
        file_id=rslt["id"]
        client.send_message(chat_id=message.chat.id, text="hi", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("400mb", url=file_id),InlineKeyboardButton("700mb", url=file_id)]])
                                                                                               
app.run()
