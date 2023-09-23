from telethon.sync import TelegramClient
from telethon.tl.types import MessageService
import config
import asyncio

photo_medias = list()


async def send_file_group(client, dest_chat, medias_list):
    caption = ''

    # Extract caption from list
    for num, item in enumerate(medias_list):
        if isinstance(item, str):
            caption = medias_list.pop(num)

    # Extract media files from medias_list
    media_files = [item[1] for item in medias_list if isinstance(item, tuple)]

    await client.send_file(dest_chat,
                           file=media_files,
                           caption=caption)


def add_media_to_list(medias_list, grouped_id, media, caption):
    # Append media and its grouped_id as a tuple to medias_list
    medias_list.append((grouped_id, media))

    # Append caption just as regular str to medias_list if it's not empty
    if caption:
        medias_list.append(caption)


async def func():
    client = TelegramClient(config.PHONE_NUMBER,
                            config.API_ID, config.API_HASH)
    await client.connect()
    async for message in client.iter_messages(config.SOURCE, reverse=True):

        # Check if message is not Service Message
        if not isinstance(message, MessageService):

            # Check if message is in album (don't know why but telethon recognizes every media in album as separate message)
            if message.grouped_id is not None:
                if len(photo_medias) != 0:
                    prev_group = photo_medias[0][0]

                    # Check if new group started then if is - send previous album
                    if prev_group != message.grouped_id:
                        await send_file_group(client, config.DESTINATION, photo_medias)
                        photo_medias.clear()
                        add_media_to_list(
                            photo_medias, message.grouped_id, message.media, message.text)
                        await asyncio.sleep(config.COOL_DOWN)
                    else:
                        add_media_to_list(
                            photo_medias, message.grouped_id, message.media, message.text)
                else:
                    add_media_to_list(
                        photo_medias, message.grouped_id, message.media, message.text)
            else:

                # If this is a regular message - send an album if it is in our list
                if photo_medias:
                    await send_file_group(client, config.DESTINATION, photo_medias)
                    photo_medias.clear()
                    await asyncio.sleep(config.COOL_DOWN)
                await client.send_message(config.DESTINATION, message)
                await asyncio.sleep(config.COOL_DOWN)
                photo_medias.clear()

    # If we still have an album left after the end of the cycle, we send it too
    if photo_medias:
        await send_file_group(client, config.DESTINATION, photo_medias)


async def main():
    task = asyncio.create_task(func())
    await task

asyncio.run(main())
