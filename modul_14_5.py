from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from  crud_function import *
import asyncio


api = ""
bot = Bot(token = api)
dp = Dispatcher(bot, storage= MemoryStorage())

initiate_db()
insert_products()

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button0 = KeyboardButton(text="Регистрация")
kb.add(button0)
button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
kb.add(button, button2)
button3 = KeyboardButton(text="Купить")
kb.add(button3)

catalog_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Product1", callback_data="product_1")],
        [InlineKeyboardButton(text="Product2", callback_data="Product_2")],
        [InlineKeyboardButton(text="Product3", callback_data="Product_3")],
        [InlineKeyboardButton(text="Product4", callback_data="product_4")]
    ]
)
class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()

@dp.message_handler(text="Регистрация")
async def sing_up(message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    username = message.text
    if is_included(username):
        await message.answer("Пользователь существует, введите другое имя:")
    else:
        await state.update_data(username=username)
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()

@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    email = message.text
    await state.update_data(email=email)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    age = int(message.text)
    data = await state.get_data()
    username = data['username']
    email = data['email']

    add_user(username, email, age)
    await message.answer("Регистрация прошла успешно")

    await state.finish()

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


def get_inline_menu():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(text="Рассчитать норму калорий", callback_data="calories"),
        InlineKeyboardButton(text="Формулы расчёта", callback_data="formulas")
    )
    return keyboard

@dp.message_handler(text="Купить")
async def get_buying_list(message):
    products = get_all_products()

    catalog_kb = InlineKeyboardMarkup()
    for product in products:
        product_id = product[0]
        product_name = product[1]
        catalog_kb.add(InlineKeyboardButton(text=product_name, callback_data=f"product_{product_id}"))

    for product in products:
        product_id, title, description, price, image_path = product
        with open(image_path, 'rb') as photo:
            await message.answer_photo(
                photo, caption=f"Название: {title}\nОписание: {description}\nЦена: {price} руб."
            )
    await message.answer("Выберите продукт для покупки:", reply_markup=catalog_kb)

@dp.message_handler(text = ['Привет', 'привет'])
async def urban_message(message):
    await message.answer("Введите команду /start, чтобы начать общение.")

@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью.", reply_markup= kb)

@dp.message_handler(text = "Рассчитать")
async def set_age(message, state):
    await message.answer("Вывберите опцию:", reply_markup=get_inline_menu())

@dp.callback_query_handler(text="formulas")
async def get_formulas(call):
    formula = "10 × вес (кг) + 6,25 × рост (см) − 5 × возраст (г) − 161"
    await call.message.answer(f"Формула Миффлина-Сан Жеора для женщин:\n{formula}")
    await call.answer()

@dp.callback_query_handler(text="calories")
async def set_age(call, state):
    await call.message.answer("Введите свой возраст:")
    await UserState.age.set()
    await call.answer()

@dp.message_handler(state= UserState.age)
async def set_growth(message, state):
    await state.update_data(age= message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    try:
        age = int(data['age'])
        growth = int(data['growth'])
        weight = int(data['weight'])

        calories = 10 * weight + 6.25 * growth - 5 * age - 161

        await message.reply(f"Ваша норма калорий: {calories:.2f} ккал в день.")
    except ValueError:
        await message.reply("Пожалуйста, введите корректные числовые значения.")

    await state.finish()

@dp.callback_query_handler(text="product_1")
async def buy_product_1(call: types.CallbackQuery):
    await call.message.answer("Вы успешно приобрели продукт 1!")
    await call.answer()

@dp.callback_query_handler(text="product_2")
async def buy_product_2(call: types.CallbackQuery):
    await call.message.answer("Вы успешно приобрели продукт 2!")
    await call.answer()

@dp.callback_query_handler(text="product_3")
async def buy_product_3(call: types.CallbackQuery):
    await call.message.answer("Вы успешно приобрели продукт 3!")
    await call.answer()

@dp.callback_query_handler(text="product_4")
async def buy_product_4(call: types.CallbackQuery):
    await call.message.answer("Вы успешно приобрели продукт 4!")
    await call.answer()

if __name__ == "__main__":
    products = get_all_products()
    print("Продукты в базе данных:", products)

    executor.start_polling(dp, skip_updates=True)