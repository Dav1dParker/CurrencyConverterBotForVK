import vk_api
from vk_api import utils
from vk_api.longpoll import VkLongPoll, VkEventType
import requests
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import json
import urllib.request
import xml.dom.minidom
import datetime
from translate import translation_dict


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
    currency_value = [w.replace(',', '.') for w in currency_value]  # , -> .
    return currency_nominals, currency_value


def write_msg(user_id, message):
    random_id = vk_api.utils.get_random_id()
    vk.method('messages.send', {'user_id': user_id, 'message': message, "random_id": random_id})


# API-ключ созданный ранее
token_name = open('token.txt', 'r')
token = token_name.read()
token_name.close()

# Авторизуемся как сообщество
vk = vk_api.VkApi(token=token)
vk_plus = vk.get_api()
# Работа с сообщениями
longpoll = VkLongPoll(vk)


def main_menu():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Конвертер валют', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Погода', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Справка', color=VkKeyboardColor.SECONDARY)
    vk_plus.messages.send(user_id=event.user_id, random_id=vk_api.utils.get_random_id(),
                          keyboard=keyboard.get_keyboard(), message='Выберите функцию')


def cur_calculation(entered_val, first_currency_index, second_currency_index, currency_nominals, currency_value):
    return round((((entered_val * float(currency_value[first_currency_index]) / float(
        currency_nominals[first_currency_index]))) / (float(currency_value[second_currency_index]) / float(
        currency_nominals[second_currency_index]))), 2)  # Возврат результата


