import random
import os
import discord
from dotenv import load_dotenv
import asyncio
import asyncpg
from typing import List
import datetime
from datetime import datetime
import Bumper
from discord.ext import commands
from discord_slash import SlashContext, SlashCommand


load_dotenv()
token = os.getenv('token')
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
client = discord.Client()
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
                            1085563045020975256,
                            1102235103008149544,
                            1109067479185100860,
                            1143873808835551403]


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


async def get_message_count(discord_id):
    query = 'SELECT messages_count ' \
            'FROM users ' \
            'WHERE discord_id = $1'
    result = await connection.fetchval(query, discord_id)
    return result


allowed_users = [417432559086206977]


@slash.slash(
    name="clear",
    description="Удаляет последние N сообщений в текущем канале",
    options=[
        {
            "name": "amount",
            "description": "Количество сообщений для удаления",
            "type": 4,
            "required": True
        }
    ]
)
async def clear(ctx: SlashContext, amount: int):
    if ctx.author.id in allowed_users:
        await ctx.channel.purge(limit=amount)
        await asyncio.sleep(1)
        await ctx.send(f"Удалено {amount} сообщений.")
    else:
        emoji_pepeMegaSmile = discord.utils.get(bot.emojis, name='pepeMegasmile')
        await ctx.send(f"Вы не имеете доступа к этой команде.")
        await ctx.send(f" {emoji_pepeMegaSmile} ")


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
async def say(ctx, *, message=None):
    await ctx.channel.purge(limit=1)
    if len(ctx.message.attachments) > 0:
        attachment = ctx.message.attachments[0]
        await ctx.send(message or "", file=await attachment.to_file())
    else:
        await ctx.send(message)


@slash.slash(description="Лобби SiGame")
async def sigame(ctx):
    await ctx.send('Программа на пк: <https://vladimirkhil.com/si/game>\n'
                   'Онлайн: <https://vladimirkhil.com/si/online/>\n'
                   'Название лобби: gay123\n'
                   'Пароль: 1099\n',
                   file=discord.File('./SiGameStart.gif'))


@slash.slash(description="Количество твоих сообщений")
async def messages_count(ctx):
    user_id = ctx.author.id
    emoji_pepeSmart = discord.utils.get(bot.emojis, name='pepeSmart')

    sql = "SELECT messages_count " \
          "FROM users " \
          "WHERE discord_id = $1"
    result = await connection.fetchrow(sql, user_id)

    if result:
        messages_count = result["messages_count"]
        await ctx.send(f"Количество твоих сообщений: {messages_count}")
    else:
        await ctx.send(f"Не удалось найти твою запись в базе данных {emoji_pepeSmart}")


@slash.slash(description="Бросить монетку")
async def coinflip(ctx):
    await ctx.send(random.choice(['Орел', 'Решка']))


@bot.event
async def on_member_remove(member):
    emoji_pepe_cleaner = discord.utils.get(bot.emojis, name='cleaner')
    channel = bot.get_channel(1064961124153438339)
    await channel.send(f"{member.mention}, известный под именем {member.name}, покинул сервер")
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
        chance = random.randint(1, 4)
        if chance == 1:
            await message.channel.send(content='пизда')

    if message.content.lower() == "нет":
        chance = random.randint(1, 4)
        if chance == 1:
            await message.channel.send(content='пидора ответ')

    if message.content.lower() == ("300", "триста"):
        chance = random.randint(1, 4)
        if chance == 1:
            await message.channel.send(content='отсоси у тракториста')

    if message.author == bot.user:
        return
    if str(message.author.roles).find('1016367823490134027') != -1:
        await message.add_reaction('💩')

    if message.channel.id == 1016973280940408843:
        if (message.attachments != [] or str(message.content).rfind(
                "https://") != -1):
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


@bot.command(aliases=['не'])
async def nesrat(ctx):
    await ctx.channel.purge(limit=1)
    emoji2 = discord.utils.get(bot.emojis, name='pepeBasedge')
    emoji3 = discord.utils.get(bot.emojis, name='nonono')
    await ctx.send(str(emoji2) + str(emoji3) + ' НЕ СРАТЬ')


@commands.has_permissions(administrator=True)
@bot.command()
async def bump(ctx):
    await ctx.channel.purge(limit=1)
    
    temp_bumper = Bumper
    temp_bumper.bump_function()
    
    emoji = discord.utils.get(bot.emojis, name='EZ')
    await ctx.send('Бампнул тредю ' + str(emoji))


bot.run(token)

