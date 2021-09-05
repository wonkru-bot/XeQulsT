import os

import asyncio

from pytgcalls import GroupCallFactory
from pyrogram.raw.functions.phone import CreateGroupCall
from pyrogram import Client, filters

from pyrogram.types import Message
from config import Config



group_call_factory = GroupCallFactory(GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM)
VIDEO_CALL = {}

@Client.on_message(filters.command("stream"))

async def stream(client, m: Message):

    replied = m.reply_to_message

    if not replied:

        await m.reply("`Reply to some Video!`")

    elif replied.video or replied.document:

        msg = await m.reply("`Downloading...`")

        chat_id = m.chat.id

        if os.path.exists(f'stream-{chat_id}.raw'):

            os.remove(f'stream-{chat_id}.raw')

        try:

            video = await client.download_media(m.reply_to_message)

            await msg.edit("`Converting...`")

            os.system(f'ffmpeg -i "{video}" -vn -f s16le -ac 2 -ar 48000 -acodec pcm_s16le -filter:a "atempo=0.81" vid-{chat_id}.raw -y')

        except Exception as e:

            await msg.edit(f"**🚫 Error** - `{e}`")

        await asyncio.sleep(5)

        try:

            group_call = group_call_factory.get_file_group_call(f'vid-{chat_id}.raw')

            await group_call.start(chat_id)

            await group_call.set_video_capture(video)

            VIDEO_CALL[chat_id] = group_call

            await msg.edit("**▶️ Started Streaming!**")

        except FloodWait as e:

            await sleep(e.x)

            if not group_call.is_connected:

                await group_call.start(chat_id)

        except Exception as e:

            await msg.edit(f"**Error** -- `{e}`")

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

