![Guess the Number Telegram Bot](https://habrastorage.org/webt/qb/8s/gu/qb8sgups0owfqkrggy7_9el-zu4.png)

# Guess the Number Telegram Bot
[t.me/tg_guess_the_number_bot](t.me/tg_guess_the_number_bot)

Telegram bot playing "Guess the number" game.

Bot thinks of a number from one to the number you choose. You can try to guess it. Bot informs if the number is less or more than the hidden one.

### Requrements
Python **3.7+**
```
$ pip install aiogram
```

### Setup
* Set environment variable TOKEN with your Telegram API Token value **OR**
* Set your Telegram API Token as variable value: ```bot = Bot(token='TELEGRAM_API_TOKEN_HERE')``` (**bot.py**, *line 10*)
* Execute **bot.py**
### Commands
* /help — about the bot
* /start — start the game
* /cancel — stop the game
