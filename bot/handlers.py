from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from api import ExchangeRateAPI
from database import Database
from .keyboards import get_main_keyboard

router = Router()

api: ExchangeRateAPI = None
db: Database = None


def init_handlers(exchange_api: ExchangeRateAPI, database: Database):
    global api, db
    api = exchange_api
    db = database


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "👋 Привет! Я бот для отслеживания курсов валют.\n\n"
        "Основные функции:\n"
        "• Текущие курсы RUB/CNY\n"
        "• Конвертер валют\n"
        "• Уведомления об изменениях\n"
        "• Целевые курсы\n"
        "• Предложение обмена\n\n"
        "Используйте команды или кнопки ниже:",
        reply_markup=get_main_keyboard()
    )


@router.message(Command("rates"))
@router.callback_query(F.data == "rates")
async def cmd_rates(event: Message | CallbackQuery):
    rate = await api.get_rub_cny_rate()
    if rate:
        text = f"📊 Текущий курс RUB/CNY:\n\n1 RUB = {rate:.4f} CNY\n1 CNY = {1/rate:.2f} RUB"
    else:
        text = "❌ Не удалось получить курс валют"
    
    if isinstance(event, CallbackQuery):
        await event.message.edit_text(text, reply_markup=get_main_keyboard())
        await event.answer()
    else:
        await event.answer(text, reply_markup=get_main_keyboard())


@router.message(Command("convert"))
async def cmd_convert(message: Message):
    args = message.text.split()
    if len(args) != 4:
        await message.answer(
            "Использование: /convert [сумма] [из] [в]\n"
            "Пример: /convert 1000 RUB CNY"
        )
        return
    
    try:
        amount = float(args[1])
        from_currency = args[2].upper()
        to_currency = args[3].upper()
    except ValueError:
        await message.answer("❌ Неверный формат суммы")
        return
    
    result = await api.convert(amount, from_currency, to_currency)
    if result:
        await message.answer(
            f"💱 Конвертация:\n\n"
            f"{amount:.2f} {from_currency} = {result:.2f} {to_currency}",
            reply_markup=get_main_keyboard()
        )
    else:
        await message.answer("❌ Не удалось выполнить конвертацию")


@router.callback_query(F.data == "convert")
async def callback_convert(callback: CallbackQuery):
    await callback.message.edit_text(
        "💱 Для конвертации используйте команду:\n"
        "/convert [сумма] [из] [в]\n\n"
        "Пример: /convert 1000 RUB CNY",
        reply_markup=get_main_keyboard()
    )
    await callback.answer()


@router.message(Command("subscribe"))
@router.callback_query(F.data == "subscribe")
async def cmd_subscribe(event: Message | CallbackQuery):
    user_id = event.from_user.id
    chat_id = event.chat.id if isinstance(event, Message) else event.message.chat.id
    
    if isinstance(event, CallbackQuery):
        await event.answer()
    
    success = await db.add_subscription(user_id, chat_id)
    if success:
        text = "✅ Вы подписались на уведомления о курсах валют!"
    else:
        text = "❌ Ошибка при подписке"
    
    if isinstance(event, CallbackQuery):
        await event.message.edit_text(text, reply_markup=get_main_keyboard())
    else:
        await event.answer(text, reply_markup=get_main_keyboard())


@router.message(Command("target"))
@router.callback_query(F.data == "target")
async def cmd_target(event: Message | CallbackQuery):
    if isinstance(event, CallbackQuery):
        await event.message.edit_text(
            "🎯 Для установки целевого курса используйте:\n"
            "/target [валюта] [курс]\n\n"
            "Пример: /target CNY 12.5",
            reply_markup=get_main_keyboard()
        )
        await event.answer()
        return
    
    args = event.text.split()
    if len(args) != 3:
        await event.answer(
            "Использование: /target [валюта] [курс]\n"
            "Пример: /target CNY 12.5"
        )
        return
    
    currency = args[1].upper()
    try:
        target_rate = float(args[2])
    except ValueError:
        await event.answer("❌ Неверный формат курса")
        return
    
    user_id = event.from_user.id
    success = await db.add_target_rate(user_id, currency, target_rate)
    if success:
        await event.answer(
            f"✅ Целевой курс установлен:\n"
            f"{currency} = {target_rate}",
            reply_markup=get_main_keyboard()
        )
    else:
        await event.answer("❌ Ошибка при установке целевого курса")


@router.message(Command("exchange"))
@router.callback_query(F.data == "exchange")
async def cmd_exchange(event: Message | CallbackQuery):
    text = (
        "💰 Обмен RUB на CNY\n\n"
        "Для обмена валют свяжитесь со мной:\n"
        "https://t.me/your_username\n\n"
        "Актуальный курс: проверьте командой /rates"
    )
    
    if isinstance(event, CallbackQuery):
        await event.message.edit_text(text, reply_markup=get_main_keyboard())
        await event.answer()
    else:
        await event.answer(text, reply_markup=get_main_keyboard())
