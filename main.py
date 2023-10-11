import requests
from bs4 import BeautifulSoup
from sidedatas import headers


def get_max_pages(url):
    responce = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(responce.text, 'lxml')
    all_pages = str(soup.find_all('div', class_="pagination-wrapper"))
    page_list = [int(i) for i in all_pages if i.isdigit()]
    max_number_pages = max(page_list)
    return max_number_pages


def collect_data(url):
    responce = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(responce.text, 'lxml')
    with open("data.html", 'a', encoding='utf-8') as file:
        all_links = soup.find_all('a', href=lambda x: x and x.startswith("https://forums"))
        link = [link['href'] for link in all_links[1:]]
        for row in link:
            file.write(row + "\n")


number_of_pages = get_max_pages(url='https://www.grimtools.com/builds/mastery/druid')
#пока такой урл, в дальнейшем прост череще инпут все равно

for i in range(1, number_of_pages + 1):
    collect_data(url=f'https://www.grimtools.com/builds/mastery/druid/{i}')


def get_grimtools():
    pages =[]
    with open('data.html', 'r') as file:
        for row in file:
            pages.append(row.rstrip())
    with open("grimtols.html", 'a', encoding='utf-8') as f:
        for line in pages:
            try:
                responce = requests.get(url=line, headers=headers)
                soup = BeautifulSoup(responce.text, 'lxml')
                all_links = soup.find_all('a', href=lambda x: x and x.startswith("https://www.grimtools"))
                link = [link['href'] for link in all_links]
                f.write(str(link[0]) + "\n")
            except Exception as ex:
                print(ex)




get_grimtools()
