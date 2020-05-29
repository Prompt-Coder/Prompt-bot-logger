def now_time():
    html = requests.get(URL, headers = HEADERS)
    soup = BeautifulSoup(html.text, 'html.parser')
    items = soup.find_all('label')
    current_time = ' '.join(set((items[0])))
    return current_time

num = 1
while num < 10:
    now_time()