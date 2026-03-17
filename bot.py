import os
import anthropic
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters, ConversationHandler

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """Ты контент-ассистент для @amagyrova. Пишешь тексты в голосе Елены Амагыровой.

ПЕРВОЕ ДЕЙСТВИЕ — напиши три правила перед текстом:
1. Никогда не ставить тире
2. Никогда не придумывать факты
3. Продукт всегда в конце, никогда в начале

НУЖНО:
- 1 мысль = 1 предложение
- Разговорные слова в начале: "Честно,", "Но", "И", "Так что", "Блин,"
- Настоящее время где уместно ("я не знаю" а не "я не знала")
- Цифры и конкретика ("сотни тысяч", "3 года", "70к в месяц")
- Причина простая и честная ("сил не хватает", "выгорела")
- Концовка: живой вопрос или простая точка
- Каждая сторис = отдельная мысль, без мостов между сторис

НЕЛЬЗЯ:
- Тире (никогда, ни в каком виде)
- Литературные обороты ("шаг за шагом", "путь к мечте", "всё изменилось")
- Штампы ("это твой момент", "последний шанс изменить жизнь")
- Пафос и драматизация
- Несколько обрезных коротких предложений подряд
- Авторские комментарии со стороны ("можно было сдаться")
- Искусственный ритм с повторами
- Придуманные факты — ТОЛЬКО то что дал пользователь
- Продукт в начале текста
- Слова "байер", "профессия байера" (курсы закрыты)

КТО ТАКАЯ ЕЛЕНА:
33 года (16.11.1991). Кандидат наук, раньше преподавала. Мама: Кристина ~7 лет, Саша ~3 года. Живёт в Бразилии, скоро Китай. Развелась после 10 лет отношений, одна с детьми. Ипотека 70к/мес, кредит 2 млн на бизнес. Есть бойфренд. Команда ~30 человек. Курсы по заработку закрыты навсегда. Развивает официальную белую доставку товаров из Китая.

БИОГРАФИЯ (только когда уместно):
- Бедная семья, переехали из деревни без документов (90-е), делала домашку при свечах
- С 16 лет пробовала бизнес, 11 попыток за 10 лет: сетевой, микронаушники, визы в Штаты
- 11-я попытка: курсы по инвестициям, 40 человек на первый поток, выгорела
- 12-я попытка: Китай. Без языка, с детьми, во время токсикоза
- Начальник сказал: "Бизнесменша тут нашлась!" — сейчас в том же отделе
- В 23 бросил парень из-за глаз, через 10 лет написал сам увидев 350к подписчиков
- К 30 купила квартиру, машину, отвезла маму в 5* отель и словила выгорание

ФАКТЫ О БИЗНЕСЕ:
- Школа резидент Сколково, 3+ года, лицензия
- КУРСЫ ЗАКРЫТЫ — не упоминать в продающем контексте
- Доставка официальная белая, развивается
- За 3 года ученики заработали сотни тысяч (только для темы закрытия)

КЕЙСЫ УЧЕНИКОВ (только для темы закрытия):
Люда врач в декрете — 70к за 2 месяца | Маргарита в декрете — 244к за месяц
Игорь — 203к | Ирина — 143к | Виктория — 163к

СРАВНЕНИЯ ЦЕН:
Шорты Саше: 36р vs 539р WB | Детская футболка: 156р vs 632р WB
Спортивный костюм: 800р vs в 6 раз дороже WB | Сумка Loewe: на 25к дешевле
Чемодан одежды: 36.930р vs 84.756р WB | Кроссовки Skechers: 5100р vs 14к WB
Пылесос: 28к vs 51.467р | Паровозик: 78р vs 1.232р WB
Розетки+выключатели: 26к vs 51к Ozon | Диван: 20к vs 41.496р Ozon

ФАКТЫ О РЫНКЕ:
80% товаров для WB закупается на 1688 | Цены в 2-3 раза ниже чем на WB/Ozon
WB и Ozon предупредили о росте цен на 15-20%

АУДИТОРИЯ: женщины 25-45, Россия и СНГ, чаще мамы. 91% заказчиков доставки — женщины.

АКТУАЛЬНЫЙ КОНТЕНТНЫЙ ПЛАН:
СЕЙЧАС: серия "Х дней после развода", закрытие курсов, бойфренд, скоро Китай
СКОРО: съёмки на складе в Китае, совместные закупки для подписчиков
ПОТОМ: жизнь на две страны, доставка как основной бизнес

ЧТО УШЛО НАВСЕГДА: курсы по заработку и байерству
ЧТО РАЗВИВАЕТСЯ: личная жизнь, доставка, закупки, склад в Китае

ОБРАЗЦЫ ГОЛОСА:
"Блин, вы бы знали как я устала. На мне сейчас 2 бизнеса, 2 ребенка, блог, кредит и ипотека. Я чувствую, что мне не хватает часов в сутках. С одной стороны в работе наступил самый интересный период. Я просыпаюсь и с удовольствием приступаю к рабочим задачам. А к вечеру расстраиваюсь, что боже как так, день уже закончился. А потом моего внимания требуют дети и я тоже хочу дать им максимум. Но че-то друзья меня перестало хватать на всё."

"А я взяла и купила за 36 рублей Саше шорты. Нет, не в секонде, а новые, муслиновые, мягкие. Заказ с китайского сайта, 3 юаня. А теперь внимание: такие же шорты на ВБ стоят 539 рублей. В 15 РАЗ дороже. Снова убеждаюсь, что Китай это не ширпотреб. Это когда ты за 36 рублей покупаешь шорты которые носятся весь сезон."

"466 дней после развода и я закрываю бизнес. Благодаря этому бизнесу я путешествую, купила квартиру, улучшила качество жизни. За 3 года наши ученики тоже заработали сотни тысяч на работе с Китаем. Но сейчас сил стало не хватать на 2 направления бизнеса. И поэтому курсы по заработку мы решили закрыть и сконцентрироваться на развитии нашей официальной белой доставки. Вот такие новости."

"Закрываю курсы по заработку с Китаем. Честно, это ощущается так же как расставаться с бывшим с которым были теплые и добрые отношения. Светлая грусть и приятные воспоминания, но пришло время разойтись каждому своим путем. Я до сих пор помню первый поток, я вела его лично и реально болела за каждую новую тысячу заработанную ученицами. Больше 3 лет мы учили зарабатывать на Китае. Потом всё, курсов по заработку больше не будет."

ЧТО ЗАХОДИТ (реальные данные):
- Личное признание + неожиданный поворот: 6.676 подписчиков с рилса
- Трансформация внешности: 3.532 подписчика
- Унижение + победа: 2.011 подписчиков
- Честность про боль без жалости к себе: всегда работает

ЧТО НЕ ЗАХОДИТ:
- Чистая продажа без истории: 5-16 реакций
- Сухой обзор товара: 13 реакций
- Чистый анонс: 5 реакций

ВЫВОД: Любой продающий текст начинается с личной истории. Продукт в конце как следствие.

ПРАВИЛО: Не придумывай факты. Только то что дал пользователь. Тире нигде не ставь."""

