from pyrogram import Client

while True:
    NAME_SESSION = input("Название сессии: ")
    TIME = float(input("ВРЕМЯ: "))
    PROMT = input("ПРОМТ: ")

    with Client(NAME_SESSION, api_id=15354199, api_hash="4b42c4babb1f7866c005b8c5a967add7"):
        pass

    with open(NAME_SESSION + ".ini", "w") as file:
        file.write(f"[INFO]\nNAME_SESSION = {NAME_SESSION}\nTIME = {TIME}\nPROMT = {PROMT}")