def moscow():
    main_weather = "None"
    description_weather = "None"
    weather = requests.get(
        "https://api.openweathermap.org/data/2.5/weather?q=moscow&appid=bc6fb75f3340b3fbb4417fd96406e0f1&units=metric")
    json_weather = json.loads(weather.content)
    for i in json_weather["weather"]:
        main_weather = (translation_dict[i["main"]])
        description_weather = (translation_dict[i["description"]])
    temp_min = json_weather["main"]["temp_min"]
    temp_max = json_weather["main"]["temp_max"]
    pressure = json_weather["main"]["pressure"]
    aqua = json_weather["main"]["humidity"]
    speed = json_weather["wind"]["speed"]
    deg = json_weather["wind"]["deg"]
    wind_directions = (
        "северный", "северо-восточный", "восточный", "юго-восточный", "южный", "юго-западный", "западный",
        "северо-западный")
    direction_value = int((deg + 22.5) // 45 % 8)
    direction = str(wind_directions[direction_value])
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
    forecast = ("Погода в Москве: " + main_weather + "\n" + description_weather + "\nТемпература " + str(
        int(temp_min)) + "-" + str(
        int(temp_max)) + "°C\n" + "Давление: " + str(int(float(pressure) * 0.750064)) + " мм рт.ст. Влажность: " + str(
        aqua) + "%\n" + "Ветер: " + wind_type + ", " + str(speed) + " м/с, " + direction)
    write_msg(event.user_id, forecast)


# Основной цикл
input_flag = 0
entered_val = 1
first_currency_index = 14
second_currency_index = 0
currency_nominals = []
currency_value = []
user_sessions = {}
current_user_id = 0
with open("currency_names_nominative_case.txt", 'r', encoding='UTF-8') as file:
    currency_names_nominative_case = [line.rstrip() for line in file]
file.close()

with open("currency_names_genitive_case.txt", 'r', encoding='UTF-8') as file:
    currency_names_genitive_case = [line.rstrip() for line in file]
file.close()

with open("currency_names_genitive_case_one.txt", 'r', encoding='UTF-8') as file:
    currency_names_genitive_case_one = [line.rstrip() for line in file]
file.close()

with open("currency_names_shortcuts.txt", 'r', encoding='UTF-8') as file:
    currency_names_shortcuts = [line.rstrip() for line in file]
file.close()

lower_currency_names_nominative_case = [item.lower() for item in currency_names_nominative_case]
keyboard = VkKeyboard(one_time=True)
for event in longpoll.listen():

    # Если пришло новое сообщение
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.to_me:

        # Если оно имеет метку для меня(то есть бота)
        if event.to_me:
            print('New from {}, text = {}'.format(event.user_id, event.text))
            if current_user_id != event.user_id:
                if not (event.user_id in user_sessions):
                    # Сохраняем сессию прошлого пользователя
                    user_sessions[current_user_id] = [input_flag, entered_val, first_currency_index,
                                                      second_currency_index]
                    # Создаём сессию для нового пользователя
                    input_flag = 0
                    entered_val = 1
                    first_currency_index = 14
                    second_currency_index = 0
                    user_sessions[event.user_id] = [input_flag, entered_val, first_currency_index,
                                                    second_currency_index]
                # Индексы: 0 - input_flag; 1 - введённое значение; 2 - индекс первой; 3 - индекс второй
                else:
                    # Сохраняем сессию прошлого пользователя
                    user_sessions[current_user_id] = [input_flag, entered_val, first_currency_index,
                                                      second_currency_index]
                    # Загружаем сессию текущего пользователя
                    input_flag = user_sessions[event.user_id][0]
                    entered_val = user_sessions[event.user_id][1]
                    first_currency_index = user_sessions[event.user_id][2]
                    second_currency_index = user_sessions[event.user_id][3]
            current_user_id = event.user_id
            request = event.text
            request = request.lower()
            # Сообщение от пользователя
            # Каменная логика ответа
            if input_flag == 1:
                input_flag = 0
                if request.isdigit():
                    if 1 <= int(request) <= 44:
                        first_currency_index = int(request) - 1
                    else:
                        vk_plus.messages.send(user_id=event.user_id, random_id=vk_api.utils.get_random_id(),
                                              keyboard=keyboard.get_keyboard(),
                                              message="Кажется Вы попытались ввести номер валюты в списке, но валюты "
                                                      "с таким номером не существует")
                        continue
                elif len(request) == 3:
                    shortcut = str(request).upper()
                    try:
                        first_currency_index = currency_names_shortcuts.index(shortcut)
                    except ValueError:
                        vk_plus.messages.send(user_id=event.user_id, random_id=vk_api.utils.get_random_id(),
                                              keyboard=keyboard.get_keyboard(),
                                              message="Кажется Вы попытались ввести код валюты, но валюты с таким "
                                                      "кодом не существует")
                        continue
                else:
                    try:
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
                if request.isdigit():
                    if 1 <= int(request) <= 44:
                        second_currency_index = int(request) - 1
                    else:
                        vk_plus.messages.send(user_id=event.user_id, random_id=vk_api.utils.get_random_id(),
                                              keyboard=keyboard.get_keyboard(),
                                              message="Кажется Вы попытались ввести номер валюты в списке, но валюты "
                                                      "с таким номером не существует")
                        continue
                elif len(request) == 3:
                    shortcut = str(request).upper()
                    try:
                        second_currency_index = currency_names_shortcuts.index(shortcut)
                    except ValueError:
                        vk_plus.messages.send(user_id=event.user_id, random_id=vk_api.utils.get_random_id(),
                                              keyboard=keyboard.get_keyboard(),
                                              message="Кажется Вы попытались ввести код валюты, но валюты с таким "
                                                      "кодом не существует")
                        continue
                else:
                    try:
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
                          "Здравствуйте, я бот для конвертации валют.\nВы можете производить взаимодействие с помощью "
                          "команды 'бот'\nДля подробной справки используйте команду '/help'")
                main_menu()
                continue
            if request == "привет":
                write_msg(event.user_id, 'Привет, ' + vk_plus.users.get(user_id=event.user_id)[0]['first_name'])
                main_menu()
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
                for i in range(len(currency_names_nominative_case)):
                    cur_list += str(i + 1) + " " + currency_names_nominative_case[i] + " (" + currency_names_shortcuts[
                        i] + ")" + "\n"
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
                write_msg(event.user_id,
                          "Введите полное название исходной валюты, либо номер валюты в списке, либо её код")
                input_flag = 1
                continue
            elif request == "выбрать целевую валюту":
                write_msg(event.user_id,
                          "Введите полное название исходной валюты либо номер валюты в списке либо её код")
                input_flag = 2
                continue
            elif request == "ввести сумму":
                write_msg(event.user_id, "Введите количество исходной валюты")
                input_flag = 3
                continue
            elif request == "перевести":
                try:
                    answer = cur_calculation(entered_val, first_currency_index, second_currency_index,
                                             currency_nominals, currency_value)
                    if entered_val == 1:
                        name1 = currency_names_nominative_case[first_currency_index]
                    elif entered_val < 1 or 1 < entered_val < 5:
                        name1 = currency_names_genitive_case_one[first_currency_index]
                    else:
                        name1 = currency_names_genitive_case[first_currency_index]
                    if answer == 1:
                        name2 = currency_names_nominative_case[second_currency_index]
                    elif answer < 1 or 1 < answer < 5:
                        name2 = currency_names_genitive_case_one[second_currency_index]
                    else:
                        name2 = currency_names_genitive_case[second_currency_index]
                    write_msg(event.user_id,
                              str(entered_val) + " " + name1 + " = " + str(answer) + " " + name2)
                except:
                    write_msg(event.user_id, "Что-то пошло не так")
                main_menu()
                continue
            elif request == "погода" or request == "2":
                try:
                    moscow()
                except:
                    write_msg(event.user_id, "Что-то пошло не так")
                main_menu()
                continue
            elif request == "/help" or request == "help" or request == "справка" or request == "помощь":
                write_msg(event.user_id, "я бот для конвертации валют.\nТакже я могу показать погоду в Москве\n Для "
                                         "входа в главного меню используйте команду 'бот'\nДля быстрого доступа к "
                                         "конвертору валют введите команду'конвертер валют' или отправьте цифру "
                                         "1\nДля быстрого просмотра прогноза погоды введите команду 'погода' или "
                                         "отправьте цифру 2")
                main_menu()
                continue
            else:
                write_msg(event.user_id, "Неизвестная команда\n Вы можете посмотреть справку по командам с помощью "
                                         "/help")
                main_menu()
