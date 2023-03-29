import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import requests
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import json
import urllib.request
import xml.dom.minidom
import datetime


# Возвращает текущее время
def nowp(a):  # Аргументы: 0 - Дата/Месяц/Год; 1 - Дата; 2 - Месяц; 3 - Год
    current_date = datetime.datetime.now()
    if a == 0:
        return current_date.strftime('%d/%m/%Y')
    if a == 1:
        return current_date.strftime('%d')
    if a == 2:
        return current_date.strftime('%m')
    if a == 3:
        return current_date.strftime('%Y')


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
            # print(child.nodeName)
            # print(child.childNodes[0].nodeValue) #Получение значения
    for i in range(len(ValValue)):  # , -> .
        ValValue[i] = ValValue[i].replace(',', '.')
    return ValName, ValNom, ValValue


def write_msg(user_id, message):
    random_id = vk_api.utils.get_random_id()
    vk.method('messages.send', {'user_id': user_id, 'message': message, "random_id": random_id})


# API-ключ созданный ранее
token = "vk1.a.HvAMs19yEDZK28npckGJhtF_6J2LEb3j9UgNAlx1Xom4xt9Xv_ibLBPFcjj1fpDj9wSP6i_ln2MqQYSwDpP-RzXSpvD1SPSx9f7BARSkoqdNS0cYWinoxbJ6lOVZwOxR0a6qx1AEdZXRitM24upM6paIPfqd5Y5lQQc1c9M_uMdTXI6AEnAOlzRwHrUrYOhuoUOM74VhUB33paAFPjy_yA"

# Авторизуемся как сообщество
vk = vk_api.VkApi(token=token)
vkplus = vk.get_api()
# Работа с сообщениями
longpoll = VkLongPoll(vk)
week = datetime.datetime.today() - datetime.datetime(2022, 2, 9)
week = int(week.days / 7 + 1)


def mainmenu():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Конвертер валют', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button('Погода', color=VkKeyboardColor.SECONDARY)
    """
    keyboard.add_button('На завтра', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()  # переход на вторую строку
    keyboard.add_button('на эту неделю', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('на следующую неделю', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()  # переход на вторую строку
    keyboard.add_button('какая неделя?', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button('какая группа?', color=VkKeyboardColor.SECONDARY)
    """
    vkplus.messages.send(user_id=event.user_id, random_id=vk_api.utils.get_random_id(),
                         keyboard=keyboard.get_keyboard(), message='Выберите валюту')


def converterMenu(ValName):
    keyboard = VkKeyboard(one_time=True)
    for i in range(10):
        print(ValName[i])
        keyboard.add_button(ValName[i], color=VkKeyboardColor.SECONDARY)
        if i != 9:
            keyboard.add_line()

    vkplus.messages.send(user_id=event.user_id, random_id=vk_api.utils.get_random_id(),
                         keyboard=keyboard.get_keyboard(), message='Выберите валюту')


def cur_calculation(entered_val, name1, name2, ValName, ValNom, ValValue):
    res = 0.0
    valute1 = 0.0  # Переменная в которой хранится курс первой валюты к рублю
    valute2 = 0.0  # Переменная в которой хранится курс второй валюты к рублю
    for i in range(len(ValName)):
        if name1 == ValName[i]:  # Ищем совпадение названия выбранной валюты и перебираемых названий валют
            valute1 = float(ValValue[i]) / float(ValNom[i])  # Нашли название, значит по тому-же индексу и курс, запоминаем его.
            break

    for i in range(len(ValName)):  # Тоже самое для второй валюты
        if name2 == ValName[i]:
            valute2 = float(ValValue[i]) / float(ValNom[i])
            break

    res = (entered_val * valute1) / valute2  # Вычисление соотношения курсов валют (Ответа)
    return res  # Вывод результата


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
        "http://api.openweathermap.org/data/2.5/weather?q=moscow&appid=bc6fb75f3340b3fbb4417fd96406e0f1&units=metric")
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
    if float(speed) >= 0.3 and float(speed) <= 1.5:
        windtype = "Тихий"
    if float(speed) >= 1.6 and float(speed) <= 3.3:
        windtype = "Лёгкий"
    if float(speed) >= 3.4 and float(speed) <= 5.4:
        windtype = "Слабый"
    if float(speed) >= 5.5 and float(speed) <= 7.9:
        windtype = "Умеренный"
    if float(speed) >= 8 and float(speed) <= 10.7:
        windtype = "Свежий"
    if float(speed) >= 10.8 and float(speed) <= 13.8:
        windtype = "Сильный"
    if float(speed) >= 13.9 and float(speed) <= 17.1:
        windtype = "Крепкий"
    if float(speed) >= 17.2 and float(speed) <= 20.7:
        windtype = "Очень крепкий"
    if float(speed) >= 20.8 and float(speed) <= 24.4:
        windtype = "Шторм"
    if float(speed) >= 24.5 and float(speed) <= 28.4:
        windtype = "Сильный шторм"
    if float(speed) >= 28.5 and float(speed) <= 32.6:
        windtype = "Жестокий шторм"
    if float(speed) >= 33:
        windtype = "Ураган"
    forecat = ("Погода в Москве: " + mainW + "\n" + descriptionW + " Температура " + str(int(temp_min)) + "-" + str(
        int(temp_max)) + "°C\n" + "Давление: " + str(int(float(pressure) * 0.750064)) + "мм рт.ст. Влажность: " + str(
        aqua) + "%\n" + "Ветер: " + windtype + ", " + str(speed) + "м/с, " + dir)
    """
    print("Погода в Москве: " + mainW)
    print(descriptionW + " Температура " + str(int(temp_min)) + "-" + str(int(temp_max)) + "°C")
    print("Давление: " + str(int(float(pressure) * 0.750064)) + "мм рт.ст. Влажность: " + str(aqua) + "%")
    print("Ветер: " + windtype +)
    """
    write_msg(event.user_id, forecat)


# Основной цикл
for event in longpoll.listen():

    # Если пришло новое сообщение
    if event.type == VkEventType.MESSAGE_NEW:

        # Если оно имеет метку для меня(то есть бота)
        if event.to_me:
            print('New from {}, text = {}'.format(event.user_id, event.text))
            # Сообщение от пользователя
            request = event.text
            request = request.lower()
            # Каменная логика ответа
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
                converterMenu(ValName)
                continue
            elif request == "перевести":
                #Для тестирования:
                # ————————————————————————————
                entered_val = 10
                name1 = "Австралийский доллар"
                name2 = "Российский рубль"
                #————————————————————————————

                answer = cur_calculation(entered_val, name1, name2, ValName, ValNom, ValValue)
                write_msg(event.user_id, str(entered_val) + " " + name1 + " = " + str(answer) + " " + name2)
            elif request == "погода":
                moscow()
                continue
            else:
                write_msg(event.user_id, "Неизвестная команда")
