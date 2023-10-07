import discord
import random


async def get_response(message: str) -> str:
    p_message = message.lower()

    command = ".spy "

    if p_message == command + 'hello':
        return 'Hey there!'

    if message == command + 'roll':
        return str(random.randint(1, 6))

    if message == command + "test":
        await send_test_response(message)

    if p_message == command or command + 'help':
        return '`Soon...`'


async def send_test_response(message):
    embedVar = discord.Embed(title="Title", description="Desc", color=0x00ff00)
    embedVar.add_field(name="Field1", value="hi", inline=False)
    embedVar.add_field(name="Field2", value="hi2", inline=False)
    await message.channel.send(embed=embedVar)
