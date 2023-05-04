import asyncio
import time
import configparser
import os

import openai
from pyrogram import Client, filters


def parse_config():
    config_list = {}
    index = 0
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.split(".")[-1] == "ini":
                config_list[index] = file.split(".")[0]
                index += 1
    return config_list


config_list = parse_config()
name_config = config_list[int(input(f"Список конфигов: {parse_config()}\nНапиши цифру: "))]

config = configparser.ConfigParser()
config.read(name_config + ".ini", encoding="UTF-8")

NAME_SESSION = config["INFO"]["NAME_SESSION"]
TIME = float(config["INFO"]["TIME"])
PROMT = config["INFO"]["PROMT"]


app = Client(NAME_SESSION, api_id=23421561, api_hash="4747ccdaa5840d30fda5411478616b7a")

openai.api_key = ""


async def chat_gpt(promt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=promt,
        max_tokens=1024,
        temperature=0.85,
    )
    await asyncio.sleep(TIME)
    return response.choices[0].text


@app.on_message(filters.channel)
async def comment(client, message):
    start = time.time()
    if message.edit_date is None:
        return
    linked = await get_linked(message)
    message_to_answer = await get_forwarded_in_linked(message.message_id, linked)
    print(message.text)
    response_text = await chat_gpt(message.text + "\n" + PROMT)
    await app.send_message(linked.id, response_text.split("\n")[-1], reply_to_message_id=message_to_answer.message_id)
    print(f"ANSWERED TO: {message.chat.title} За {time.time() - start}")


async def get_forwarded_in_linked(message_id, linked):
    async for message in app.search_messages(linked.id, limit=1, filter="pinned"):
        return message


async def get_linked(msg):
    channel = await app.get_chat(msg.sender_chat.id)
    return channel.linked_chat

app.run()
