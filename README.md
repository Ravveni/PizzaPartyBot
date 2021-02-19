# Pizza Party Bot

Automated bot constructed to play [Pizza Party on MiniGames.com](https://www.minigames.com/games/pizza-party). 

Powered primarily through `pyautogui` for image recognition and GUI control.
#

## Bot Capabilities
- Opens browser to game
- Scrolls so that game is in view
- Navigates through menus and description screens
- Plays through all levels

## TODO
- [x] Add additional level compatibility
- [x] Cache ingredientLocations dictionary to add to instead of reinitializing
- [ ] Requirements.txt for pip installation of dependencies
- [ ] Setup script for venv creation and dependency download
- [ ] Alleviate bottleneck on `PizzaPartyBot.py ln. 64`
- [ ] Historical database for amount of each pizza per level
