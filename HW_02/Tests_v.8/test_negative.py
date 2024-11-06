'''
Автотест архиватора 7z
Файл с негативными тестами (проверками)

v.7.1

для работы с pytest его нужно установить!
см. Tests_v.4

код запускается с консоли:
1) переходим в терминал ИДЕ
2) переходим в папку, где лежит файл с тестами
3) пишем pytest (либо указываем явно pytest <имя файла>)
 так же указываем ключ -v для более информативного вывода
'''

from checkers import checkout_negative

folder_in = "/home/user/test_folder" # куда распаковываем архив
folder_neg = "/home/user/folder_neg" # откуда берем поврежденный архив

def test_nstep1():
    #test neg 1
    assert checkout_negative("cd {}; 7z e arh3.7z -o{} -y".format(folder_neg, folder_in),
                             "ERROR"), "test negative 1 FAIL"

def test_nstep2():
    #test neg 2
    assert checkout_negative("cd {}; 7z t arh.7z".format(folder_neg), "ERROR"), \
        "test negative 2 FAIL"