# Pizza Party Bot

Automated bot constructed to play [Pizza Party on MiniGames.com](https://www.minigames.com/games/pizza-party). 

Powered primarily through `pyautogui` for image recognition and GUI control.
#

## Bot Capabilities
- Opens browser to game
- Scrolls so that game is in view
- Navigates through menus and description screens
- Plays through all levels perfectly
- Closes browser and shuts itself down

## Requirements
- Firefox web browser
- Python 3.4-3.9
- Mac Retina display (Points v. pixel calculation difference, can probably remove the `/ 2` after move calculations for other screens, but that is untested at the moment)
- A powerful enough machine to have multithreaded image recognition
- [Follow setup docs](https://github.com/Ravveni/PizzaPartyBot/blob/main/Setup.md)

### TODO
- [x] Add additional level compatibility
- [x] Cache ingredientLocations dictionary to add to instead of reinitializing
- [x] Requirements.txt for pip installation of dependencies
- [x] Alleviate bottleneck for pizza image recognition
- [ ] Historical database for amount of each pizza per level
- [ ] Finish setup documentation for Mac