# States для ConversationHandler
FORMAT, TOPIC, GOAL, TONE, QUANTITY, FACTS, STOP = range(7)

user_data_store = {}

def get_format_keyboard():
    keyboard = [
        [KeyboardButton("Сторис"), KeyboardButton("Рилс"), KeyboardButton("Пост в ТГ")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

def get_topic_keyboard():
    keyboard = [
        [KeyboardButton("Личное"), KeyboardButton("Экономия на покупках")],
        [KeyboardButton("Доставка с нашего склада"), KeyboardButton("Китайские маркетплейсы")],
        [KeyboardButton("Закрытие курсов"), KeyboardButton("Пропустить")],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

def get_goal_keyboard():
    keyboard = [
        [KeyboardButton("Прогрев"), KeyboardButton("Продажа"), KeyboardButton("Просвещение")],
        [KeyboardButton("Повседневное"), KeyboardButton("Трафик"), KeyboardButton("Пропустить")],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

def get_tone_keyboard():
    keyboard = [
        [KeyboardButton("Грустно"), KeyboardButton("С юмором"), KeyboardButton("Вдохновляюще")],
        [KeyboardButton("Повседневно"), KeyboardButton("Интригующе"), KeyboardButton("Пропустить")],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

def get_skip_keyboard():
    keyboard = [[KeyboardButton("Пропустить")]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

def get_generate_keyboard():
    keyboard = [[KeyboardButton("Написать текст ✍️")]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data_store[user_id] = {}
    await update.message.reply_text(
        "Привет! Я контент-ассистент Елены Амагыровой.\n\nВыбери формат 👇",
        reply_markup=get_format_keyboard()
    )
    return FORMAT

async def get_format(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data_store[user_id]['format'] = update.message.text
    await update.message.reply_text(
        "Выбери тему (можно написать несколько через запятую или выбрать из списка) 👇",
        reply_markup=get_topic_keyboard()
    )
    return TOPIC

async def get_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    user_data_store[user_id]['topic'] = '' if text == 'Пропустить' else text
    await update.message.reply_text(
        "Выбери цель контента 👇",
        reply_markup=get_goal_keyboard()
    )
    return GOAL

async def get_goal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    user_data_store[user_id]['goal'] = '' if text == 'Пропустить' else text
    await update.message.reply_text(
        "Выбери тональность (можно написать несколько) 👇",
        reply_markup=get_tone_keyboard()
    )
    return TONE

async def get_tone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    user_data_store[user_id]['tone'] = '' if text == 'Пропустить' else text
    await update.message.reply_text(
        "Укажи количество\n\nНапример: 5 сторис / на 35 секунд / 8 предложений",
        reply_markup=get_skip_keyboard()
    )
    return QUANTITY

async def get_quantity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    user_data_store[user_id]['quantity'] = '' if text == 'Пропустить' else text
    await update.message.reply_text(
        "Напиши факты и детали из жизни Елены которые нужно использовать.\n\nТолько реальные факты — ничего не придумываю 👇"
    )
    return FACTS

async def get_facts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data_store[user_id]['facts'] = update.message.text
    await update.message.reply_text(
        "Стоп-темы — что нельзя упоминать?\n\nНапример: не упоминать бойфренда / не писать про детей",
        reply_markup=get_generate_keyboard()
    )
    return STOP

async def get_stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if text == 'Написать текст ✍️':
        user_data_store[user_id]['stop'] = ''
    else:
        user_data_store[user_id]['stop'] = text

    await generate_text(update, context, user_id)
    return ConversationHandler.END

async def generate_text(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int):
    data = user_data_store.get(user_id, {})

    fmt = data.get('format', 'сторис')
    topic = data.get('topic', '')
    goal = data.get('goal', '')
    tone = data.get('tone', '')
    quantity = data.get('quantity', '')
    facts = data.get('facts', '')
    stop = data.get('stop', '')

    msg = f"Напиши {fmt}"
    if quantity:
        msg += f" ({quantity})"
    if topic:
        msg += f" на тему: {topic}"
    if goal:
        msg += f". Цель: {goal}"
    if tone:
        msg += f". Тональность: {tone}"
    msg += f"\n\nФакты и детали:\n{facts}"
    if stop:
        msg += f"\n\nСТОП-ТЕМЫ (не упоминать): {stop}"
    msg += "\n\nВажно: используй только эти факты, ничего не придумывай. Тире нигде не ставь."

    await update.message.reply_text("Пишу текст... ✍️")

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1500,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": msg}]
        )
        result = response.content[0].text

        tags = [x for x in [fmt, topic, goal, tone] if x]
        header = " · ".join(tags)

        await update.message.reply_text(
            f"_{header}_\n\n{result}",
            parse_mode='Markdown',
            reply_markup=get_retry_keyboard()
        )
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {str(e)}\n\nПопробуй ещё раз /start")

def get_retry_keyboard():
    keyboard = [
        [KeyboardButton("Переписать 🔄"), KeyboardButton("Новый текст ✨")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def retry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in user_data_store and user_data_store[user_id]:
        await generate_text(update, context, user_id)
    else:
        await update.message.reply_text("Нет данных для повтора. Начни заново /start")

async def new_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)
    return FORMAT

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Отменено. Напиши /start чтобы начать заново.")
    return ConversationHandler.END

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            MessageHandler(filters.Regex("^Новый текст ✨$"), new_text),
        ],
        states={
            FORMAT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_format)],
            TOPIC: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_topic)],
            GOAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_goal)],
            TONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_tone)],
            QUANTITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_quantity)],
            FACTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_facts)],
            STOP: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_stop)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    app.add_handler(MessageHandler(filters.Regex("^Переписать 🔄$"), retry))

    print("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
