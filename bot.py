import discord
import random
import requests
import json
import asyncio
import time
import re
from bs4 import BeautifulSoup

toggleScrap = True


def read_json_line(index):
  with open('characters.json', 'r') as f:
    for i, line in enumerate(f):
      if i == index:
        return json.loads(line)
  return None


def write_to_json(githubname, name, commits, last_commit_nom,
                  last_commit_date):
  character = {
    "githubname": githubname,
    "name": name,
    "commits": commits,
    "LastCommitNom": last_commit_nom,
    "LastCommitDate": last_commit_date
  }

  with open('characters.json', 'a') as f:
    json.dump(character, f)
    f.write('\n')


def update_json_line(index,
                     githubname=None,
                     name=None,
                     commits=None,
                     last_commit_nom=None,
                     last_commit_date=None):
  with open('characters.json', 'r') as f:
    lines = f.readlines()

  if index < 0 or index >= len(lines):
    return False

  character = json.loads(lines[index])

  if githubname is not None:
    character["githubname"] = githubname
  if name is not None:
    character["name"] = name
  if commits is not None:
    character["commits"] = commits
  if last_commit_nom is not None:
    character["LastCommitNom"] = last_commit_nom
  if last_commit_date is not None:
    character["LastCommitDate"] = last_commit_date

  with open('characters.json', 'w') as f:
    for i, line in enumerate(lines):
      if i == index:
        f.write(json.dumps(character) + '\n')
      else:
        f.write(line)

  return True


async def send_periodic_message(channel):
  while toggleScrap:
    print(toggleScrap)
    #await channel.send('Message envoyé toutes les 20 secondes !')

    arrayUrl = [
      'https://github.com/CabaretRomain/TP3',
      'https://github.com/Yasserbenanane/TP3',
      'https://github.com/WilliamBegue/TP3', 'https://github.com/raihanadz/DZ',
      'https://github.com/prasanthcadirvele/tphtmlcssfinal',
      'https://github.com/rathusan01/formulaire.io',
      'https://github.com/dbneUO/Matttt',
      'https://github.com/WilliamJordan02/WilliamJordanJs',
      'https://github.com/DorianRecharach/portefolio',
      'https://github.com/BgameB/site-PRINCIPAL-BTS-SIO-1E-ANNEE-BRICE',
      'https://github.com/jocespr/site1',
      'https://github.com/Malle02/iframe.ML',
      'https://github.com/Jonah92160/dossier-double-page',
      'https://github.com/EssohEvan/Site1',
      'https://github.com/Anwar101293/tp-2-dev',
      'https://github.com/OumarS21/IFRAME',
      'https://github.com/Ibra94000/iframe_',
      'https://github.com/WilfriedSIO/Site',
      'https://github.com/Darshanprkh/IFRAME',
      'https://github.com/Goldfinger212/portfolio',
      'https://github.com/maellyettia17/Portfolio',
      'https://github.com/GoldVetal/Portfolio_laprog',
      'https://github.com/Samiramaiga/portfolio',
      'https://github.com/maimounaaa/site_MK',
      'https://github.com/maissa17/portfolio1',
      'https://github.com/eliasmw78/sitedeelias',
      'https://github.com/Nico91170/TP-Nicolas-Pires-De-Jesus-BTS-SIOS',
      'https://github.com/jimistay/projet', 'https://github.com/kais922/site3',
      'https://github.com/tristanplsrd/tristanplsrd',
      'https://github.com/wSky111/siteweb/',
      'https://github.com/cgollain/portfolio',
      'https://github.com/Strik0w0/Strik0w0.github.io',
      'https://github.com/Damien-Codes/Portfolio-2050',
      'https://github.com/Ma902/portfolio',
      'https://github.com/Rithik-Mutsuddy/PortfolioRM',
      'https://github.com/Florimondbeckerich/PORTFOLIO',
      'https://github.com/acheurfi/portfolio'
    ]

    for i in range(len(arrayUrl)):

      response = requests.get(arrayUrl[i])
      time.sleep(2)

      if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('title')
        print("\n", title.text)

        span = soup.findAll('span')

        for value in span:
          a = value.find('strong')

          if (a != None):
            commit = a
            html = str(commit)
            soup = BeautifulSoup(html, 'html.parser')
            text = soup.get_text()
            break
        print("Commits :", text)

        response = requests.get(arrayUrl[i] + "/commits/main")
        time.sleep(1)

        if response.ok:
          soup = BeautifulSoup(response.text, 'html.parser')
          title = soup.find('title')
          print("\n", title.text)

          first_a_text = soup.select_one('p.mb-1').find('a').get_text()
          date = soup.select_one('h2').get_text()

          print(" Nom du commit :", first_a_text)

          date = re.sub(r'^Commits on\s*', '', date)
          print(" date de publication :", date)

          pattern = " · (.+?)/"
          resultat = re.search(pattern, title.text)
          GithubUser = resultat.group(1)

          if (read_json_line(i) == None):
            write_to_json(GithubUser, 'Unknow', text, first_a_text, date)
            #time.sleep(2)
            current_time = time.strftime("%H:%M:%S")

            embed = discord.Embed(title=GithubUser,
                                  url=arrayUrl[i],
                                  description=read_json_line(i)['name'],
                                  color=0x050505)
            embed.add_field(name="Nombre de modifications",
                            value=text,
                            inline=False)
            embed.add_field(name="Dernière modification",
                            value=first_a_text,
                            inline=True)
            embed.add_field(name="Date de modification",
                            value=date,
                            inline=True)
            embed.set_footer(text=current_time)
            await channel.send(embed=embed)
            #await channel.send( GithubUser + ' ---------------- ALERT NO DATA-----------------')
            print("---------------- ALERT NO DATA-----------------")
            print(read_json_line(i))
            #time.sleep(1)
          else:
            if (read_json_line(i)['githubname'] != GithubUser
                or read_json_line(i)['commits'] != text
                or read_json_line(i)['LastCommitNom'] != first_a_text
                or read_json_line(i)['LastCommitDate'] != date):
              current_time = time.strftime("%H:%M:%S")

              embed = discord.Embed(title=GithubUser,
                                    url=arrayUrl[i],
                                    description=read_json_line(i)['name'],
                                    color=0x050505)
              embed.add_field(name="Nombre de modifications",
                              value=text,
                              inline=False)
              embed.add_field(name="Dernière modification",
                              value=first_a_text,
                              inline=True)
              embed.add_field(name="Date de modification",
                              value=date,
                              inline=True)
              embed.set_footer(text=current_time)
              await channel.send(embed=embed)

              #await channel.send(GithubUser + ' ---------------- ALERT DIF DATA-----------------')
              print("---------------- ALERT DIF DATA -----------------")
              update_json_line(i,
                               githubname=GithubUser,
                               commits=text,
                               last_commit_nom=first_a_text,
                               last_commit_date=date)
              #time.sleep(1)
            else:

              #await channel.send(GithubUser + ' ---------------- ALERT NO CHANGE-----------------')
              print("---------------- NO CHANGE -----------------")
              #time.sleep(1)
            """
                        print("---")
                        print(read_json_line(i)['githubname'], " - ", GithubUser)
                        print(read_json_line(i)['commits'], " - ", text)
                        print(read_json_line(i)['LastCommitNom'], " - ", first_a_text)
                        print(read_json_line(i)['LastCommitDate'], " - ", date)

                        print("|")
                        print(read_json_line(i))
                        print("---")
                        """

      else:
        print(response)

      print("\n=======\n")

    await asyncio.sleep(600)


