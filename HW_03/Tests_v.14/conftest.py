'''
файл с фикстурами
'''

import random
import pytest
import string
import yaml
from datetime import datetime
from checkers import checkout, getout


with open('config.yaml') as f:
    data = yaml.safe_load(f) # safe_load - безопасный способ считывания информации


@pytest.fixture()
def make_folders():
    # создание тестовых каталогов
    # проверим наличие пустоой строки, чтобы функция всегда возвращала Истину
    return checkout("mkdir {} {} {} {}".format(data["folder_in"],
                                               data["folder_out"],
                                               data["folder_from"],
                                               data["folder_neg"]), "")


@pytest.fixture()
def clear_folders():
    # отчищение тестовых каталогов
    # rm - команда для удаления файлов
    # -rf ключи, чтобы рекурсивно все удалить и нам не задавали лишних вопросов
    # /* чтобы уж точно все удалить из каталогов (если там будут подкаталоги)
    return checkout("rm -rf {}/* {}/* {}/* {}/*".format(data["folder_in"],
                                                        data["folder_out"],
                                                        data["folder_from"],
                                                        data["folder_neg"]), "")


@pytest.fixture()
def make_files():
    # создание тестовых файлов опред. размера, с рандомными именами, заполненные данными
    list_of_files = [] # создаем пустой список
    for i in range(data["count"]): # в цикле создаем опред.кол-во файлов (кол-во итераций цикла)
        # генерируем имена файлов из случайных букв в верх.регистре и цифр, длиной 5 символов
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        # cd {} - переходим в папку, в кот. будем созд. случ. файлы
        # dd - команда Linux
        # if=/dev/urandom - где Linux берет рандом
        # of={} - указ. имя файла
        # bs=1M - указ. размер файла
        # count=1 - счетчик файлов (сколько раз) т.к. у нас и так цикл, то указ. 1 раз
        # iflag=fullblock - метод заполнения файлов ("поплотнее"), не очень важный параметр
        if checkout("cd {}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data["folder_from"],
                                                                                           filename,
                                                                                           data["bs"]), ""):
            # сохраняем имя только если все прошло успешно (проверяем код возврата 0)
            list_of_files.append(filename) # добавляем созданное имя в список
    return list_of_files


@pytest.fixture()
def make_subfolder():
    # создание подкаталога и файла в нем
    filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

    # если операция по созданию каталога не успешна
    if not checkout("cd {}; mkdir {}".format(data["folder_from"], subfoldername), ""):
        return None, None # возвращаем "ничего" для каталога и файла (второй аргумент)
    # если операция по созданию файла не успешна
    if not checkout("cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(data["folder_from"],
                                                                                              subfoldername,
                                                                                              filename), ""):
        return subfoldername, None # возвращаем имя каталога и "ничего" для файла
    else:
        return subfoldername, filename


@pytest.fixture(autouse=True)
def print_time():
    # выводит время текущее время перед стартом теста и сразу после завершения теста
    # autouse=True - чтобы не вписывать фикстуру во все тесты
    # импортируем библиотеку
    # %H:%M:%S.%f - часы:минуты:секунды.милисекунды
    print("Start: {}".format(datetime.now().strftime("%H:%M:%S.%f")))
    yield print("Stop: {}".format(datetime.now().strftime("%H:%M:%S.%f")))


@pytest.fixture()
def make_bad_arh():
    # создание архива и его повреждение
    checkout("cd {}; 7z a {}/broken_arh".format(data["folder_from"], data["folder_neg"]), "")
    checkout("truncate -s 1 {}/broken_arh.{}".format(data["folder_neg"],
                                                     data["type"]), "Everything is Ok")
    yield "broken_arh"
    checkout("rm -f {}/broken_arh.{}".format(data["folder_neg"], data["type"]), "")


@pytest.fixture(autouse=True)
def stat_lig():
    yield
    time = datetime.now().strftime("%H:%M:%S.%f")
    stat = getout("cat /proc/loadavg")
    checkout("echo 'time: {} count: {} size: {} load: {}' >> stat.txt".format(time,
                                                                              data["count"],
                                                                              data["bs"],
                                                                              stat), "")