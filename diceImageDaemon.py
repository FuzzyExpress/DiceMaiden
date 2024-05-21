import discord, subprocess, os, time, asyncio, socket
from discord.ext import commands
from dotenv import load_dotenv
os.chdir(os.path.dirname(__file__))


load_dotenv()

TOKEN = os.getenv('TOKEN')



intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'{client.user} has logged in.')
    client.loop.create_task(socket_server())

async def socket_server():
    server = await asyncio.start_server(handle_client, '127.0.0.1', 8888)

    async with server:
        await server.serve_forever()

async def handle_client(reader, writer):
    data = await reader.read(10000)
    message = data.decode()
    print("".join(message))

    file_path, int1, int2 = message.split(',')

    if not os.path.exists(file_path):
        file_path = '/home/evans/Documents/Discord/DiceMaiden/DiceRolls/Error.png'

    print("got")
    for guild in client.guilds:
        if guild.id == int(int1):
            for channel in guild.channels:
                if channel.id == int(int2):
                    await channel.send(file=discord.File(file_path))
                    print("sent")
    

    writer.write("Image sent successfully".encode())
    await writer.drain()
    writer.close()

# Run the Discord bot and socket server in the same thread
if __name__ == '__main__':
    # Start the Discord bot in the main thread
    client.run(TOKEN)