# --- COMMAND
async def get_response(message: discord.Message) -> str:
  p_message = message.content.lower()

  global toggleScrap

  command = ".spy "
  ALLOWED_CHANNELS = [1079088683950546964]

  if message.channel.id in ALLOWED_CHANNELS:

    if p_message == command + 'on':
      toggleScrap = True
      print(toggleScrap)
      return '`-- 🔧 ACTIVATION DU MODE SPY 🔧 kc -- ` donc <@268820219290583042> relance le moi  !'
      #return '`-- 🟢 ACTIVATION DU MODE SPY 🟢 --`'
    elif p_message == command + 'off':
      toggleScrap = False
      print(toggleScrap)
      return '`-- 🔴 DÉSACTIVATION DU MODE SPY 🔴 --`'
    elif p_message == command + 'hello':
      return 'Hey there!'


async def send_test_response(message):
  embedVar = discord.Embed(title="SpyBoard",
                           description="Un nouveau monde s'ouvre à nous = )",
                           color=0x000000)
  embedVar.add_field(name=".spy <command>",
                     value="- Affichage de toutes les commandes",
                     inline=True)
  embedVar.add_field(name=".spy 1", value="- data ", inline=True)
  embedVar.add_field(name="undefined", value="undefined", inline=False)
  embedVar.add_field(name="undefined", value="undefined", inline=True)
  embedVar.set_footer(text="By Moi 🦾🗿")

  response = ""
  await message.channel.send(response, embed=embedVar)


# --- gestion
async def send_message(message, user_message, is_private):
  try:
    response = await get_response(message)
    if is_private:
      await message.author.send(response)
    else:
      await message.channel.send(response)

  except Exception as e:
    print(e)


def run_discord_bot():
  intents = discord.Intents.default()
  intents.message_content = True
  client = discord.Client(intents=intents)

  @client.event
  async def on_ready():
    print(f'{client.user} is now running!')
    channel = client.get_channel(1079087676235448452)

    await send_periodic_message(channel)

    client.loop.create_task(send_periodic_message(channel))

  @client.event
  async def on_message(message):
    if message.author == client.user:
      return

    username = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel)

    print(f'{username} said: "{user_message}" ({channel})')

    if user_message.startswith('?'):
      user_message = user_message[1:]
      await send_message(message, user_message, is_private=True)
    else:
      await send_message(message, user_message, is_private=False)

  #client.run(TOKEN)
