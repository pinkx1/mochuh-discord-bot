import random
import os
import discord
from discord.ext import commands
from discord_slash import SlashCommand
from dotenv import load_dotenv
from email import message
from inspect import getcomments
from time import sleep
import asyncio
import asyncpg

load_dotenv()
token = os.getenv('token')

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)


async def connect_to_db():
    db_user = os.getenv('db_user')
    db_password = os.getenv('db_password')
    db_host = os.getenv('db_host')
    db_database = os.getenv('db_database')
    try:
        connection = await asyncpg.create_pool(user=db_user,
                                               password=db_password,
                                               host=db_host,
                                               port=5432,
                                               database=db_database)
        print("Successfully connected to the database")
        return connection
    except (Exception, asyncpg.Error) as error:
        print("Error while connecting to PostgreSQL", error)





@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error


@bot.event
async def on_ready():
    print('Bot connected')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('жижу 2'))
    global connection
    connection = await connect_to_db()


@commands.has_permissions(administrator=True)
@bot.command()
async def say(ctx, *, arg):
    await ctx.channel.purge(limit = 1)
    await ctx.send(arg)


@slash.slash(description="Лобби SiGame")
async def sigame(ctx):
    await ctx.send('Программа на пк: <https://vladimirkhil.com/si/game>\n'
                                    'Онлайн: <https://vladimirkhil.com/si/online/>\n'
                                    'Название лобби: gay123\n'
                                    'Пароль: 1099\n',
                                    file=discord.File('./sigame.png'))


@slash.slash(description="Бросить монетку")
async def coinflip(ctx):
    await ctx.send(random.choice(['Орел', 'Решка']))


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(973593062045548636)
    await channel.send(f"{member.mention} проскальзывает на сервер! Ласкаво просимо!")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    user_id = message.author.id
    # Проверяем наличие пользователя в базе данных
    sql = "SELECT * FROM users WHERE discord_id = $1"
    user_data = await connection.fetchrow(sql, user_id)
    if user_data:
        # Если пользователь есть в базе данных, то обновляем messages_count
        sql = "UPDATE users SET messages_count = messages_count + 1 WHERE discord_id = $1"
        await connection.execute(sql, user_id)
    else:
        # Если пользователя нет в базе данных, то добавляем его
        sql = "INSERT INTO users(discord_id, messages_count) VALUES($1, 1)"
        await connection.execute(sql, user_id)

    if message.author == bot.user:
        return

    if message.content.lower() in ("да", "дa", "da", "dа"):
        chance = random.randint(1,4)
        if chance == 1:
            await message.channel.send(content='пизда')

    if message.content.lower() == "нет":
        chance = random.randint(1,4)
        if chance == 1:
            await message.channel.send(content='пидора ответ')

    if message.content.lower() == ("300", "триста"):
        chance = random.randint(1,4)
        if chance == 1:
          await message.channel.send(content='отсоси у тракториста')

    if message.author == bot.user:
        return
    if str(message.author.roles).find('1016367823490134027') != -1:
        await message.add_reaction('💩')

    if message.attachments != [] and message.channel.id != 973593062045548636 and message.channel.id != 1004034044297756673:
        await message.add_reaction('💖')
        sleep(0.1)
        await message.add_reaction('👍')
        sleep(0.1)
        await message.add_reaction('👎')
    if str(message.content).rfind("https://") != -1 and message.channel.id != 973593062045548636 and message.channel.id != 1004034044297756673:
        await message.add_reaction('💖')
        sleep(0.1)
        await message.add_reaction('👍')
        sleep(0.1)
        await message.add_reaction('👎')

    await bot.process_commands(message)


@bot.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 1039187036600553522:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds) 

        if payload.emoji.name == 'sigame':
            role = discord.utils.get(guild.roles, name='Своя Игра')
        elif payload.emoji.name == 'dota2':
            role = discord.utils.get(guild.roles, name='Dota 2')
        elif payload.emoji.name == 'leagueoflegends':
            role = discord.utils.get(guild.roles, name='League of Legends')
        elif payload.emoji.name == 'wow':
            role = discord.utils.get(guild.roles, name='World of Warcraft')
        else:
            role = discord.utils.get(guild.roles, name=payload.emoji.name)

        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.add_roles(role)
                print('done')
            else:
                print('Member not found.')
        else:
            print('Role not found.')


@bot.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if message_id == 1039187036600553522:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds) 

        if payload.emoji.name == 'sigame':
            role = discord.utils.get(guild.roles, name='Своя Игра')
        elif payload.emoji.name == 'dota2':
            role = discord.utils.get(guild.roles, name='Dota 2')
        elif payload.emoji.name == 'leagueoflegends':
            role = discord.utils.get(guild.roles, name='League of Legends')
        elif payload.emoji.name == 'wow':
            role = discord.utils.get(guild.roles, name='World of Warcraft')
        else:
            role = discord.utils.get(guild.roles, name=payload.emoji.name)

        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)
                print('done')
            else:
                print('Member not found.')
        else:
            print('Role not found.')


@commands.has_permissions(administrator=True)
@bot.command()
async def bump(ctx):
    await ctx.channel.purge(limit = 1)
    import http.client
    import mimetypes
    from codecs import encode

    conn = http.client.HTTPSConnection("2ch.hk")
    cookie = os.getenv('cookie')
    boundary = os.getenv('boundary')
    usercode = os.getenv('usercode')
    thread_link = os.getenv('thread_link')
    thread_id = os.getenv('thread_id')
    
    dataList = []
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=task;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode("post"))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=board;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode("ch"))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=thread;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode(thread_id))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=usercode;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode(usercode))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=captcha_type;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode("2chcaptcha"))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=formimages[];'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode("(binary)"))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=comment;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode("bump"))
    dataList.append(encode('--'+boundary+'--'))
    dataList.append(encode(''))
    body = b'\r\n'.join(dataList)
    payload = body
    headers = {
        'scheme': 'https',
        'path': '/user/posting?nc=1',
        'method': 'POST',
        'authority': '2ch.hk',
        'x-requested-with': 'XMLHttpRequest',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'referer': thread_link,
        'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
        'cookie': cookie,
        'origin': 'https://2ch.hk',
        'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
    }
    conn.request("POST", "/user/posting?nc=1", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))


    emoji = discord.utils.get(bot.emojis, name='EZ')
    await ctx.send('Бампнул тредю ' + str(emoji))
    
bot.run(token)

