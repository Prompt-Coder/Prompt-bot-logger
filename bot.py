import discord
from discord.ext import commands, tasks
import requests
from bs4 import BeautifulSoup
import asyncio
import copy

client = commands.Bot(command_prefix='.')
client.remove_command('help')


# .help
@client.command(pass_context=True)
async def help(help_message):
    await help_message.send(
        'Команды для бота:\n1. **.time** (показывает время на севрере)\n2. **.dead Имя Фамилия** (ищет все данные об игроке в дедлисте (**СОБИРАЕТ ЛОГИ ТОЛЬКО С 23.05.2020!!!**)\nПример использования команды .dead - (``.dead Suchimi Nakachimi)``')


@client.event
async def on_ready():
    print('Bot is here')
    server_time.start()
    dead_users.start()


    await client.change_presence(activity=discord.Game('.help'))


@client.command(pass_context=True)
async def hello(ctx, written):
    await ctx.send(f'hello im a bot {written}')


@tasks.loop(minutes=7)
async def server_time():
    if online_time() >= 0 and online_time() < 1:
        channel = client.get_channel(714090432317095946)
        role_mention = "706550950726205454"
        await channel.send(f' Пора на грузы ебать - **{now_time()}**')


@client.command(pass_context=True)
async def time(game_time):
    await game_time.send(f'**{now_time()}**')


@client.command(pass_context=True)
async def dead(message, *name):
    obtain_message = ' '.join(name)
    answer = dead_answer(obtain_message)
    await message.send(f'{answer}')


@client.command(pass_context=True)
async def dead_requests(command, *requests_name):
    names = ''.join(' '.join(requests_name)).split(', ')
    channel = command.channel.id
    inf = list(names)
    inf.append(f'{channel}')
    data_list = []
    number = 0
    for i in inf:
        data_list.append(inf[number])
        number = number + 1
    information = (', '.join(data_list))
    await command.send('Добавление..')
    logs_check = open('players_data.txt', 'r', encoding='utf-8')
    checking = logs_check.read()
    logs_check.close()
    print(checking)
    if checking == information:
        await command.send(f'Имена: **{", ".join(information.split(", ")[:-1])}** уже в списке')
    elif checking != inf:
        dead_data = open('players_data.txt', 'w', encoding='utf-8')
        dead_data.write(information)
        dead_data.close()
        await command.send(f'Имена были обновлены на **{", ".join(information.split(", ")[:-1])}**')
    return information


@tasks.loop(hours=1)
async def dead_users():
    catch = copy.copy(catcher())
    if len(catch) != 0:
        users = '\n'.join(catch)
        logs_check = open('players_data.txt', 'r', encoding='utf-8')
        checking = logs_check.read()
        logs_check.close()
        chan = int(checking.split(', ')[-1])
        channel = client.get_channel(chan)
        await channel.send(f'**{users}**')


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


def dead_answer(my_name):
    opening = open('logs.txt', 'r', encoding='utf-8')
    deads_last = (opening.read()).split('\n')[1:]  # инфа которая уже есть
    opening.close()
    variable = deads_last
    numeral = 0
    dead_search = []
    for i in variable:  # соединяем все провиннлсти игрока в единый список
        full_name_list = (''.join(variable[numeral]).split(' ')[1] + ' ' + ''.join(variable[numeral]).split(' ')[2])
        full_name_list_2 = (''.join(variable[numeral]).split(' ')[2] + ' ' + ''.join(variable[numeral]).split(' ')[3])
        if_server_url = ''.join(variable[numeral]).split(' ')[-1]
        if_url = "".join(variable[numeral]).split("#")[-1]
        if_url_2 = "".join(variable[numeral]).split("№")[-1]
        svetofor = (''.join(variable[numeral]).split(' ')[0] + ' ' + ''.join(variable[numeral]).split(' ')[1])
        if ''.join(variable[numeral]).split(' ')[
            0] == 'Server':  # если первое слово равно server, берем 2 и 3е слово для имени
            if full_name_list == my_name:
                dead_search.append(variable[numeral] + '\n')
                if if_server_url.isdigit():  # добавляем ссылку в жалобу, если в конце число
                    dead_search.append(f'Ссылка на жалобу: https://dednet.ru/report-id-{if_server_url}')
        if full_name_list_2 == my_name:
            dead_search.append(variable[numeral] + '\n')
            if if_url.isdigit():
                dead_search.append(
                    f'Ссылка на жалобу: https://dednet.ru/report-id-{if_url}')
            elif if_url_2.isdigit():
                dead_search.append(
                    f'Ссылка на жалобу: https://dednet.ru/report-id-{if_url_2}')
            elif svetofor == 'Naix Bennette':
                if if_server_url.isdigit():
                    dead_search.append(f'Ссылка на жалобу: https://dednet.ru/report-id-{if_server_url}')
        numeral = numeral + 1
        if numeral + 2 > len(variable):
            break
        if my_name == 'Jose Ghost':
            return 'О нем лучше не спрашивать'
    if len(dead_search) == 0:
        return f'``С 23.05.20, {my_name}, еще не попадал в дедлист, но все не вечно, да?``)'
    dead_search.reverse()
    return '\n'.join(dead_search)


def dead_last_func():
    dead_logs = open('logs.txt', 'r', encoding='utf-8')
    deads_last = (dead_logs.read()).split('\n')[1:]  # инфа которая уже есть
    dead_logs.close()
    return deads_last


# print(deads_now[0:])
def answering_func():
    join_dead_last = ' '.join(dead_last_func())
    splited_dead_last = join_dead_last
    return join_dead_last


def union_deads_func():  # получение словаря из списка deads_now
    dead_players_now = dead_players()  # информация на теккущий момент
    deads_now = dead_players_now.split('\n')[12:]

    dead_players_data = []
    a = 0
    for i in deads_now:
        dead_players_data.append(
            (deads_now[a] + ' ' + deads_now[a + 1] + ' ' + deads_now[a + 2] + ' ' + deads_now[a + 3] + ' ' + deads_now[
                a + 4] + ' ' +
             deads_now[a + 5] + ' ' + deads_now[a + 6])
        )
        a = a + 7
        if a + 7 > len(deads_now):
            break
    for g in range(len(dead_players_data)):
        dead_players_data[g] = dead_players_data[g].strip()
    return (dead_players_data)

def uniqe_dead_list():
    result = list(set(union_deads_func()) - set(dead_last_func()))
    if len(result) != 0:
        my_list = '\n'.join(result)
        deads_last_w = open('logs.txt', 'a', encoding='utf-8')
        deads_last_w.write(f'{my_list}\n')
        deads_last_w.close()
        print('Добавлено')
    print(len(result), '\n'.join(result))
    x = '\n'.join(result)
    return x


def catcher():
    dead_list = copy.copy(str(uniqe_dead_list()).split('\n'))
    logs_check = open('players_data.txt', 'r', encoding='utf-8')
    checking = logs_check.read()
    logs_check.close()
    dead_users = (checking.split(', ')[:-1])
    users_data = []

    for i in dead_users:
        for e in dead_list:
            if i in e:
                users_data.append(e)
    return users_data
def online_time():
    return int(((now_time().split(' '))[2]).split(':')[0])

# a = ['Choor Chella Jose Ghost 06-02, 15:32 Разбан Откат']
# b = ['Jose Ghost']
# if b[0] in a[0]:
# print('изи')

token = open('token.txt', 'r').readline()
client.run(token)
