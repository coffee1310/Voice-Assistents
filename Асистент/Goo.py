import random
import speech_recognition
import pyowm
import requests
import wikipedia
import webbrowser
import os
import fake_useragent
import pymorphy2
from rich.progress import track
from time import sleep
from bs4 import BeautifulSoup
from googletrans import Translator

word_activator = ['глеб','жбаб','ассистент']

sr = speech_recognition.Recognizer()
sr.pause_threshold = 0.5
commands_dict = {
    'commands':{
        'greeting':['hello', 'привет','здравствуй','здравствуйте'],
        'weather':['weather','погода','что на улице','погодка'],
        'search_information':['найди информацию','загугли','поищи','найти'],
        'enter_programm':['создать программу','записать программу','запиши программу','создай программу','ввести программу'],
        'open_programm':["открой программу",'программа','открыть программу'],
        'show_programm':['покажи все программы','покажи мои программы','список программ','показать все программы'],
        'limit_time_listening':['лимит'],
        'show_websites':['список сайтов','сайты'],
        'enter_site':['создать сайт','записать сайт','запиши сайт','создай сайт','ввести сайт'],
        'open_site':['открыть сайт','открой сайт'],
        'open_something':['открой','открыть'],
        'random_image':['случайную картинку','случайное изображение','случайная картинка','случайное изображение','скачай картинку','скачай изображение']
    }
}

def limit_time_listening(query):
    global ltl
    print('Назовите лимит от 2 до 20 секунд')
    try:
        with speech_recognition.Microphone() as mic:
            sr.adjust_for_ambient_noise(source=mic, duration=0.5)
            audio = sr.listen(source=mic, phrase_time_limit=2)
            l_commands = sr.recognize_google(audio_data=audio, language='ru-RU').lower()
            try:
                if 'секунд' in l_commands:
                    if 'ы' in l_commands:
                        l_commands.replace('секунды', '')
                    else:
                        l_commands.replace('секунд', '')
                if listen_command() < 2:
                    print("Слишком мало, вы не успеете ничего сказать!")
                elif l_commands > 20:
                    print("Слишком много, вы успеете заснуть!")
                else:
                    ltl = l_commands
            except Exception:
                print('')
    except speech_recognition.UnknownValueError:
        print("Извините, я вас не расслышал")

ltl = 2

def listen_command(ltl=ltl):
    try:
        with speech_recognition.Microphone() as mic:
            sr.adjust_for_ambient_noise(source=mic, duration=0.5)
            audio = sr.listen(source=mic, phrase_time_limit=ltl)
            query = sr.recognize_google(audio_data=audio, language='ru-RU').lower()
            print(query)
            return query
    except speech_recognition.UnknownValueError:
        print("Извините, я вас не расслышал")

def greeting(query):
    print('Добрейшего')

def weather(query):
    for step in track(range(100), description="Идет поиск"):
        sleep(random.uniform(0.01,0.1))
    place = requests.get('https://ipinfo.io')
    data = place.json()
    city = data['city']
    weatherI = pyowm.OWM('0506e9f2e8b4b327f011bece65e67552')
    weather_Manager = weatherI.weather_manager()
    weatherAtPlace = weather_Manager.weather_at_place(city)
    weather_now = weatherAtPlace.weather
    temp = weather_now.temperature('celsius')['temp']
    wind = weather_now.wind()['speed']
    detail = weather_now.detailed_status
    print(f'Температура: {temp}°C\n'
          f'Скорость ветра: {wind} м/с\n'
          f'На улице {detail}')

def search_information(query):
    first_exp = True
    try:
        print("Что вы хотите найти?")
        ls_cmd = listen_command(ltl=ltl)
        translator = Translator()
        translation = translator.translate(ls_cmd, src='ru', dest='en')
        wiki = wikipedia.page(f'{translation.text}')
        wiki_page = wiki.content
        wiki_page = wiki_page[0:wiki_page.find("=")]
        wiki_text = translator.translate(text=str(wiki_page), dest='ru').text
        print(wiki_text)
    except Exception as ex:
        if first_exp == True and ls_cmd!=None:
            webbrowser.open(f"http://www.google.com/search?q={ls_cmd}")
            first_exp = False


