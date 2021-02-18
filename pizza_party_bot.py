import cv2
import pyautogui
import re
from pyscreeze import Point
from selenium import webdriver
import sys
import time

confidence = 0.85
orderRegex = re.compile(r'Images/(.*)_pizza.png')
potentialOrders = ['Images/margherita_pizza.png', 'Images/marinara_pizza.png']

class PizzaPartyBot():
    ingredientLocations = None
    isNextLevel = False

# Startup

    def openBrowserAndStartGame(self):
        print('\nInitializing bot...\n')
        browser = webdriver.Firefox()
        browser.get('https://www.minigames.com/games/pizza-party')
        pyautogui.click(600, 200)
        pyautogui.scroll(-22)

        self.go()
        time.sleep(1)
        self.start()
        self.description()
        self.continueToNextLevel()

    def start(self):
        self.clickButton('Images/start_button.png', needed=True)

    def go(self):
        self.clickButton('Images/go_button.png', needed=True)

    def description(self):
        self.clickButton('Images/description.png', needed=True)

# Navigation

    def continueToNextLevel(self):
        self.isNextLevel = True
        self.clickButton('Images/continue_button.png', needed=True)

# Order creation

    def getNewOrder(self) -> str:
        print('Getting new order...')

        for orderName in potentialOrders:
            order = pyautogui.locateCenterOnScreen(orderName, confidence=confidence)
            if order == None:
                continue
            else:
                purgedOrderName = orderRegex.findall(orderName)
                if purgedOrderName != []:
                    return purgedOrderName[0]

        return None

    def prepareNewOrder(self, order):
        print('Starting the %s pizza...' % order)
        ingredients = self.getIngredientsForOrder(order)

        for ingredient in ingredients:
            pyautogui.click(ingredient.x / 2, ingredient.y / 2)

        print('The %s pizza is finished...\n' % order)
        time.sleep(2.5)

    def getIngredientsForOrder(self, order) -> list:
        if self.ingredientLocations == None or self.isNextLevel:
            self.getIngredientLocations()

        ingredients = []

        if order == 'margherita':
            ingredients.append(self.ingredientLocations['tomato'])
            ingredients.append(self.ingredientLocations['mozzarella'])
            ingredients.append(self.ingredientLocations['basil'])
            ingredients.append(self.ingredientLocations['oven'])
        elif order == 'marinara':
            ingredients.append(self.ingredientLocations['tomato'])
            ingredients.append(self.ingredientLocations['oregano'])
            ingredients.append(self.ingredientLocations['oven'])

        return ingredients

    def getIngredientLocations(self):
        locations = {}

        locations['tomato'] = self.getIngredientLocation('Images/tomato.png')
        locations['mozzarella'] = self.getIngredientLocation('Images/mozzarella.png')
        locations['basil'] = self.getIngredientLocation('Images/basil.png')
        locations['oregano'] = self.getIngredientLocation('Images/oregano.png')
        locations['oven'] = self.getIngredientLocation('Images/oven_button.png')

        self.isNextLevel = False
        self.ingredientLocations = locations

    def getIngredientLocation(self, ingredient) -> Point:
        location = pyautogui.locateCenterOnScreen(ingredient, confidence=confidence)
        if location != None:
            return location

# Utility methods

    def clickButton(self, button, needed=False, checkInterval=1):
        if needed:
            self.waitForButtonToClick(button, checkInterval)
        else:
            self.clickButtonIfExists(button)

    def clickButtonIfExists(self, buttonName):
        button = pyautogui.locateCenterOnScreen(buttonName, confidence=confidence)

        if button == None:
            return
        else:
            pyautogui.moveTo(button.x / 2, button.y / 2, duration=0.25)
            pyautogui.click(button.x / 2, button.y / 2)

    def waitForButtonToClick(self, buttonName, checkInterval):
        waiting = True

        while waiting:
            button = pyautogui.locateCenterOnScreen(buttonName, confidence=confidence)
            if button == None:
                time.sleep(checkInterval)
            else:
                pyautogui.moveTo(button.x / 2, button.y / 2, duration=0.25)
                pyautogui.click(button.x / 2, button.y / 2)
                waiting = False

def main():
    app = PizzaPartyBot()
    app.openBrowserAndStartGame()

    time.sleep(2) # Wait for first customer

    while True:
        order = app.getNewOrder()

        if order == None:
            print('\nNo next order, reached next level\n')
            # app.continueToNextLevel()
            sys.exit(1)
        else:
            app.prepareNewOrder(order)

if __name__ == '__main__':
    main()
