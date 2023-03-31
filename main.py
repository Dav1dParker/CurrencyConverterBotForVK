import vk_api
from vk_api import utils
from vk_api.longpoll import VkLongPoll, VkEventType
import requests
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import json
import urllib.request
import xml.dom.minidom
import datetime


def converter_start():
    link = "https://www.cbr.ru/scripts/XML_daily.asp?date_req=" + datetime.datetime.now().strftime(
        '%d/%m/%Y')  # Ссылка на сегодняшние котировки
    response = urllib.request.urlopen(link)
    currency_nominals = ["1.0"]  # Список с номиналами валют
    currency_value = ["1.0"]  # Список с курсом валют
    dom = xml.dom.minidom.parse(response)  # Получение DOM структуры файла #Знать бы что такое DOM
    dom.normalize()
    node_array = dom.getElementsByTagName("Valute")  # Получение элементов с тегом
    for node in node_array:
        child_list = node.childNodes  # Получение дочерних элементов
        for child in child_list:
            if child.nodeName == "Nominal":
                currency_nominals.append(child.childNodes[0].nodeValue)
            if child.nodeName == "Value":
                currency_value.append(child.childNodes[0].nodeValue)
    for i in range(len(currency_value)):  # , -> .
        currency_value[i] = currency_value[i].replace(',', '.')
    return currency_nominals, currency_value


def write_msg(user_id, message):
    random_id = vk_api.utils.get_random_id()
    vk.method('messages.send', {'user_id': user_id, 'message': message, "random_id": random_id})


# API-ключ созданный ранее
tokenName = open('token.txt', 'r')
token = tokenName.read()
tokenName.close()

# Авторизуемся как сообщество
vk = vk_api.VkApi(token=token)
vk_plus = vk.get_api()
# Работа с сообщениями
longpoll = VkLongPoll(vk)


def main_menu():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Конвертер валют', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button('Погода', color=VkKeyboardColor.SECONDARY)
    vk_plus.messages.send(user_id=event.user_id, random_id=vk_api.utils.get_random_id(),
                          keyboard=keyboard.get_keyboard(), message='Выберите функцию')


def cur_calculation(entered_val, first_currency_index, second_currency_index, currency_nominals, currency_value):
    return round((((entered_val * float(currency_value[first_currency_index]) / float(
        currency_nominals[first_currency_index]))) / (float(currency_value[second_currency_index]) / float(
        currency_nominals[second_currency_index]))), 2)  # Возврат результата


