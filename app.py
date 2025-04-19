from telethon import TelegramClient, events

api_id = 20225004
api_hash = "8f4c78e858658cd2aa21967a087bf819"
session_name = "session_telegram"

origem_id = -1002590813877
destino_id = -1002656975250

client = TelegramClient(session_name, api_id, api_hash)

@client.on(events.NewMessage(chats=origem_id))
async def encaminhar_mensagem(event):
    await client.forward_messages(destino_id, event.message)

print("Bot rodando...")
client.start()
client.run_until_disconnected()





add forwarder script
