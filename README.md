# Anketa Bot

Anketa Bot is a Telegram bot that allows users to fill out a questionnaire and store their data in a database. The bot is built using the aiogram library and SQLAlchemy ORM.

## Features

- User questionnaire with multiple questions
- Data storage in a SQLite database using SQLAlchemy ORM
- Notification of admins when a new questionnaire is submitted or edited
- Throttling middleware to prevent spamming
- Logging of errors to a file

## Installation

1. Clone the repository:

```
git clone https://github.com/potatoenergy/Anketa_bot.git
```

2. Install the required dependencies:

```
apt update
apt upgrade -y
apt install virtualenv python3 python3-venv python3-virtualenv python3-pip -y
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

3. Create a `.env` file with the following variables:

```
BOT_TOKEN=<your_bot_token>
ADMINS=<admin_user_id_1>,<admin_user_id_2>,...
```

4. Run the bot:

```
python3 app.py
```

## Usage

The bot has a single command: `/start`. When a user sends this command, the bot will greet them and display a menu with the option to fill out the questionnaire.

When a user fills out the questionnaire, their data is stored in a SQLite database. If the user has already filled out the questionnaire, they will be asked if they want to fill it out again.

Admins will receive a notification when a new questionnaire is submitted or edited.

## Customization

To add new questions to the questionnaire, follow these steps:

1. Add a new state to the `states/data_collection.py` file:

```python
class Form(StatesGroup):
    ...
    act_new_question = State()
```

2. Add a new query to the `models.py` file:

```python
class People(Base):
    ...
    act_new_question = Column(String, nullable=True, default=None)
```

3. Add a new message handler to the `handlers/menu.py` file:

```python
@dp.message(data_collection.Form.act_new_question)
async def process_new_question(message: types.Message, state: FSMContext):
    await state.update_data(act_new_question=message.text)
    # Add code to handle the user's response to the new question
```

3. Update the `process_skills` function in the `handlers/menu.py` file to save the user's response to the new question to the database and include it in the notification message to admins.

## Credits

This bot was created by [ChebupelAnfica](https://github.com/ChebupelAnfica) and edited by [Ponfertato](https://github.com/ponfertato) for the [Potato Energy](https://github.com/potatoenergy) project.