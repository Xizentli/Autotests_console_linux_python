'''
Автотест архиватора 7z
Файл с позитивными тестами (проверками)

v.14

код запускается с консоли:
    cd ..
    cd HW_03/Tests_v.14/
    cd Tests_v.14/
    pytest
    pytest -s - чтобы увидеть время (python3 -m pytest -s)

    или так:
    python3 -m pytest

    отчеты:
    python3 -m pytest --junitxml=report.xml
    python3 -m pytest --html=report.html
    python3 -m pytest --html-report=report-report.html


'''

import yaml
from checkers import checkout, getout


with open('config.yaml') as f:
    data = yaml.safe_load(f) # safe_load - безопасный способ считывания информации

# тестовый класс
class TestPositive:
    # фикстуры передаются в качестве параметров в функции
    def test_step1(self, make_folders, clear_folders, make_files):
        #test1 - создание архива
        res1 = checkout("cd {}; 7z a {}/arh".format(data["folder_from"],
                                                    data["folder_out"]), "Everything is Ok")
        res2 = checkout("ls {}".format(data["folder_out"]), "arh.{}".format(data["type"]))
        assert res1 and res2, "test1 FAIL"


    def test_step2(selt, clear_folders, make_files):
        #test2 - разархивация (+ создание архива) //нет проверки на создание архива, как в test1 ("ls {}")
        # make_files вернул нам список файлов (list_of_files), в котором мы перебираем элементы для сравнения
        res = []
        res.append(checkout("cd {}; 7z a {}/arh".format(data["folder_from"],
                                                        data["folder_out"]), "Everything is Ok"))
        res.append(checkout("cd {}; 7z e arh.{} -o{} -y".format(data["folder_out"],
                                                                data["type"],
                                                                data["folder_in"]), "Everything is Ok"))
        for item in make_files:
            res.append(checkout("ls {}".format(data["folder_in"]), item))
        assert all(res), "test2 FAIL"


    def test_step3(self):
        #test3 - проверка целостности архива
        assert checkout("cd {}; 7z t arh.{}".format(data["folder_out"],
                                                    data["type"]), "Everything is Ok"), "test3 FAIL"


    def test_step4(self):
        #test4 - обновление файлов в архиве
        assert checkout("cd {}; 7z u arh.{}".format(data["folder_from"],
                                                    data["type"]), "Everything is Ok"), "test4 FAIL"


    def test_step5(self, clear_folders, make_files):
        #test5 - список содержимого архива
        res = []
        # заново создаем архив
        res.append(checkout("cd {}; 7z a {}/arh".format(data["folder_from"],
                                                        data["folder_out"]), "Everything is Ok"))
        for item in make_files:
            # проверяем вхождение имен файлов из переданного списка фикстурой make_files в вывод
            res.append(checkout("cd {}; 7z l arh.{}".format(data["folder_out"],
                                                            data["type"]), item))
        assert all(res), "test5 FAIL"


    def test_step6(self, clear_folders, make_files, make_subfolder):
        #test6 - извлечение файлов с полными путями
        res = []
        # заново создаем архив
        res.append(checkout("cd {}; 7z a {}/arh".format(data["folder_from"],
                                                        data["folder_out"]), "Everything is Ok"))
        res.append(checkout("cd {}; 7z x arh.{} -o{} -y".format(data["folder_out"],
                                                                data["type"],
                                                                data["folder_in"]), "Everything is Ok"))

        # проверяем, что файлы разархивировались и находятся в нужном каталоге
        for item in make_files:
            res.append(checkout("ls {}".format(data["folder_in"]), item))

        # проверяем, что подкаталог упаковался и распаковался с сохранением структуры каталога
        # т.к. make_subfolder возвращает список с двумя аргументами, то обращаемся к ним по индексу:
        # make_subfolder[0] - содержит имя каталога
        # make_subfolder[1] - содержит имя файла
        res.append(checkout("ls {}".format(data["folder_in"]), make_subfolder[0])) # сначала проверяем наличие подкаталога
        res.append(checkout("ls {}/{}".format(data["folder_in"], make_subfolder[0]), make_subfolder[1])) # потом проверяем наличие в нем файла
        assert all(res), "test6 FAIL"


    def test_step7(self):
        #test7 - удаление файлов из архива
        assert checkout("cd {}; 7z d arh.{}".format(data["folder_out"],
                                                    data["type"]), "Everything is Ok"), "test7 FAIL"


    def test_step8(self, clear_folders, make_files):
        #test8 - проверка хэша
        res = []
        for item in make_files:
            res.append(checkout("cd {}; 7z h {}".format(data["folder_from"], item), "Everything is Ok"))
            hash = getout("cd {}; crc32 {}".format(data["folder_from"], item)).upper()
            res.append(checkout("cd {}; 7z h {}".format(data["folder_from"], item), hash))
        assert all(res), "test8 FAIL"