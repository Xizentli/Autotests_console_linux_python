'''
Автотест архиватора 7z
Файл с позитивными тестами (проверками)

v.8 - добавили позитивные проверки на вывод списка файлов и рахархивирование с путями

для работы с pytest его нужно установить!
см. Tests_v.4

код запускается с консоли:
1) переходим в терминал ИДЕ
2) переходим в папку, где лежит файл с тестами
3) пишем pytest (либо указываем явно pytest <имя файла>)
 так же указываем ключ -v для более информативного вывода
 pytest -v
'''

from checkers import checkout

folder_in = "/home/user/test_folder" # куда распаковываем архив
folder_out = "/home/user/test_out" # куда помещаем архив
folder_from = "/home/user/test_dir" # откуда берем файлы для архивации
folder_neg = "/home/user/folder_neg" # откуда берем поврежденный архив


def test_step1():
    #test1
    res1 = checkout("cd {}; 7z a {}/arh".format(folder_from, folder_out), "Everything is Ok")
    res2 = checkout("ls {}".format(folder_out), "arh.7z")
    assert res1 and res2, "test1 FAIL"

def test_step2():
    #test2
    res1 = checkout("cd {}; 7z e arh.7z -o{} -y".format(folder_out, folder_in),
                    "Everything is Ok")
    res2 = checkout("ls {}".format(folder_in), "7zip command")
    res3 = checkout("ls {}".format(folder_in), "lessen_02")
    res4 = checkout("ls {}".format(folder_in), "README")
    assert res1 and res2 and res3 and res4, "test2 FAIL"

def test_step3():
    #test3
    assert checkout("cd {}; 7z t arh.7z".format(folder_out), "Everything is Ok"), \
        "test3 FAIL"

def test_step4():
    #test4
    assert checkout("cd {}; 7z u arh.7z".format(folder_out), "Everything is Ok"), \
        "test4 FAIL"
def test_step5():
    #test5
    assert checkout("cd {}; 7z l arh.7z".format(folder_out), "....A"), \
        "test6 FAIL"

def test_step6():
    #test6
    assert checkout("cd {}; 7z x arh.7z -o{}".format(folder_out, folder_in),
                    "Everything is Ok"), "test6 FAIL"

def test_step10():
    #test10
    assert checkout("cd {}; 7z d arh.7z".format(folder_out), "Everything is Ok"), \
        "test5 FAIL"

