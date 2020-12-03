import argparse
import discord
from discord.ext import commands
import mysql.connector
import requests
import re
import base64
from discord.utils import get
import os
import socket
import time


mydb = mysql.connector.connect(
  host="localhost",
  database="c0omhauth",
  user="c0auth",
  password="pass"
)


print(mydb)

sql_select_Query = "SELECT * FROM users"
cursor = mydb.cursor()
cursor.execute(sql_select_Query)
records = cursor.fetchall()

intents = discord.Intents.all()
client = commands.Bot(command_prefix="oar>", intents=intents) # someone said i needed this

@client.event
async def on_ready():
    print('bot logged in')
    #cancelled = 0
    game = discord.Game("omh role bot | http://status.hubza.co.uk/")
    await client.change_presence(status=discord.Status.dnd, activity=game)

@client.event
async def on_message(message):
    if message.author.bot == False:
        if message.content.startswith("who is " + client.user.name) or message.content.startswith("o>reportallbots"):
            await message.channel.send("I'm " + client.user.name + " running on " + str(socket.gethostname()) + "\n" + "`PROCESS ID` : `" + str(os.getpid()) + "`\n`PARENT ID` : `" + str(os.getppid()) + "`\n`LOCATION` : `" + os.path.realpath(__file__) + "`")
        if message.content.startswith("oar>cancel"):
            #cancelled = 1
            channel = client.get_channel(740661218548646040)
            embed = discord.Embed(title="Cancelling is not implemented yet.", color=0xFF0000) # make green embed
            await channel.send(embed=embed)
        if message.content.startswith("oar>reloadroles"):
            if message.channel.id == 740661218548646040:
                orderby = message.content.split("reloadroles",1)[1] 
                print("extras: " + orderby)
                if orderby == "":
                    orderby = "id"
                sql_select_Query = "SELECT * FROM users ORDER BY " + orderby;
                cursor = mydb.cursor()
                cursor.execute(sql_select_Query)
                records = cursor.fetchall()
                user = client.get_user(message.author.id)
                channel = client.get_channel(740661218548646040)
                embed = discord.Embed(title="Applying roles to all users automatically. Please wait.", color=0xaaaa00) # make green embed
                await channel.send(embed=embed)
                for obj in records:
                    aosu = obj[1]
                    adiscord = obj[2]
                    await process(aosu, adiscord, channel, obj)
                    time.sleep(5)
        if message.content.startswith("oar>reload"):
            username = uid = message.content.replace("oar>reload ","")
            cursor = mydb.cursor()
            cursor.execute("SELECT * FROM users WHERE osuname = %(username)s", {'username': username});
            records = cursor.fetchall()
            user = client.get_channel(message.author.id)
            channel = client.get_channel(message.channel.id)
            for obj in records:
                aosu = obj[1]
                adiscord = obj[2]
                await process(aosu, adiscord, channel, obj)
                time.sleep(5)
                    
@client.event
async def process(aosu, adiscord, channel, obj = 0):
    guild = client.get_guild(639515567233171476)

    user = client.get_user(adiscord)

    if guild.get_member(adiscord) is not None:
        embed = discord.Embed(title="Processing User", description="id: " + str(obj[0]) + "\nosuid: " + str(aosu) + "\ndiscordid: " + user.mention, color=0xaaaa00) # make green embed
        await channel.send(embed=embed)
        print("getting medal count")
        url = 'https://osu.ppy.sh/users/' + str(aosu)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
        }
        cookies = requests.head(url)
        r = requests.get(url, headers=headers, allow_redirects=True, cookies=cookies)
        content = str(r.content)
        medals = content.count("achievement_id")
        print("getting roles")
        r50cid = 667130931617988610
        r50c = get(guild.roles, id=r50cid)
        r75cid = 667130932406255647
        r75c = get(guild.roles, id=r75cid)
        r90cid = 639517663990906910
        r90c = get(guild.roles, id=r90cid)
        r95cid = 643262553681559593
        r95c = get(guild.roles, id=r95cid)
        user = guild.get_member(adiscord)
        await user.remove_roles(r50c)
        await user.remove_roles(r75c)
        await user.remove_roles(r90c)
        await user.remove_roles(r95c)
        print("applying roles")
        if(medals >= 129 and medals < 193):
            print("50%")
            await user.add_roles(r50c)
        if(medals >= 193 and medals < 232):
            print("75%")
            await user.add_roles(r75c)
        if(medals >= 232 and medals < 245):
            print("90%")
            await user.add_roles(r90c)
        if(medals > 245):
            print("95%")
            await user.add_roles(r95c)
        mhr = 639516052056965130
        rmhr = get(guild.roles, id=mhr)
        await user.add_roles(rmhr)

        print("setting username")
        uname = re.search('<title>(.*?) ', content).group(1)
        uname = uname.replace("&nbsp;", " ") 
        uname = uname.replace("\u2665", " ")

        print("setting up user info with this info:")
        print("osuid: " + str(aosu))
        print("discordid: " + str(aosu))
        print("osuname: " + uname)
        string_bytes = user.name.encode("utf-8")
        base64_bytes = base64.b64encode(string_bytes) 
        base64_string = base64_bytes.decode("ascii") 
        dname = base64_string;



        print("discordname: " + dname + "#" + user.discriminator)

    
        pfp = str(user.avatar_url)

        if pfp is None:
            pfp = "none";





        print("discordpfp: " + pfp)
        mycursor = mydb.cursor()
        sql = "UPDATE users SET discordname = '" + dname + "', osuname = '" + uname + "', pfp = '" + pfp + "', discordtag = " + str(user.discriminator) + ", medals = " + str(medals) + " WHERE discordid = " + str(adiscord);
        mycursor.execute(sql)
        mydb.commit()
        print(mycursor.rowcount, "record(s) affected") 
        print("response from osu! : " + content[0:50])
        
        embed = discord.Embed(title="User Processed", description="id: " + str(obj[0]) + "\nosuid: " + str(aosu) + "\ndiscordid: " + user.mention + "\nmedals = " + str(medals), color=0xaaaa00) # make green embed  
        await channel.send(embed=embed)
        
        time.sleep(3)
    else:
        channel = client.get_channel(740661218548646040)
        embed = discord.Embed(title="User does not exist", description="The system will automatically remove this user.\nid: " + str(obj[0]) + "\nosuid: " + str(aosu) + "\ndiscordid: " + str(adiscord), color=0xaaaa00) # make 
        await channel.send(embed=embed)
        mycursor = mydb.cursor()
        sql = "DELETE FROM `users` WHERE `users`.`osuid` = " + str(aosu);
        mycursor.execute(sql)
        mydb.commit()

client.run('no')
