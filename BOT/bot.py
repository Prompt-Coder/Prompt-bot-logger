import discord
from discord.ext import commands, tasks
import requests
from bs4 import BeautifulSoup
import asyncio


client = commands.Bot(command_prefix='.')


# .help


@client.event
async def on_ready():
    print('Bot is here')
    server_time.start()
    auto_updating_dead_list.start()


@client.command(pass_context=True)
async def hello(ctx, written):
    await ctx.send(f'hello im a bot {written}')


@tasks.loop(minutes=5)
async def server_time():
    if online_time() >= 0 and online_time() < 1:
        channel = client.get_channel(714090432317095946)
        await channel.send(f'Пора на грузы ебать - **{now_time()}**')


@client.command(pass_context=True)
async def time(game_time):
    await game_time.send(f'**{now_time()}**')


URL = 'https://dednet.ru/servers'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Mobile Safari/537.36',
    'accept': '*/*'}


def now_time():
    html = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(html.text, 'html.parser')
    items = soup.find_all('label')
    current_time = ' '.join(set((items[0])))
    return current_time


def dead_players():
    html = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(html.text, 'html.parser')
    items = soup.find('table', class_='highlight responsive-table').get_text()
    deads_info = items.split('>')
    deads_info_2 = '>'.join(deads_info)
    deads_info_3 = deads_info_2.split('\n')[12:]

    return deads_info_2



def dead_last_func():
    dead_logs = open('logs.txt', 'r', encoding='utf-8')
    deads_last = (dead_logs.read()).split('\n')[1:] # инфа которая уже есть
    dead_logs.close()
    return deads_last


# print(deads_now[0:])
# print(deads_last[0:])



def union_deads_func():  # получение словаря из списка deads_now
    dead_players_now = dead_players()# информация на теккущий момент
    deads_now = dead_players_now.split('\n')[12:]

    dead_players_data = []
    a = 0
    b = 1
    c = 2
    d = 3
    e = 4
    f = 5
    g = 6
    for i in deads_now:
        dead_players_data.append(
            (deads_now[a] + ' ' + deads_now[b] + ' ' + deads_now[c] + ' ' + deads_now[d] + ' ' + deads_now[e] + ' ' +
             deads_now[f] + ' ' + deads_now[g])
        )
        a = a + 7
        b = b + 7
        c = c + 7
        d = d + 7
        e = e + 7
        f = f + 7
        g = g + 7
        if a + 7 > len(deads_now):
            break
    for g in range(len(dead_players_data)):
        dead_players_data[g] = dead_players_data[g].strip()
    return (dead_players_data)


print('\n'.join(union_deads_func()))

print('----------------------------------------------------------------------'
      '---------------------------------------------------------------------'
      '----------------------------------------------------------------------')
print(dead_last_func())

print('------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')

def uniqe_dead_list(): #переписать
    result = list(set(union_deads_func()) - set(dead_last_func()))
    if len(result) != 0:
        my_list = '\n'.join(result)
        deads_last_w = open('logs.txt', 'a', encoding='utf-8')
        deads_last_w.write(f'{my_list}\n')
        deads_last_w.close()
        print('Добавлено')
    print(len(result), '\n'.join(result))
    return len(result), '\n'.join(result)

@tasks.loop(seconds=5)
async def auto_updating_dead_list():
          uniqe_dead_list()




def online_time():
    return int(((now_time().split(' '))[2]).split(':')[0])


token = open('token.txt', 'r').readline()
client.run(token)
