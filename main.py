import discord
from discord import app_commands,File
import os
import json

with open("config.json",'r') as file:
    data = json.load(file)

    token = data['token']
    guild_id = data['guild_id']

client = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(client)
guild = discord.Object(id=guild_id)

@client.event
async def on_ready():
    await tree.sync(guild=guild)

@tree.command(name="icon",description="Send an icon from the library in chat",guild=guild)
@app_commands.describe(iconname="The name of the icon you want to send. Use /list to see all available options")
async def icon(ctx,*,iconname:str):
    for file in os.listdir("images/"):
        if iconname.lower() == file.split(".")[0].lower():
            icon_file = File(f"images/{file}")
            await ctx.response.send_message(file=icon_file)
            return

    await ctx.response.send_message("Icon not found. Make sure you wrote the name correctly",ephemeral=True)

@tree.command(name="list",description="Get a list of all the icons",guild=guild)
async def list(ctx):
    desc = "All the available icons:\n\n"
    for file in os.listdir("images/"):
        desc += file.split(".")[0]+"\n"
    await ctx.response.send_message(desc,ephemeral=True)

client.run(token)