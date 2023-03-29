import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import requests
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import json
import urllib.request
import xml.dom.minidom


def converterStart():
    link = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + nowp(0)  # Ссылка на сегодняшние котировки
    response = urllib.request.urlopen(link)
    ValName = ["Российский рубль"]  # Список с названиями валют
    ValNom = ["1.0"]  # Список с номиналами валют
    ValValue = ["1.0"]  # Список с курсом валют
    dom = xml.dom.minidom.parse(response)  # Получение DOM структуры файла #Знать бы что такое DOM
    dom.normalize()
    nodeArray = dom.getElementsByTagName("Valute")  # Получение элементов с тегом
    for node in nodeArray:
        childList = node.childNodes  # Получение дочерних элементов
        for child in childList:
            if (child.nodeName == "Name"):
                ValName.append(child.childNodes[
                                   0].nodeValue)  # Добавление информации в списки ВАЖНО: Списки ассоциируются между друг другом только по индексу. Нельзя менять порядок только в одном списке, только во всех одновременно!
            if (child.nodeName == "Nominal"):
                ValNom.append(child.childNodes[0].nodeValue)
            if (child.nodeName == "Value"):
                ValValue.append(child.childNodes[0].nodeValue)
    for i in range(len(ValValue)):  # , -> .
        ValValue[i] = ValValue[i].replace(',', '.')
    for i in range(len(ValName)):
        ValName[i] = ValName[i].lower()
    return ValName, ValNom, ValValue


def write_msg(user_id, message):
    random_id = vk_api.utils.get_random_id()
    vk.method('messages.send', {'user_id': user_id, 'message': message, "random_id": random_id})


# API-ключ созданный ранее
tokenName = open('token.txt', 'r')
token = tokenName.read()
tokenName.close()

# Авторизуемся как сообщество
vk = vk_api.VkApi(token=token)
vkplus = vk.get_api()
# Работа с сообщениями
longpoll = VkLongPoll(vk)


def mainmenu():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Конвертер валют', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button('Погода', color=VkKeyboardColor.SECONDARY)
    vkplus.messages.send(user_id=event.user_id, random_id=vk_api.utils.get_random_id(),
                         keyboard=keyboard.get_keyboard(), message='Выберите функцию')


def cur_calculation(entered_val, name1, name2, ValName, ValNom, ValValue):
    valute1 = 0.0  # Переменная в которой хранится курс первой валюты к рублю
    valute2 = 0.0  # Переменная в которой хранится курс второй валюты к рублю
    for i in range(len(ValName)):
        if name1 == ValName[i]:  # Ищем совпадение названия выбранной валюты и перебираемых названий валют
            valute1 = float(ValValue[i]) / float(
                ValNom[i])  # Нашли название, значит по тому-же индексу и курс, запоминаем его.
            break

    for i in range(len(ValName)):  # Тоже самое для второй валюты
        if name2 == ValName[i]:
            valute2 = float(ValValue[i]) / float(ValNom[i])
            break
    return (entered_val * valute1) / valute2  # Возврат результата


