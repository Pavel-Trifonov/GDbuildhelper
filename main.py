import requests
from bs4 import BeautifulSoup
from sidedatas import headers
from sidedatas import classes


def get_max_pages(url):
    responce = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(responce.text, 'lxml')
    all_pages = str(soup.find_all('div', class_="pagination-wrapper"))
    page_list = [int(i) for i in all_pages if i.isdigit()]
    max_number_pages = max(page_list)
    return max_number_pages


# def collect_data(url):
#     responce = requests.get(url=url, headers=headers)
#     soup = BeautifulSoup(responce.text, 'lxml')
#     with open(f"{class_in_url}.html", 'a', encoding='utf-8') as file:
#         all_links = soup.find_all('a', href=lambda x: x and x.startswith("https://forums"))
#         link = [link['href'] for link in all_links[1:]]
#         for row in link:
#             file.write(row + "\n")

# #пока такой урл, в дальнейшем прост череще инпут все равно


def list_of_data(class_in_url):
    pages = []
    with open(f"{class_in_url}.html", 'r') as file:
        for row in file:
            pages.append(row.rstrip())
    return pages


def get_grimtools(class_in_url):
    pages = list_of_data(class_in_url)
    with open(f"{class_in_url}-gt.html", 'a', encoding='utf-8') as f:
        for line in pages:
            try:
                responce = requests.get(url=line, headers=headers)
                soup = BeautifulSoup(responce.text, 'lxml')
                all_links = soup.find_all('a', href=lambda x: x and x.startswith("https://www.grimtools.com/calc"))
                link = [link['href'] for link in all_links]
                f.write(str(link[0]) + "\n")
            except Exception as ex:
                print(ex)


def list_of_gt(class_in_url):
    gtpages = []
    with open(f"{class_in_url}-gt.html", 'r') as file:
        for row in file:
            gtpages.append(row.rstrip())
    return gtpages


def final_result():
    for clas in classes:
        classs = clas
        number_of_pages = get_max_pages(url=f'https://www.grimtools.com/builds/mastery/{classs}')
        for i in range(1, number_of_pages + 1):
            url=f'https://www.grimtools.com/builds/mastery/{classs}/{i}'
            responce = requests.get(url=url, headers=headers)
            soup = BeautifulSoup(responce.text, 'lxml')
            with open(f"{classs}.html", 'a', encoding='utf-8') as file:
                all_links = soup.find_all('a', href=lambda x: x and x.startswith("https://forums"))
                link = [link['href'] for link in all_links[1:]]
                for row in link:
                    file.write(row + "\n")
        list_of_data(classs)
        get_grimtools(classs)


# final_result()
