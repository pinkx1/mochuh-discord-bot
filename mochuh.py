import random
import os
import discord
from discord import member
from discord.ext import commands
from discord_slash import SlashCommand
from dotenv import load_dotenv
from email import message
from inspect import getcomments
from time import sleep
import asyncio
import asyncpg
from typing import List
import datetime

load_dotenv()
token = os.getenv('token')
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)


no_bot_reaction_channels = [973593062045548636,
                            1004034044297756673,
                            1065638324380909649,
                            1061571232094502942,
                            1057994630731415582,
                            1034698950369874010,
                            983364354521063444,
                            1004034044297756673,
                            1050397252889346099,
                            1044239842680258731,
                            974615451638317106,
                            1024728422724943893,
                            1020734141328797777,
                            1038853570159714464,
                            1064961124153438339,
                            1085563045020975256]


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


async def check_achievement(discord_id: int, message_count: int, message):
    if message_count >= 2000:
        existing_achievement_spacemaker = await connection.fetchval("SELECT COUNT(*) "
                                                         "FROM achievements "
                                                         "WHERE discord_id = $1 "
                                                         "AND achievement_name = 'Спейсователь'", discord_id)

        if existing_achievement_spacemaker == 0:
            await connection.execute("INSERT INTO achievements (discord_id, achievement_name) "
                                     "VALUES ($1, 'Спейсователь')", discord_id)
            user = bot.get_user(discord_id)
            channel = bot.get_channel(1034698950369874010)
            await channel.send(f"{user.mention} получил ачивку «Спейсователь» за 2000 сообщений на сервере!")

    if 'получка' in message.content.lower():
        existing_achievement_poluchka = await connection.fetchval("SELECT COUNT(*) "
                                                                    "FROM achievements "
                                                                    "WHERE discord_id = $1 "
                                                                    "AND achievement_name = 'Прадед'", discord_id)

        if existing_achievement_poluchka == 0:
            await connection.execute("INSERT INTO achievements (discord_id, achievement_name) "
                                     "VALUES ($1, 'Прадед')", discord_id)
            user = bot.get_user(discord_id)
            channel = bot.get_channel(1034698950369874010)
            await channel.send(f"{user.mention} получил ачивку «Прадед»")


async def get_achievements(discord_id) -> List[str]:
    query = 'SELECT achievement_name ' \
            'FROM achievements ' \
            'WHERE discord_id = $1'
    achievements = await connection.fetch(query, discord_id)
    return [a["achievement_name"] for a in achievements]


async def get_message_count(discord_id):
    query = 'SELECT messages_count ' \
            'FROM users ' \
            'WHERE discord_id = $1'
    result = await connection.fetchval(query, discord_id)
    return result


spam_protection = {}
spam_list = []


def add_user_to_spam_list(user_id):
    current_time = datetime.datetime.now()
    if user_id in spam_protection:
        if (current_time - spam_protection[user_id]['last_message_time']).total_seconds() < 60:
            spam_protection[user_id]['message_count'] += 1
        else:
            spam_protection[user_id]['message_count'] = 1
    else:
        spam_protection[user_id] = {'last_message_time': current_time, 'message_count': 1}
    if spam_protection[user_id]['message_count'] > 7:
        spam_list.append(user_id)


def check_spam_list():
    current_time = datetime.datetime.now()
    for user_id in list(spam_list):
        if (current_time - spam_protection[user_id]['last_message_time']).total_seconds() > 300:
            del spam_list[user_id]


async def remove_user_from_spam_list(user_id):
    spam_list.pop(user_id, None)


async def add_exp(exp: int, user_id: int):
    if user_id in spam_list:
        return
    await connection.execute("INSERT INTO users (discord_id, exp) "
                             "VALUES ($1, $2) "
                             "ON CONFLICT (discord_id) "
                             "DO UPDATE SET exp = users.exp + $2",
                             user_id, exp)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error


@bot.event
async def on_ready():
    print('Bot connected')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('приколы'))
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


@slash.slash(description="Количество твоих сообщений")
async def messages_count(ctx):
    user_id = ctx.author.id
    sql = "SELECT messages_count " \
          "FROM users " \
          "WHERE discord_id = $1"
    result = await connection.fetchrow(sql, user_id)
    if result:
        messages_count = result["messages_count"]
        await ctx.send(f"Количество твоих сообщений: {messages_count}")
    else:
        await ctx.send("Не удалось найти твою запись в базе данных.")


#@bot.command(name='ачивки')
@slash.slash(description="Твои ачивки")
async def achievements(ctx):
    author = ctx.author
    discord_id = author.id
    achievements = await get_achievements(discord_id)
    if achievements:
        achievement_list = "\n".join(achievements)
        await ctx.send(f'{author.mention}, ваши ачивки:\n{achievement_list}')
    else:
        await ctx.send(f'{author.mention}, у вас пока нет ачивок =(')



@slash.slash(description="Бросить монетку")
async def coinflip(ctx):
    await ctx.send(random.choice(['Орел', 'Решка']))


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1085563045020975256)
    emoji_pepe_basedge = discord.utils.get(bot.emojis, name='pepeBasedge')
    emoji_nonono = discord.utils.get(bot.emojis, name='nonono')

    await asyncio.sleep(5)
    await channel.send(f"{member.mention} привет! Для того, чтобы получить доступ к основному чату, тебе нужно побалакать с кем-нибудь из модеров {emoji_pepe_basedge}{emoji_nonono}")


@bot.event
async def on_member_remove(member):
    emoji_pepe_cleaner = discord.utils.get(bot.emojis, name='cleaner')
    channel = bot.get_channel(1064961124153438339)
    await channel.send(f"{member.mention} был смыт в унитаз")
    await channel.send(f"{emoji_pepe_cleaner}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    user_id = message.author.id
    sql = "SELECT * " \
          "FROM users " \
          "WHERE discord_id = $1"
    user_data = await connection.fetchrow(sql, user_id)
    if user_data:
        sql = "UPDATE users " \
              "SET messages_count = messages_count + 1 " \
              "WHERE discord_id = $1"
        await connection.execute(sql, user_id)
    else:
        sql = "INSERT INTO users(discord_id, messages_count) " \
              "VALUES($1, 1)"
        await connection.execute(sql, user_id)

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

    if message.channel.id == 1016973280940408843:
        pepeheadphones_emoji = discord.utils.get(message.guild.emojis, name='pepeheadphones')
        if pepeheadphones_emoji is not None:
            await message.add_reaction(pepeheadphones_emoji)
            await message.add_reaction('👍')
            await message.add_reaction('👎')
    else:
        if (message.attachments != [] or str(message.content).rfind(
                "https://") != -1) and message.channel.id not in no_bot_reaction_channels:
            await message.add_reaction('💖')
            await message.add_reaction('👍')
            await message.add_reaction('👎')

    await bot.process_commands(message)

    message_count = await get_message_count(user_id)
    await check_achievement(user_id, message_count, message)

    exp = random.randint(5, 15)
    await add_exp(exp, user_id)
    add_user_to_spam_list(user_id)
    check_spam_list()


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

