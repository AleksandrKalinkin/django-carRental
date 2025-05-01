import os
import sys
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
import django
import logging

# Настройка Django
PROJECT_PATH = r'C:\Users\Настя\Desktop\Обучение ТОР\Python\Django\DjangoProject\pythonProject1\carRental'
sys.path.append(PROJECT_PATH)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carRental.settings')
django.setup()

from cars.models import Cars  # Импортируем вашу модель Cars

API_TOKEN = '7906918584:AAGBYIjdLhPgqhZ6D0yhQuQ45VIbOWKZ10E'
bot = telebot.TeleBot(API_TOKEN)

# Глобальные переменные для хранения состояния
user_states = {}


@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("Показать каталог", callback_data='show_catalog'),
        InlineKeyboardButton("Весь список авто", callback_data='full_list')
    )
    markup.row(
        InlineKeyboardButton("Помощь", callback_data='help'),
        InlineKeyboardButton("Ссылка на сайт", callback_data='website')
    )

    bot.send_message(
        message.chat.id,
        "Привет! Я бот для просмотра каталога автомобилей компании CarRentRzn\n\n"
        "Выберите вариант просмотра:",
        reply_markup=markup
    )


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(
        message.chat.id,
        "Доступные команды:\n"
        "/start - начать работу с ботом\n"
        "/help - показать эту справку"
    )


@bot.callback_query_handler(func=lambda call: call.data == 'help')
def handle_help_button(call):
    help(call.message)
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data == 'website')
def handle_website_button(call):
    bot.send_message(call.message.chat.id, "Наш сайт: http://127.0.0.1:8000/")
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data == 'show_catalog')
def show_catalog(call):
    try:
        # Получаем все автомобили из БД
        cars = Cars.objects.select_related('category').all()

        if not cars.exists():
            bot.send_message(call.message.chat.id, "Каталог автомобилей пуст!")
            return

        # Сохраняем данные в глобальную переменную
        user_states[call.message.chat.id] = {
            'cars': list(cars),
            'current_index': 0,
            'has_photo': True
        }

        # Показываем первый автомобиль
        show_car(call.message.chat.id, call.message.message_id if hasattr(call.message, 'message_id') else None)

    except Exception as e:
        bot.send_message(call.message.chat.id, f"Произошла ошибка: {str(e)}")


@bot.callback_query_handler(func=lambda call: call.data == 'full_list')
def show_full_list(call):
    try:
        cars = Cars.objects.select_related('category').all()

        if not cars.exists():
            bot.send_message(call.message.chat.id, "Каталог автомобилей пуст!")
            return

        # Формируем список всех автомобилей
        cars_list = []
        for i, car in enumerate(cars, 1):
            car_info = (
                f"{i}. <b>{car.name}</b>\n"
                f"   Категория: {car.category.name if car.category else 'Не указана'}\n"
                f"   Цена: {float(car.price):.2f} ₽/сутки\n"
                f"   Описание: {car.short_description}\n"
            )
            cars_list.append(car_info)

        # Разбиваем список на части, если он слишком длинный
        message_text = "<b>Полный список автомобилей:</b>\n\n" + "\n".join(cars_list)
        if len(message_text) > 4000:  # Ограничение Telegram на длину сообщения
            parts = [message_text[i:i + 4000] for i in range(0, len(message_text), 4000)]
            for part in parts:
                bot.send_message(call.message.chat.id, part, parse_mode='HTML')
        else:
            bot.send_message(call.message.chat.id, message_text, parse_mode='HTML')

        # Добавляем кнопку для просмотра в карусели
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Просмотреть в карусели", callback_data='show_catalog'))
        bot.send_message(call.message.chat.id, "Хотите просмотреть автомобили в виде карусели?", reply_markup=markup)

    except Exception as e:
        bot.send_message(call.message.chat.id, f"Произошла ошибка: {str(e)}")


def show_car(chat_id, message_id=None):
    if chat_id not in user_states or not user_states[chat_id]['cars']:
        bot.send_message(chat_id, "Каталог автомобилей недоступен.")
        return

    data = user_states[chat_id]
    cars = data['cars']
    index = data['current_index']
    car = cars[index]

    # Создаем клавиатуру для навигации
    markup = InlineKeyboardMarkup()
    row = []
    if len(cars) > 1:
        row.append(InlineKeyboardButton("← Предыдущая", callback_data='prev_car'))
        row.append(InlineKeyboardButton("Следующая →", callback_data='next_car'))
        markup.row(*row)
    markup.row(
        InlineKeyboardButton("Весь список", callback_data='full_list'),
        InlineKeyboardButton("Закрыть", callback_data='close_catalog')
    )

    # Формируем описание автомобиля
    caption = (
        f"<b>{car.name}</b>\n\n"
        f"{car.short_description}\n\n"
        f"<b>Цена:</b> {float(car.price):.2f} ₽/сутки\n"
        f"<b>Категория:</b> {car.category.name if car.category else 'Не указана'}"
    )

    try:
        if car.image:
            with open(car.image.path, 'rb') as photo:
                if message_id is None:
                    bot.send_photo(
                        chat_id,
                        photo,
                        caption=caption,
                        parse_mode='HTML',
                        reply_markup=markup
                    )
                else:
                    try:
                        bot.edit_message_media(
                            chat_id=chat_id,
                            message_id=message_id,
                            media=InputMediaPhoto(photo),
                            reply_markup=markup
                        )
                        bot.edit_message_caption(
                            chat_id=chat_id,
                            message_id=message_id,
                            caption=caption,
                            parse_mode='HTML',
                            reply_markup=markup
                        )
                        data['has_photo'] = True
                    except telebot.apihelper.ApiTelegramException as e:
                        if "message is not modified" in str(e):
                            pass
                        else:
                            raise
        else:
            if message_id is None:
                bot.send_message(
                    chat_id,
                    caption + "\n\n(Изображение отсутствует)",
                    parse_mode='HTML',
                    reply_markup=markup
                )
            else:
                if data.get('has_photo', True):
                    bot.delete_message(chat_id, message_id)
                    bot.send_message(
                        chat_id,
                        caption + "\n\n(Изображение отсутствует)",
                        parse_mode='HTML',
                        reply_markup=markup
                    )
                else:
                    bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=message_id,
                        text=caption + "\n\n(Изображение отсутствует)",
                        parse_mode='HTML',
                        reply_markup=markup
                    )
                data['has_photo'] = False
    except Exception as e:
        error_msg = f"{caption}\n\n(Не удалось загрузить изображение: {str(e)})"
        if message_id is None:
            bot.send_message(
                chat_id,
                error_msg,
                parse_mode='HTML',
                reply_markup=markup
            )
        else:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=error_msg,
                parse_mode='HTML',
                reply_markup=markup
            )


@bot.callback_query_handler(func=lambda call: call.data in ['prev_car', 'next_car'])
def navigate_car(call):
    data = user_states.get(call.message.chat.id)
    if not data:
        bot.answer_callback_query(call.id, "Сессия устарела. Начните заново.")
        return

    cars = data['cars']
    index = data['current_index']

    if call.data == 'prev_car':
        data['current_index'] = (index - 1) % len(cars)
    else:
        data['current_index'] = (index + 1) % len(cars)

    show_car(call.message.chat.id, call.message.message_id)
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data == 'close_catalog')
def close_catalog(call):
    if call.message.chat.id in user_states:
        del user_states[call.message.chat.id]

    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(call.message.chat.id, "Каталог закрыт. Для повторного просмотра нажмите /start")
    bot.answer_callback_query(call.id)


if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling()