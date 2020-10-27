from pyrogram import Client, filters
import os, shutil
from creds import my
from telegraph import upload_file
import logging

logging.basicConfig(level=logging.INFO)


TGraph = Client(
    "Image upload bot",
    bot_token = my.BOT_TOKEN,
    api_id = my.API_ID,
    api_hash = my.API_HASH
)


@TGraph.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(f"Hello {message.from_user.first_name},\Im a telegraph uploader bot. I can upload ur medias to telegraph. BOT BY @INDUSBOTS", True)
    
@TGraph.on_message(filters.photo)
async def getimage(client, message):
    tmp = os.path.join("downloads",str(message.chat.id))
    if not os.path.isdir(tmp):
        os.makedirs(tmp)
    imgdir = tmp + "/" + str(message.message_id) +".jpg"
    dwn = await message.reply_text("Media downloading by indus telegraph bot...", True)          
    await client.download_media(
            message=message,
            file_name=imgdir
        )
    await dwn.edit_text("Uploading media to telegram by indus telegraph bot....")
    try:
        response = upload_file(imgdir)
    except Exception as error:
        await dwn.edit_text(f"Sed....Im facing technical issues....contact @induschats\n{error}")
        return
    await dwn.edit_text(f"MEDIA UPLOADED

LINK:- https://telegra.ph{response[0]}

UPLOADED BY @INDUS_TELEGRAPHBOT")
    shutil.rmtree(tmp,ignore_errors=True)


TGraph.run()
