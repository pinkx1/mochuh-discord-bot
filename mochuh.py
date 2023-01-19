import random
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from email import message
from inspect import getcomments
from time import sleep
from discordLevelingSystem import DiscordLevelingSystem, LevelUpAnnouncement, RoleAward

load_dotenv()
token = os.getenv('token')

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

main_guild_id = 1050324651034824784 # OLD

test = 973593060992753695
johns_server = 973593060992753695

my_awards = {
    johns_server : [
        RoleAward(role_id=1050323843169919016, level_requirement=10, role_name='Маслёнок'),
        RoleAward(role_id=1047144673979924601, level_requirement=20, role_name='Булочка'),
        RoleAward(role_id=1050323952410566686, level_requirement=30, role_name='Крутой в интернете')
    ]

}


lvlupmessage = f'{LevelUpAnnouncement.Member.mention} апнул уровень {LevelUpAnnouncement.LEVEL} 😎'  # придумать текст лвлапа
announcement = LevelUpAnnouncement(message=lvlupmessage, level_up_channel_ids=(1034698950369874010,))
nitro_booster = 1033058782319742977
kabanchiki = 1040533421908299838
mirnyak = 1050749022111010877
lvl = DiscordLevelingSystem(rate=5000000,awards=my_awards, level_up_announcement=announcement, no_xp_channels=(1034698950369874010,),
                            announce_level_up=True, stack_awards=False, )
#lvl.create_database_file('/home/ec2-user/mochuh-bot/DiscordLevelingSystem.db')
lvl.connect_to_database_file(r'/home/ec2-user/mochuh-bot/DiscordLevelingSystem.db')
print('connected to db')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error

@bot.event
async def on_ready():
    print('bot connected')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('жижу 2'))
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('жижу 2'))


@commands.has_permissions(administrator=True)
@bot.command()
async def say(ctx, *, arg):
    await ctx.channel.purge(limit=1)
    await ctx.send(arg)


@bot.command(aliases=['ранг'])
async def rank(ctx):
    data = await lvl.get_data_for(ctx.author)
    await ctx.send(f'У тебя уровень {data.level} и твой ранг {data.rank}')


@bot.command(aliases=['лидерборд'])
async def leaderboard(ctx):
    data = await lvl.each_member_data(ctx.guild, sort_by='rank')
    for each in data:
        await ctx.send(f'Ранг {each.rank} у {each.name}')


@bot.command(aliases=['не'])
async def nesrat(ctx):
    await ctx.channel.purge(limit=1)
    emoji2 = discord.utils.get(bot.emojis, name='pepeBasedge')
    emoji3 = discord.utils.get(bot.emojis, name='nonono')
    await ctx.send(str(emoji2) + str(emoji3) + ' НЕ СРАТЬ')


@bot.command(aliases=['своя'])
async def sigame(ctx):
    await ctx.send('Программа на пк: <https://vladimirkhil.com/si/game>\n'
                   'Онлайн: <https://vladimirkhil.com/si/online/>\n'
                   'Название лобби: gay123\n'
                   'Пароль: 1099\n',
                   file=discord.File('./sigame.png'))


@bot.command(aliases=['бросить'])
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
    elif message.author.id == 978650416977952808:
        return

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

    if message.attachments != [] and message.channel.id != 973593062045548636 and message.channel.id != 1004034044297756673 and message.channel.id != 1044239842680258731 and message.channel.id != 1061571232094502942 and message.channel.id != 1057994630731415582 and message.channel.id != 1034698950369874010 and message.channel.id != 1038853570159714464 and message.channel.id != 1020734141328797777 and message.channel.id != 1065638324380909649:
        await message.add_reaction('💖')
        sleep(0.1)
        await message.add_reaction('👍')
        sleep(0.1)
        await message.add_reaction('👎')
    if str(message.content).rfind(
            "https://") != -1 and message.channel.id != 973593062045548636 and message.channel.id != 1004034044297756673 and message.channel.id != 1044239842680258731 and message.channel.id != 1061571232094502942 and message.channel.id != 1057994630731415582 and message.channel.id != 1034698950369874010 and message.channel.id != 1038853570159714464 and message.channel.id != 1020734141328797777 and message.channel.id != 1065638324380909649:
        await message.add_reaction('💖')
        sleep(0.1)
        await message.add_reaction('👍')
        sleep(0.1)
        await message.add_reaction('👎')

    await lvl.award_xp(amount=20, message=message, level_up_channel_ids=1034698950369874010, bonus=DiscordLevelingSystem.Bonus([nitro_booster, kabanchiki, mirnyak], 20, multiply=False))
    await bot.process_commands(message)

@bot.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 1039187036600553522:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)

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
            member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
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
        guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)

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
            member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
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
