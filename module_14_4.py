# Домашнее задание по теме "План написания админ панели".
# Цель: написать простейшие CRUD функции для взаимодействия с базой данных.

# Установлен Aiogram последней версии для Python 3.12!!!

from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import FSInputFile
import asyncio
from crud_functions import get_all_products

# Инициализация бота и диспетчера
TOKEN = "My_Token"
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()
dp.include_router(router)
button_1 = KeyboardButton(text='Рассчитать')
button_2 = KeyboardButton(text='Информация')
button_3 = KeyboardButton(text='Купить')

kb = ReplyKeyboardMarkup(keyboard=[[button_1, button_2], [button_3]], resize_keyboard=True)

# Создание инлайн-клавиатуры с 4 кнопками
but_inl_1 = InlineKeyboardButton(text='Product1', callback_data='product_buying')
but_inl_2 = InlineKeyboardButton(text='Product2', callback_data='product_buying')
but_inl_3 = InlineKeyboardButton(text='Product3', callback_data='product_buying')
but_inl_4 = InlineKeyboardButton(text='Product4', callback_data='product_buying')

catalog_kb = InlineKeyboardMarkup(inline_keyboard=[
    [but_inl_1],
    [but_inl_2],
    [but_inl_3],
    [but_inl_4]])

# Запуск функции get_all_products из модуля crud_functions
get_all_products()

@router.message(F.text == 'Купить') # Фильтр F.text == 'Купить' проверяет, соответствует ли текст
# входящего сообщения строке 'Купить'
async def get_buying_list(message: types.Message):
    products = get_all_products()
    for product in products:
        id, title, description, price = product
        await message.answer(f"Название: {title} | Описание: {description} | Цена: {price}")
    # for i in range(1, 5):
    #     await message.answer(f"Название: Product{i} | Описание: описание {i} | Цена: {i * 100}")
        file_path = f'files/vit{id}.png'
        try:
            # Открываем файл вручную и передаем его в FSInputFile
            with open(file_path, 'rb') as file:
                photo = FSInputFile(file_path)
                await message.answer_photo(photo)
        except FileNotFoundError:
            await message.answer("Файл не найден.")
        except Exception as e:
            await message.answer(f"Произошла ошибка: {e}")
            print(e)
    await message.answer("Выберите продукт для покупки:", reply_markup=catalog_kb)

# Callback хэндлер, который реагирует на текст "product_buying"
@router.callback_query(F.data == 'product_buying')
async def send_confirm_message(call: CallbackQuery):
    await call.message.answer("Вы успешно приобрели продукт!")


# Определение состояний пользователя
class UserState(StatesGroup):  # создаем класс, который наследуется от группы состояний
    age = State()  # экземпляр класса State для определения состояния возраста
    growth = State()  # ...состояния роста
    weight = State()  # ...состояния веса


# Проверка, является ли вводимое значение положительным целым числом
# value.isdigit() — проверяем, что строка состоит только из цифр.
# int(value) > 0 — проверяем, что число положительное.
def is_valid_number(value):
    return value.isdigit() and int(value) > 0


# Ответ на нажатие кнопки 'Рассчитать'
@router.message(F.text.lower() == 'рассчитать')
async def set_age(message: types.Message, state: FSMContext):
    await message.answer("Введите свой возраст:")  # бот отправляет сообщение с просьбой ввести возраст
    await state.set_state(UserState.age)  # устанавливаем состояние age, где бот ожидает ввода возраста


# Хендлер для обработки возраста
@router.message(UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    if is_valid_number(message.text):
        await state.update_data(age=int(message.text))  # обновляет данные состояния, сохраняя возраст пользователя
        await message.answer("Введите свой рост (в см):")
        await state.set_state(UserState.growth)  # устанавливаем состояние growth, где бот ожидает ввода роста
    else:
        await message.answer("Возраст должен быть положительным числом. Пожалуйста, введите корректное значение.")


# Хендлер для обработки роста
@router.message(UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    if is_valid_number(message.text):
        await state.update_data(growth=int(message.text))  # обновляет данные состояния, сохраняя рост пользователя
        await message.answer("Введите свой вес (в кг):")
        await state.set_state(UserState.weight)  # устанавливаем состояние weight, где бот ожидает ввода вес
    else:
        await message.answer("Рост должен быть положительным числом. Пожалуйста, введите корректное значение.")


# Хендлер для обработки веса и вычисления нормы калорий
@router.message(UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    if is_valid_number(message.text):
        await state.update_data(weight=int(message.text))  # обновляет данные состояния, сохраняя вес пользователя
        data = await state.get_data()  # извлекаем все данные введенные пользователем (возраст, рост, вес)

        age = data['age']
        growth = data['growth']
        weight = data['weight']

        # Формула Миффлина - Сан Жеора для мужчин
        calories = 10 * weight + 6.25 * growth - 5 * age + 5

        await message.answer(f"Ваша норма калорий: {calories:.2f} ккал в день.")

        await state.clear()  # Завершение машины состояний
    else:
        await message.answer("Вес должен быть положительным числом. Пожалуйста, введите корректное значение.")


# Команда start
@dp.message(Command("start"))
async def start_form(message: Message):
    # await message.answer("Привет! Я бот, помогающий твоему здоровью. Если хочешь узнать свою суточную норму калорий, "
    #                      "то напиши слово 'Calories'.")
    await message.answer("Привет! Я бот, помогающий твоему здоровью. Если хочешь узнать свою суточную норму "
                         "калорий, то нажми 'Рассчитать'.", reply_markup=kb)


# Хендлер для перенаправления всех остальных сообщений на start
@router.message(~F.text.lower('Рассчитать') and ~F.state(UserState.age) and ~F.state(UserState.growth)
                and ~F.state(UserState.weight))
async def redirect_to_start(message: types.Message):
    await start_form(message)  # Перенаправляем сообщение на хендлер команды /start


# Основная функция запуска бота
async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
