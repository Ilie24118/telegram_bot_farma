# telegram_bot_farma
This is a Telegram bot that fetches data from various pharmaceutical websites. It displays the availability of the product you have selected in your area. The main feature is the live notifications you receive when a new item is in stock. The data is presented in a list from the nearest to the farthest location based on your location.
# How to deploy?
Deploying is pretty much straight forward and is divided into several steps as follows:
## Installing requirements
- Clone this repo:
```
git clone https://github.com/Ilie24118/telegram_bot_farma/
cd telegram_bot_farma
```
- Install requirements
```
pip install requirements.txt
```
### Change the main.py and telegramBot.py files:
- Put your own latitude and longitude coordinates and change the web url in main.py
- Put your own token and user id in telegramBt.py file

# Notes
- This is a personal project for learning purposes
- At the moment it only gets data from Farmacia Famila website
