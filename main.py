import asyncio
from typing import cast
from telethon import TelegramClient, events
from telethon.tl.custom import Message
from app.config_reader import config
from app import Console, gvs, read
from telethon_utils import event_filters




async def on_message(message: Message) -> None:
    if message.media:
        Console.info("Message have media. Forwarding ...")
        client = cast(TelegramClient, message.client)   # pyright: ignore

        to_send = message.message
        to_send.message = ""
        await client.send_message(int(config.OUTPUT_GROUP_ID), to_send)
        Console.info("Message forwarded to destination seccessfully.")



async def setup_event_handlers(client: TelegramClient) -> None:

    chat_ids = [int(g_id) for g_id in read.read_txt_lines(gvs.TARGET_GROUPS_FILE)]
    client.add_event_handler(on_message, events.NewMessage(func=event_filters.message_from_chatslist(chat_ids=chat_ids)))

async def main() -> None:
    client = TelegramClient(config.PHONE_NUMBER, api_id=gvs.API_ID, api_hash=gvs.API_HASH)

    await setup_event_handlers(client)

    await client.start(phone=config.PHONE_NUMBER)  # pyright: ignore
    Console.info("Bot started!")



if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.set_debug(gvs.VIRCHUAL)
    loop.create_task(main())
    loop.run_forever()