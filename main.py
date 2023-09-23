from telethon.sync import TelegramClient
from telethon.tl.types import MessageService
import config
import asyncio

photo_medias = list()

async def send_file_group(client, dest_chat, medias_list):
    caption = ''

    # Extract caption if it's provided as a string in medias_list
    for num, item in enumerate(medias_list):
        if isinstance(item, str):
            caption = medias_list.pop(num)

    # Extract media files from medias_list
    media_files = [item[1] for item in medias_list if isinstance(item, tuple)]
    
    await client.send_file(dest_chat, file=media_files, caption=caption)


def add_media_to_list(medias_list, grouped_id, media, caption):
    # Append media and its grouped_id as a tuple to medias_list
    medias_list.append((grouped_id, media))
    
    # Append caption to medias_list if it's not empty
    if caption:
        medias_list.append(caption)


async def func():
    client = TelegramClient(config.PHONE_NUMBER, config.API_ID, config.API_HASH)
    await client.connect()
    async for message in client.iter_messages(config.SOURCE, reverse=True):
        if not isinstance(message, MessageService):
            if message.grouped_id is not None:
                if len(photo_medias) != 0:
                    prev_group = photo_medias[0][0]
                    if prev_group != message.grouped_id:
                        await send_file_group(client, config.DESTINATION, photo_medias)
                        photo_medias.clear()
                        add_media_to_list(photo_medias, message.grouped_id, message.media, message.text)
                        await asyncio.sleep(config.COOL_DOWN)
                    else:
                        add_media_to_list(photo_medias, message.grouped_id, message.media, message.text)
                else:
                    add_media_to_list(photo_medias, message.grouped_id, message.media, message.text)
            else:
                if photo_medias:
                    await send_file_group(client, config.DESTINATION, photo_medias)
                    photo_medias.clear()
                    await asyncio.sleep(config.COOL_DOWN)
                await client.send_message(config.DESTINATION, message)
                await asyncio.sleep(config.COOL_DOWN)
                photo_medias.clear()
    if photo_medias:
        await send_file_group(client, config.DESTINATION, photo_medias)

async def main():
    task = asyncio.create_task(func())
    await task

asyncio.run(main())
