import argparse
import discord
import mysql.connector
import requests
import re
from discord.utils import get

mydb = mysql.connector.connect(
  host="localhost",
  database="omhauth",
  user="hubz",
  password="pass"
)

print(mydb)

sql_select_Query = "SELECT * FROM users"
cursor = mydb.cursor()
cursor.execute(sql_select_Query)
records = cursor.fetchall()

class MyClient(discord.Client):
    async def on_ready(self):
        print('bot logged in')
        #cancelled = 0
        game = discord.Game("omh role bot | http://status.hubza.co.uk/")
        await client.change_presence(status=discord.Status.dnd, activity=game)
    
    async def on_message(self, message):
        if message.author.bot == False:
            if message.content.startswith("oar>cancel"):
                #cancelled = 1
                channel = client.get_channel(740661218548646040)
                embed = discord.Embed(title="Cancelling is not implemented yet.", color=0xFF0000) # make green embed
                await channel.send(embed=embed)
            if message.content.startswith("oar>reloadroles"):
                if message.channel.id == 740661218548646040:
                    user = client.get_user(message.author.id)
                    channel = client.get_channel(740661218548646040)
                    embed = discord.Embed(title="Applying roles to all users automatically. Please wait.", color=0xaaaa00) # make green embed
                    await channel.send(embed=embed)
                    for obj in records:
                        aosu = obj[1]
                        adiscord = obj[2]
                        
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
                            if(medals > 117 and medals < 177):
                                print("50%")
                                await user.add_roles(r50c)
                            if(medals > 176 and medals < 212):
                                print("75%")
                                await user.add_roles(r75c)
                            if(medals > 211 and medals < 224):
                                print("90%")
                                await user.add_roles(r90c)
                            if(medals > 223):
                                print("95%")
                                await user.add_roles(r95c)
                            mhr = 639516052056965130
                            rmhr = get(guild.roles, id=mhr)
                            await user.add_roles(rmhr)
                            
                            print("setting username")
                            uname = re.search('<title>(.*?) ', content).group(1)
                            uname = uname.replace("&nbsp;", " ") 

client = MyClient()
client.run('token')
