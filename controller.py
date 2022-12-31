import model_mult
import model_sub
import model_sum
import model_div
from constants import MAIN_FILE
import logger
import csv

def file_reading():
    """
    Читает файл

    args -> None
    return -> list
    """  
    with open(MAIN_FILE, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        res_list = (list(file.readline().split(";")))
    return res_list

def write_in_file(update): 
    """
    Добавляет параметр, полученный от пользователя из телеграм, в файл

    args -> str
    return -> None
    """  
    with open (MAIN_FILE, 'a', encoding='utf-8') as temp_file:
        temp_file.write('{};'.format(update.message.text))

def rewrite_file(update):
    """
    Перезаписывает файл, добавляя первый параметр, полученный от пользователя из телеграм

    args -> str
    return -> None
    """  
    with open (MAIN_FILE, 'w', encoding='utf-8') as temp_file:
        temp_file.write('{};'.format(update.message.text))

def Check_num(update):
    """
    Проверяет введенное пользователем число

    args -> str
    return -> bool
    """  
    data = update.message.text
    try:
        float(data)
        
    except ValueError:
        update.message.reply_text('Ошибка! Введены не цифры. Для вещественных чисел, используйте "."\n\n'
        'Повторите ввод числа\n')
        return False
        

def get_operation(a, b):
    """
    Принимает из файла список, из которого получает значение для вида операции и совершает операцию

    args -> float, float
    return -> float
    """
    res_list = file_reading()
    if res_list[-2] == 'сложить': result = model_sum.do_it(a, b)
    elif res_list[-2] == 'вычесть':  result = model_sub.do_it(a, b)
    elif res_list[-2] == 'умножить': result = model_mult.do_it(a, b)
    elif res_list[-2] == 'разделить': result = model_div.do_it(a, b)
    logger.write(f"{a} | {res_list[-2]} | {b} | {result}")
    return result

def get_result():
    """
   Принимает из файла список, из которого получает значение для вида операции и совершает операцию

    args -> None
    return -> float
    """
    
    res_list = file_reading()
  
    if res_list[0] == 'Вещественные числа':
        a = (float(res_list[1]))
        b = (float(res_list[2]))
        return round(get_operation(a,b), 5)
    else: 
        a = complex(float(res_list[3]), float(res_list[1]))
        b = complex(float(res_list[4]), float(res_list[2]))
        return get_operation(a,b)