def moscow():
    translate = {'Thunderstorm': "Гроза", 'Drizzle': "Моросит", 'Rain': "Дождь", 'Snow': "Снег", 'Mist': "Туман",
                 'Smoke': "Дым", 'Haze': "Легкий туман", 'Dust': "Пыль", 'Fog': "Туман", 'Sand': "Моросит",
                 'Песок': "Clear", 'Ясно': "Моросит", 'Clouds': "Облачно", 'Tornado': "торнадо", 'Squall': "Шквал",
                 'Ash': "Пепел",
                 'clear sky': "чистое небо", 'few clouds': "несколько облаков", 'scattered clouds': "рассеянные облака",
                 'overcast clouds': "ААА", 'broken clouds': "разорванные облака", 'shower rain': "ливень",
                 'rain': "дождь", 'thunderstorm': "гроза", 'snow': "снег", 'mist': "туман",
                 'thunderstorm with light rain': "гроза с небольшим дождем", 'thunderstorm with rain': "гроза с дождем",
                 'thunderstorm with heavy rain': "гроза с ливнем", 'light thunderstorm': "небольшая гроза",
                 'heavy thunderstorm': "сильная гроза", 'ragged thunderstorm': "ураган",
                 'thunderstorm with light drizzle': "гроза с небольшим туманом",
                 'thunderstorm with drizzle': "гроза с туманом",
                 'thunderstorm with heavy drizzle': "гроза с сильным туманом",
                 'light intensity drizzle': "незначительный туман", 'heavy intensity drizzle': "интенсивный туман",
                 'light intensity drizzle rain': "легкий дождь с туманом", 'drizzle rain': "дождь с туманом",
                 'heavy intensity drizzle rain': "сильный туман с дождём", 'shower rain and drizzle': "туман и ливень",
                 'heavy shower rain and drizzle': "сильный туман и ливень", 'shower drizzle': "туман с ураганом",
                 'light rain': "небольшой дождь", 'moderate rain': "умеренный дождь",
                 'heavy intensity rain': "сильный дождь", 'very heavy rain': "очень сильный дождь",
                 'extreme rain': "черезвычайно сильный дождь",
                 'freezing rain': "ледяной дождь", 'light intensity shower rain': "небольшой ледяной дождь",
                 'heavy intensity shower rain': "сильный ливень", 'ragged shower rain': "ледянной ливень",
                 'light snow': "легкий снег", 'Heavy snow': "сильный снег", 'Sleet': "Слякоть",
                 'Light shower sleet': "Легкий дождь с мокрым снегом", 'Shower sleet': "Ливень с мокрым снегом",
                 'Light rain and snow': "легкий дождь со снегом", 'Rain and snow': "дождь со снегом",
                 'Light shower snow': "Легкий снежный дождь", 'Shower snow': "Ливень снега",
                 'Heavy shower snow': "Сильный ливень со снегом", 'sand/ dust whirls': "вихри песка/ пыли",
                 'volcanic ash': "Вулканический пепел",
                 'few clouds: 11-25%': "мало облаков: 11-25%", 'scattered clouds: 25-50%': "рассеянные облака: 25-50%",
                 'broken clouds: 51-84%': "разорванные облака: 51-84%",
                 'overcast clouds: 85-100%': "Облачность: 85-100%"}
    weather = requests.get(
        "https://api.openweathermap.org/data/2.5/weather?q=moscow&appid=bc6fb75f3340b3fbb4417fd96406e0f1&units=metric")
    jweather = json.loads(weather.content)
    for i in jweather["weather"]:
        mainW = (i["main"])
        mainW = (translate[mainW])
        descriptionW = (i["description"])
        descriptionW = (translate[descriptionW])
    temp_min = jweather["main"]["temp_min"]
    temp_max = jweather["main"]["temp_max"]
    pressure = jweather["main"]["pressure"]
    aqua = jweather["main"]["humidity"]
    speed = jweather["wind"]["speed"]
    deg = jweather["wind"]["deg"]
    winddirections = ("северный", "северо-восточный", "восточный", "юго-восточный", "южный", "юго-западный", "западный",
                      "северо-западный")
    direction = int((deg + 22.5) // 45 % 8)
    dir = str(winddirections[direction])
    if float(speed) <= 0.2:
        windtype = "Штиль"
    if 0.3 <= float(speed) <= 1.5:
        windtype = "Тихий"
    if 1.6 <= float(speed) <= 3.3:
        windtype = "Лёгкий"
    if 3.4 <= float(speed) <= 5.4:
        windtype = "Слабый"
    if 5.5 <= float(speed) <= 7.9:
        windtype = "Умеренный"
    if 8 <= float(speed) <= 10.7:
        windtype = "Свежий"
    if 10.8 <= float(speed) <= 13.8:
        windtype = "Сильный"
    if 13.9 <= float(speed) <= 17.1:
        windtype = "Крепкий"
    if 17.2 <= float(speed) <= 20.7:
        windtype = "Очень крепкий"
    if 20.8 <= float(speed) <= 24.4:
        windtype = "Шторм"
    if 24.5 <= float(speed) <= 28.4:
        windtype = "Сильный шторм"
    if 28.5 <= float(speed) <= 32.6:
        windtype = "Жестокий шторм"
    if float(speed) >= 33:
        windtype = "Ураган"
    forecat = ("Погода в Москве: " + mainW + "\n" + descriptionW + " Температура " + str(int(temp_min)) + "-" + str(
        int(temp_max)) + "°C\n" + "Давление: " + str(int(float(pressure) * 0.750064)) + "мм рт.ст. Влажность: " + str(
        aqua) + "%\n" + "Ветер: " + windtype + ", " + str(speed) + "м/с, " + dir)
    write_msg(event.user_id, forecat)


# Основной цикл
inputFlag = 0
for event in longpoll.listen():

    # Если пришло новое сообщение
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.to_me:

        # Если оно имеет метку для меня(то есть бота)
        if event.to_me:
            print('New from {}, text = {}'.format(event.user_id, event.text))
            # Сообщение от пользователя
            request = event.text
            request = request.lower()
            # Каменная логика ответа
            if inputFlag == 1:
                inputFlag = 0
                name1 = request
                vkplus.messages.send(user_id=event.user_id, random_id=vk_api.utils.get_random_id(),
                                     keyboard=keyboard.get_keyboard(), message="Вы выбрали " + name1)
                continue
            elif inputFlag == 2:
                inputFlag = 0
                name2 = request
                vkplus.messages.send(user_id=event.user_id, random_id=vk_api.utils.get_random_id(),
                                     keyboard=keyboard.get_keyboard(), message="Вы выбрали " + name2)
                continue
            elif inputFlag == 3:
                inputFlag = 0
                try:
                    entered_val = float(request)
                except TypeError:
                    write_msg(event.user_id, "Неверный формат")
                    continue
                vkplus.messages.send(user_id=event.user_id, random_id=vk_api.utils.get_random_id(),
                                     keyboard=keyboard.get_keyboard(), message="Вы ввели " + str(entered_val))
                continue
            if request == "начать":
                write_msg(event.user_id,
                          "Здравствуйте, я бот для конвертации валют. Вы можете производить взаимодействие с помощью команды 'бот'\n Также я могу показать погоду в Москве по команде'погода'")
                continue
            if request == "привет":
                write_msg(event.user_id, 'Привет, ' + vkplus.users.get(user_id=event.user_id)[0]['first_name'])
                continue
            elif request == "пока":
                write_msg(event.user_id, "Пока")
                continue
            elif request == "бот":
                mainmenu()
                continue
            elif request == "конвертер валют":
                ValName, ValNom, ValValue = converterStart()
                cur_list = "Вот валюты с которыми я могу работать: \n"
                for i in ValName:
                    cur_list += i + "\n"
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button('Выбрать исходную валюту', color=VkKeyboardColor.SECONDARY)
                keyboard.add_button('Выбрать целевую валюту', color=VkKeyboardColor.SECONDARY)
                keyboard.add_line()
                keyboard.add_button('Ввести сумму', color=VkKeyboardColor.PRIMARY)
                keyboard.add_button('перевести', color=VkKeyboardColor.NEGATIVE)
                vkplus.messages.send(user_id=event.user_id, random_id=vk_api.utils.get_random_id(),
                                     keyboard=keyboard.get_keyboard(), message=cur_list)
                continue
            elif request == "выбрать исходную валюту":
                write_msg(event.user_id, "Введите полное название исходной валюты")
                inputFlag = 1
                continue
            elif request == "выбрать целевую валюту":
                write_msg(event.user_id, "Введите полное название целевой валюты")
                inputFlag = 2
                continue
            elif request == "ввести сумму":
                write_msg(event.user_id, "Введите количество исходной валюты")
                inputFlag = 3
                continue
            elif request == "перевести":
                # Для тестирования:
                # ————————————————————————————
                # entered_val = 100
                # name1 = "Доллар США"
                # name2 = "Российский рубль"
                # ————————————————————————————
                answer = cur_calculation(entered_val, name1, name2, ValName, ValNom, ValValue)
                write_msg(event.user_id, str(entered_val) + " " + name1 + " = " + str(answer) + " " + name2)
                continue
            elif request == "погода":
                moscow()
                continue
            else:
                write_msg(event.user_id, "Неизвестная команда")