def enter_programm(query):
    file_path = str(input("Введите ниже путь к файлу:\n"))
    print("Произнесите название программы")
    file_name = listen_command()
    programms = open('programms.txt','a')
    programms.write(f'{file_name}\n{file_path}\n')


def open_programm(query):
    print("Скажите название программы")
    programm = listen_command()
    with open("programms.txt") as file:
        programms = file.readlines()
        programms_witout_n = []
        for p in programms:
            programms_witout_n.append(p.replace('\n', ''))
        file_path = programms_witout_n[programms_witout_n.index(programm) + 1]
    if file_path!= '':
        os.startfile(file_path)
    else:
        print("Такого файла нет!")

def del_programm(query):
    print("Скажите название программы")
    programm = listen_command()
    with open("programms.txt") as file:
        programms = file.readlines()
        programms_witout_n = []
        for p in programms:
            programms_witout_n.append(p.replace('\n', ''))
        file_path = programms_witout_n[programms_witout_n.index(programm) + 1]
    if file_path != '':
        os.startfile(file_path)
    else:
        print("Такого файла нет!")

def show_programm(query):
    file = open(r"programms.txt",'r')
    print(file.read())

def enter_site(query):
    website_url = str(input("Введите адрес сайта:\n"))
    print("Произнесите название сайта")
    website_name = listen_command()
    websites = open('websites.txt', 'a')
    websites.write(f'{website_name}\n{website_url}\n')

def open_site(query):
    print("Произнесите название сайта")
    web_site = listen_command()
    wb = False
    web_site_url = ''
    with open("websites.txt") as file:
        web_sites = file.readlines()
        web_sites_witout_n = []
        for w in web_sites:
            web_sites_witout_n.append(w.replace('\n',''))
        web_site_url = web_sites_witout_n[web_sites_witout_n.index(web_site)+1]
    print(web_site_url)
    webbrowser.open(web_site_url)

def show_websites(query):
    file = open(r"websites.txt", 'r')
    print(file.read())

def open_something(query):
    def norm(word):
        morph = pymorphy2.MorphAnalyzer()
        p = morph.parse(word)[0]
        return p.normal_form
    if 'открой' in query:
        query = query.replace('открой ','')
        query = norm(query)
    elif 'открыть' in query:
        query = query.replace('открыть ','')
        query = norm(query)
    with open("websites.txt") as file:
        web_sites = file.readlines()
        web_sites_witout_n = []
        for w in web_sites:
            web_sites_witout_n.append(w.replace('\n',''))
        if query in web_sites_witout_n:
            web_site_url = web_sites_witout_n[web_sites_witout_n.index(query)+1]
            webbrowser.open(web_site_url)
    with open("programms.txt") as file:
        programms = file.readlines()
        programms_witout_n = []
        file_path = ''
        for p in programms:
            programms_witout_n.append(p.replace('\n', ''))
        if query in programms_witout_n:
            file_path = programms_witout_n[programms_witout_n.index(query) + 1]
            os.startfile(file_path)

def translate(query):
    languages = {'en':'английский',
                 'fr':'французкий',
                 'ru':'русский',
                 'it':'итальянский'}

def random_image(query):
    chars = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890_'
    image_name = ''
    for i in range(random.randint(5,20)):
        image_name+=random.choice(chars)
    headers = {'User-Agent':fake_useragent.UserAgent().random}
    link = 'https://avavatar.ru/images/random'
    response = requests.get(link, headers=headers).text
    soup = BeautifulSoup(response, 'lxml')
    block = soup.find('div',class_='image_preview_box')
    print(block)
    image_link = block.find('a').get('href')
    print(image_link)
    download_storage = requests.get(image_link, headers=headers).text
    soup = BeautifulSoup(download_storage, 'lxml')
    result_link = 'https://avavatar.ru'
    download_block = soup.find('div','image_block').find('img').get('src')
    result_link = result_link + download_block
    image_bytes = requests.get(result_link).content
    with open(f'images/{image_name}.jpg','wb') as file:
        file.write(image_bytes)
        print('Изображение скачано!')

while True:
    l_commands = listen_command()
    solved = False
    if l_commands == None:
        l_commands = ''
    for w in word_activator:
        if w in l_commands:
            l_commands = l_commands[len(w)+1:]
            for key, val in commands_dict['commands'].items():
                for v in val:
                    if v in l_commands and solved != True:
                        (globals()[key](l_commands))
                        solved == True