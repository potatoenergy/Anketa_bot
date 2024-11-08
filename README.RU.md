# Анкета Бот

Анкета Бот - это Telegram бот, который позволяет пользователям заполнять анкету и сохранять свои данные в базе данных. Бот построен с использованием библиотеки aiogram и ORM SQLAlchemy.

## Функции

- Анкета пользователя с несколькими вопросами
- Хранение данных в SQLite базе данных с использованием ORM SQLAlchemy
- Уведомление администраторов при отправке новой анкеты или ее редактировании
- Middleware для ограничения частоты запросов, чтобы предотвратить спам
- Логирование ошибок в файл

## Установка

1. Клонируйте репозиторий:

```
git clone https://github.com/potatoenergy/Anketa_bot.git
```

2. Установите необходимые зависимости:

```
apt update
apt upgrade -y
apt install virtualenv python3 python3-venv python3-virtualenv python3-pip -y
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

3. Создайте файл `.env` со следующими переменными:

```
BOT_TOKEN=<ваш_токен_бота>
ADMINS=<id_пользователя_администратора_1>,<id_пользователя_администратора_2>,...
```

4. Запустите бота:

```
python3 app.py
```

## Использование

Бот имеет одну команду: `/start`. Когда пользователь отправляет эту команду, бот приветствует его и отображает меню с опцией заполнения анкеты.

Когда пользователь заполняет анкету, его данные сохраняются в SQLite базе данных. Если пользователь уже заполнял анкету, ему будет предложено заполнить ее снова.

Администраторы получают уведомление при отправке новой анкеты или ее редактировании.

## Настройка

Чтобы добавить новые вопросы в анкету, выполните следующие действия:

1. Добавьте новое состояние в файл `states/data_collection.py`:

```python
class Form(StatesGroup):
    ...
    act_new_question = State()
```

2. Добавьте новый запрос в файл `states/data_collection.py`:

```python
class People(Base):
    ...
    act_new_question = Column(String, nullable=True, default=None)
```

3. Добавьте новый обработчик сообщений в файл `handlers/menu.py`:

```python
@dp.message(data_collection.Form.act_new_question)
async def process_new_question(message: types.Message, state: FSMContext):
    await state.update_data(act_new_question=message.text)
    # Добавьте код для обработки ответа пользователя на новый вопрос
```

4. Обновите функцию `save_data_and_notify_admins` в файле `handlers/menu.py`, чтобы сохранить ответ пользователя на новый вопрос в базе данных и включить его в сообщение уведомления администраторам.

## Авторство

Этот бот был создан [ChebupelAnfica](https://github.com/ChebupelAnfica) и отредактирован [Ponfertato](https://github.com/ponfertato) для проекта [Potato Energy](https://github.com/potatoenergy).