def moscow():
    global main_weather, description_weather, wind_type
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
                 'extreme rain': "чрезвычайно сильный дождь",
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
    json_weather = json.loads(weather.content)
    for i in json_weather["weather"]:
        main_weather = (i["main"])
        main_weather = (translate[main_weather])
        description_weather = (i["description"])
        description_weather = (translate[description_weather])
    temp_min = json_weather["main"]["temp_min"]
    temp_max = json_weather["main"]["temp_max"]
    pressure = json_weather["main"]["pressure"]
    aqua = json_weather["main"]["humidity"]
    speed = json_weather["wind"]["speed"]
    deg = json_weather["wind"]["deg"]
    wind_directions = (
        "северный", "северо-восточный", "восточный", "юго-восточный", "южный", "юго-западный", "западный",
        "северо-западный")
    direction = int((deg + 22.5) // 45 % 8)
    dir = str(wind_directions[direction])
    wind_type = ""
    if float(speed) <= 0.2:
        wind_type = "Штиль"
    if 0.3 <= float(speed) <= 1.5:
        wind_type = "Тихий"
    if 1.6 <= float(speed) <= 3.3:
        wind_type = "Лёгкий"
    if 3.4 <= float(speed) <= 5.4:
        wind_type = "Слабый"
    if 5.5 <= float(speed) <= 7.9:
        wind_type = "Умеренный"
    if 8 <= float(speed) <= 10.7:
        wind_type = "Свежий"
    if 10.8 <= float(speed) <= 13.8:
        wind_type = "Сильный"
    if 13.9 <= float(speed) <= 17.1:
        wind_type = "Крепкий"
    if 17.2 <= float(speed) <= 20.7:
        wind_type = "Очень крепкий"
    if 20.8 <= float(speed) <= 24.4:
        wind_type = "Шторм"
    if 24.5 <= float(speed) <= 28.4:
        wind_type = "Сильный шторм"
    if 28.5 <= float(speed) <= 32.6:
        wind_type = "Жестокий шторм"
    if float(speed) >= 33:
        wind_type = "Ураган"
    forecast = ("Погода в Москве: " + main_weather + "\n" + " Температура " + str(
        int(temp_min)) + "-" + str(
        int(temp_max)) + "°C\n" + "Давление: " + str(int(float(pressure) * 0.750064)) + "мм рт.ст. Влажность: " + str(
        aqua) + "%\n" + "Ветер: " + wind_type + ", " + str(speed) + "м/с, " + dir)
    write_msg(event.user_id, forecast)


# Основной цикл
input_flag = 0
entered_val = 1
first_currency_index = 14
second_currency_index = 0
currency_names_nominative_case = [
    'Российский рубль', 'Австралийский доллар', 'Азербайджанский манат', 'Фунт стерлингов соединенного королевства',
    'Армянский драм', 'Белорусский рубль', 'Болгарский лев', 'Бразильский реал', 'Венгерский форинт',
    'Вьетнамский донг', 'Гонконгский доллар', 'Грузинский лари', 'Датская крона', 'Дирхам ОАЭ', 'Доллар США', 'Евро',
    'Египетский фунт', 'Индийская рупия', 'Индонезийская рупия', 'Казахстанский тенге', 'Канадский доллар',
    'Катарский риал', 'Киргизский сом', 'Китайский юань', 'Молдавский лей', 'Новозеландский доллар',
    'Норвежская крона', 'Польский злотый', 'Румынский лей', 'сдр (специальные права заимствования)',
    'Сингапурский доллар', 'Таджикский сомони', 'Тайский бат', 'Турецкая лира', 'Новый туркменский манат',
    'Узбекский сум', 'Украинская гривна', 'Чешская крона', 'Шведская крона', 'Швейцарский франк', 'Сербский динар',
    'Южноафриканский рэнд', 'Южнокорейская вона', 'Японская йена']

currency_names_genitive_case = ['Российских рублей', 'Австралийских долларов', 'Азербайджанских манат',
                                'Фунтов стерлингов', 'Армянских драмов', 'Белорусских рублей', 'Болгарский львов',
                                'Бразильских реалов', 'Венгерских форинтов', 'Вьетнамских донгов',
                                'Гонконгских долларов', 'Грузинских ларей', 'Датских крон', 'Дирхам ОАЭ',
                                'Долларов США', 'Евро', 'Египетских фунтов', 'Индийских рупий', 'Индонезийских рупий',
                                'Казахстанских тенге', 'Канадских долларов', 'Катарских риалов', 'киргизских сомов',
                                'Китайских юаней', 'Молдавских леев', 'Новозеландских долларов', 'Норвежских крон',
                                'Польских злотых', 'Румынских лей', 'сдр (специальные права заимствования)',
                                'Сингапурских долларов', 'Таджикских сомони', 'Таиландских батов', 'Турецких лир',
                                'Новых туркменских манат', 'Узбекских кумов', 'Украинских гривен', 'Чешских крон',
                                'Шведских крон', 'Швейцарских франков', 'Сербских динаров', 'Южноафриканских рэндов',
                                'Вон республики Корея', 'Японских иен']
lower_currency_names_nominative_case = [item.lower() for item in currency_names_nominative_case]
currency_nominals = ["Если вы это видите, то что-то пошло не так"]
currency_value = ["Если вы это видите, то что-то пошло не так"]
keyboard = VkKeyboard(one_time=True)
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
            if input_flag == 1:
                input_flag = 0
                try:
                    print(lower_currency_names_nominative_case.index(request))
                    first_currency_index = lower_currency_names_nominative_case.index(request)
                except ValueError:
                    vk_plus.messages.send(user_id=event.user_id, random_id=vk_api.utils.get_random_id(),
                                          keyboard=keyboard.get_keyboard(),
                                          message="Такой валюты нет. Пожалуйста, введите название валюты точно, "
                                                  "как написано в предложенном списке")
                    continue
                vk_plus.messages.send(user_id=event.user_id, random_id=vk_api.utils.get_random_id(),
                                      keyboard=keyboard.get_keyboard(),
                                      message="Вы выбрали " + currency_names_nominative_case[first_currency_index])
                continue
            elif input_flag == 2:
                input_flag = 0
                try:
                    print(lower_currency_names_nominative_case.index(request))
                    second_currency_index = lower_currency_names_nominative_case.index(request)
                except ValueError:
                    vk_plus.messages.send(user_id=event.user_id, random_id=vk_api.utils.get_random_id(),
                                          keyboard=keyboard.get_keyboard(),
                                          message="Такой валюты нет. Пожалуйста, введите название валюты точно, "
                                                  "как написано в предложенном списке")
                    continue
                vk_plus.messages.send(user_id=event.user_id, random_id=vk_api.utils.get_random_id(),
                                      keyboard=keyboard.get_keyboard(),
                                      message="Вы выбрали " + currency_names_nominative_case[second_currency_index])
                continue
            elif input_flag == 3:
                input_flag = 0
                try:
                    entered_val = float(request)
                except ValueError:
                    vk_plus.messages.send(user_id=event.user_id, random_id=vk_api.utils.get_random_id(),
                                          keyboard=keyboard.get_keyboard(), message="неверный формат\n Введите сумму в "
                                                                                    "виде 123.321")
                    continue
                vk_plus.messages.send(user_id=event.user_id, random_id=vk_api.utils.get_random_id(),
                                      keyboard=keyboard.get_keyboard(), message="Вы ввели " + str(entered_val))
                continue
            if request == "начать":
                write_msg(event.user_id,
                          "Здравствуйте, я бот для конвертации валют. Вы можете производить взаимодействие с помощью "
                          "команды 'бот'")
                continue
            if request == "привет":
                write_msg(event.user_id, 'Привет, ' + vk_plus.users.get(user_id=event.user_id)[0]['first_name'])
                continue
            elif request == "пока":
                write_msg(event.user_id, "Пока")
                continue
            elif request == "бот":
                main_menu()
                continue
            elif request == "конвертер валют" or request == "1":
                currency_nominals, currency_value = converter_start()
                cur_list = "Вот валюты с которыми я могу работать: \n"
                for i in currency_names_nominative_case:
                    cur_list += i + "\n"
                cur_list += "По умолчанию перевожу USD в RUB\n"
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button('Выбрать исходную валюту', color=VkKeyboardColor.SECONDARY)
                keyboard.add_button('Выбрать целевую валюту', color=VkKeyboardColor.SECONDARY)
                keyboard.add_line()
                keyboard.add_button('Ввести сумму', color=VkKeyboardColor.PRIMARY)
                keyboard.add_button('перевести', color=VkKeyboardColor.NEGATIVE)
                vk_plus.messages.send(user_id=event.user_id, random_id=vk_api.utils.get_random_id(),
                                      keyboard=keyboard.get_keyboard(), message=cur_list)
                continue
            elif request == "выбрать исходную валюту":
                write_msg(event.user_id, "Введите полное название исходной валюты")
                input_flag = 1
                continue
            elif request == "выбрать целевую валюту":
                write_msg(event.user_id, "Введите полное название целевой валюты")
                input_flag = 2
                continue
            elif request == "ввести сумму":
                write_msg(event.user_id, "Введите количество исходной валюты")
                input_flag = 3
                continue
            elif request == "перевести":
                # Для тестирования:
                # ————————————————————————————
                # entered_val = 100
                # name1 = "Доллар США"
                # name2 = "Российский рубль"
                # ————————————————————————————
                try:
                    answer = cur_calculation(entered_val, first_currency_index, second_currency_index,
                                             currency_nominals, currency_value)
                    if entered_val == 1:
                        name1 = currency_names_nominative_case[first_currency_index]
                    else:
                        name1 = currency_names_genitive_case[first_currency_index]
                    if answer == 1:
                        name2 = currency_names_nominative_case[second_currency_index]
                    else:
                        name2 = currency_names_genitive_case[second_currency_index]
                    write_msg(event.user_id,
                              str(entered_val) + " " + name1 + " = " + str(answer) + " " + name2)
                except:
                    write_msg(event.user_id, "Что-то пошло не так")
                continue
            elif request == "погода" or request == "2":
                moscow()
                continue
            elif request == "/help" or request == "help" or request == "справка" or request == "помощь":
                write_msg(event.user_id, "я бот для конвертации валют.\n Для входа в главного меню используйте "
                                         "команду 'бот'\nДля быстрого доступа к конвертору валют введите команду "
                                         "'конвертер валют' или отправьте цифру 1\nДля быстрого просмотра прогноза "
                                         "погоды введите команду "
                                         "'погода' или отправьте цифру 2")
                continue
            else:
                write_msg(event.user_id, "Неизвестная команда\n Вы можете посмотреть справку по командам с помощью "
                                         "/help")
