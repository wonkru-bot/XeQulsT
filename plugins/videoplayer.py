import os
import time
import pafy
import asyncio
import ffmpeg
from pytgcalls import GroupCallFactory
from pyrogram.raw.functions.phone import CreateGroupCall
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message
from config import Config

SESSION_NAME = Config.SESSION
API_HASH = Config.API_HASH
API_ID = Config.API_ID

app = Client(SESSION_NAME, API_ID, API_HASH)
group_call_factory = GroupCallFactory(app, GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM)
VIDEO_CALL = {}

@Client.on_message(filters.command("stream"))

async def stream(client, m: Message):

    replied = m.reply_to_message

    if not replied:

        if len(m.command) < 2:

            await m.reply("`Reply to some Video or Give Some Live Stream Url!`")

        else:

            video = m.text.split(None, 1)[1]

            youtube_regex = (

                                         r'(https?://)?(www\.)?'

                                       '(youtube|youtu|youtube-nocookie)\.(com|be)/'

                                       '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

            youtube_regex_match = re.match(youtube_regex, video)

            if youtube_regex_match:

            	try:            		yt = pafy.new(video)

            		best = yt.getbest()

            		video_url = best.url

            	except Exception as e:

            		await m.reply(f"**Error** -- `{e}`")

            		return

            	msg = await m.reply("`Starting Live Stream...`")

            	chat_id = m.chat.id

            	await asyncio.sleep(1)

            	try:

            	   group_call = group_call_factory.get_group_call()

            	   await group_call.join(chat_id)

            	   await group_call.start_video(video_url)

            	   VIDEO_CALL[chat_id] = group_call

            	   await msg.edit(f"**▶️ Started [Live Streaming](video) !**")

            	except Exception as e:

            		await msg.edit(f"**Error** -- `{e}`")

            else:

            	msg = await m.reply("`Starting Live Stream...`")

            	chat_id = m.chat.id

            	await asyncio.sleep(1)

            	try:

            	   group_call = group_call_factory.get_group_call()

            	   await group_call.join(chat_id)

            	   await group_call.start_video(video)

            	   VIDEO_CALL[chat_id] = group_call

            	   await msg.edit(f"**▶️ Started [Live Streaming](video) !**")

            	except Exception as e:

            		await msg.edit(f"**Error** -- `{e}`")

            	

    elif replied.video or replied.document:

        msg = await m.reply("`Downloading...`")

        video = await client.download_media(m.reply_to_message)

        chat_id = m.chat.id

        await asyncio.sleep(2)

        try:

            group_call = group_call_factory.get_group_call()

            await group_call.join(chat_id)

            await group_call.start_video(video)

            VIDEO_CALL[chat_id] = group_call

            await msg.edit("**▶️ Started Streaming!**")

        except Exception as e:

            await msg.edit(f"**🚫 Error** - `{e}`")

    else:

        await m.reply("`Reply to some Video!`")

@Client.on_message(filters.command("stop"))

async def stopvideo(client, m: Message):

    chat_id = m.chat.id

    try:

        await VIDEO_CALL[chat_id].stop()

        await m.reply("**⏹️ Stopped Streaming!**")

    except Exception as e:

        await m.reply(f"**🚫 Error** - `{e}`")
        
