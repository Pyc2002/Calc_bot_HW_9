from config import TOKEN
import logging
import controller



from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext
    
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

TYPE, FIRST_COMP, SECOND_COMP, FIRST_NUM, SECOND_NUM, OPERATION = range(6)

def Start(update, _):
    """ Запускает первое сообщение в телеграм с кнопками

    args -> update message
    return -> int (переход на следующий шаг по списку)
    
    """
    reply_keyboard = [['Вещественные числа', 'Комплексные числа']]
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        'Я - калькулятор. Могу выполнить простые вычисления.\n'
        'Команда /cancel, чтобы прекратить разговор.\n\n'
        'Вещественные числа или Комплексные числа?',
        reply_markup=markup_key,)
    return TYPE


def Type(update, _):
    """ Записывает поступившее сообщение и запускает второе сообщение в телеграм 
        с условием выбора типа операции

    args -> update message
    return -> int (переход на следующий шаг по списку)
            или int (переход на предыдущий шаг по списку)
    
    """
    user = update.message.from_user
    logger.info("Пользователь %s выбрал тип: %s", user.first_name, update.message.text)
    controller.rewrite_file(update)
    if update.message.text == 'Вещественные числа':
        update.message.reply_text('Введите первое вещественное число.\n' 'Команда /cancel, чтобы прекратить разговор.', reply_markup=ReplyKeyboardRemove(),)
        return FIRST_NUM
    else:
        update.message.reply_text('Введите первое мнимое число. \n''Команда /cancel, чтобы прекратить разговор.')
        return FIRST_COMP

def First_comp(update, _):
    """ Записывает поступившее сообщение и запускает третье сообщение в телеграм 

    args -> update message
    return -> int (переход на следующий шаг по списку)
        
    """
    user = update.message.from_user
    if controller.Check_num(update) == False: return FIRST_COMP  
    logger.info("Пользователь %s ввел первое мнимое число: %s", user.first_name, update.message.text)
    controller.write_in_file(update)
    update.message.reply_text('Введите второе мнимое число. \n''Команда /cancel, чтобы прекратить разговор.')
    return SECOND_COMP

def Second_comp(update, _):
    """ Записывает поступившее сообщение и запускает четвертое сообщение в телеграм 

    args -> update message
    return -> int (переход на следующий шаг по списку)
     
    """
    user = update.message.from_user
    if controller.Check_num(update) == False: return SECOND_COMP 
    logger.info("Пользователь %s ввел второе мнимое число: %s", user.first_name, update.message.text)
    controller.write_in_file(update)
    update.message.reply_text('Введите первое вещественное число. \n''Команда /cancel, чтобы прекратить разговор.')
    return FIRST_NUM

def First_num(update, _):
    """ Записывает поступившее сообщение и запускает пятое сообщение в телеграм 

    args -> update message
    return -> int (переход на следующий шаг по списку)
     
    """
    user = update.message.from_user
    if controller.Check_num(update) == False: return FIRST_NUM   
    logger.info("Пользователь %s ввел первое число: %s", user.first_name, update.message.text)
    controller.write_in_file(update)
    update.message.reply_text('Введите второе вещественное число. \n''Команда /cancel, чтобы прекратить разговор.')
    return SECOND_NUM

def Second_num(update, _):
    """ Записывает поступившее сообщение и запускает пятое сообщение в телеграм с кнопками 

    args -> update message
    return -> int (переход на следующий шаг по списку)
     
    """
    user = update.message.from_user
    if controller.Check_num(update) == False: return SECOND_NUM 
    logger.info("Пользователь %s ввел второе число: %s", user.first_name, update.message.text)
    controller.write_in_file(update)
    reply_keyboard = [['сложить', 'вычесть', 'умножить', 'разделить']]
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        'Теперь выберите операцию.\n'
        'Команда /cancel, чтобы прекратить разговор.\n\n'
        'Cложить, вычесть, умножить или разделить?',
        reply_markup=markup_key,)
    
    return OPERATION

def Operation(update, _):
    """ Записывает поступившее сообщение и запускает шестое сообщение в телеграм 

    args -> update message
    return -> завершение ConversationHandler
     
    """
    user = update.message.from_user
    logger.info("Пользователь %s выбрал операцию: %s", user.first_name, update.message.text)
    controller.write_in_file(update)
    update.message.reply_text (f'Спасибо! Ваш ответ: {controller.get_result()}, \n' 'Команда /start, чтобы начать заново.', reply_markup=ReplyKeyboardRemove(),)
    logger.info("Пользователь %s получил ответ: %s", user.first_name, controller.get_result())
    return ConversationHandler.END

def Cancel(update, _):
    """ Записывает поступившее сообщение с командой отмены 

    args -> update message
    return -> завершение ConversationHandler
     
    """
    user = update.message.from_user
    logger.info("Пользователь %s отменил разговор.", user.first_name)
    update.message.reply_text(
        'Мое дело предложить - Ваше отказаться'
        ' Будет скучно - пиши.', 
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

def main():
    """ Основная логика ConversationHandler

    args -> None
    return -> None
     
    """
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        
        entry_points=[CommandHandler('start', Start)],     
        states = {
            TYPE: [MessageHandler(Filters.regex('^(Вещественные числа|Комплексные числа)$'), Type)], 
            FIRST_COMP: [MessageHandler(Filters.text & ~Filters.command, First_comp)],
            SECOND_COMP: [MessageHandler(Filters.text & ~Filters.command, Second_comp)],
            FIRST_NUM: [MessageHandler(Filters.text & ~Filters.command, First_num)],
            SECOND_NUM: [MessageHandler(Filters.text & ~Filters.command, Second_num)],
            OPERATION: [MessageHandler(Filters.regex('^(сложить|вычесть|умножить|разделить)$'), Operation)],
        },
        
        fallbacks=[CommandHandler('cancel', Cancel)],
        
    )
  
    dispatcher.add_handler(conv_handler)
    
    
    updater.start_polling()
    updater.idle()


   
