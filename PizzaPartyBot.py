import cv2
import pyautogui
import re
from pyscreeze import Point
from selenium import webdriver
import sys
import time

aiDelay = 0.75
adDelay = 2.0
confidence = 0.9
customerDelay = 2.5
ingredientRegex = re.compile(r'Assets/Ingredients/(.*).png')
maxLevel = 6
orderRegex = re.compile(r'Assets/Pizzas/(.*)_pizza.png')
potentialOrders = ['Assets/Pizzas/margherita_pizza.png', 'Assets/Pizzas/marinara_pizza.png', 
                    'Assets/Pizzas/ham_artichoke_pizza.png', 'Assets/Pizzas/ham_mushroom_pizza.png',
                    'Assets/Pizzas/pepperoni_pizza.png', 'Assets/Pizzas/pepperoni_mushroom_pizza.png']

class PizzaPartyBot():
    browser = None
    currentLevel = 1
    ingredientLocations = {}
    isNextLevel = False

# Startup & Destruction
    def openBrowserAndStartGame(self):
        print('\nInitializing bot...\n')
        self.browser = webdriver.Firefox()
        self.browser.get('https://www.minigames.com/games/pizza-party')
        # pyautogui.click(600, 200)
        pyautogui.scroll(-22)

        self.go()
        self.start()
        self.description()
        self.continueToFirstLevel()

    def selfDestruct(self):
        print('\nI have won, mortal...\n')
        time.sleep(aiDelay)
        print('\nSelf destruct in 5...')
        for i in range(4, 0, -1):
            time.sleep(aiDelay)
            print('\n%s...' % i)
        time.sleep(aiDelay * 2)
        print('\nGoodnight...\n')
        time.sleep(aiDelay * 2)
        self.browser.close()
        sys.exit(1)

# Navigation
    def go(self):
        self.clickButton('Assets/Buttons/go_button.png', needed=True)

    def start(self):
        self.clickButton('Assets/Buttons/start_button.png', needed=True)

    def description(self):
        self.clickButton('Assets/Buttons/description_button.png', needed=True)

    def continueToFirstLevel(self):
        self.isNextLevel = True
        self.clickButton('Assets/Buttons/continue_button.png', needed=True)

    def continueToNextLevel(self):
        self.currentLevel += 1
        self.isNextLevel = True

        if self.currentLevel != maxLevel:
            self.clickButton('Assets/Buttons/next_level_button.png', needed=True)
        else:
            self.selfDestruct()

        print('\nStarting level %s...\n' % self.currentLevel)
        time.sleep(customerDelay) # Wait for first customer of upcoming level

# Order creation
    def getNewOrder(self) -> str:
        print('Getting new order...')

        # TODO: Improve bottleneck
        for orderName in potentialOrders:
            order = pyautogui.locateCenterOnScreen(orderName, confidence=confidence)

            if order == None:
                continue
            else:
                purgedOrderName = orderRegex.findall(orderName)
                if purgedOrderName[0] != None:
                    return purgedOrderName[0]

        print('\nNo new order...\n')
        return None

    def prepareNewOrder(self, order):
        print('Starting the %s pizza...' % order)
        ingredients = self.getIngredientsForOrder(order)

        for ingredient in ingredients:
            pyautogui.click(ingredient.x / 2, ingredient.y / 2) # Macs use points and have to be divided by 2

        print('Finished the %s pizza...\n' % order)
        time.sleep(customerDelay) # Wait for next customer

# Ingredient management
    def getIngredientsForOrder(self, order) -> list:
        if self.isNextLevel:
            self.getIngredientLocations()
            self.isNextLevel = False

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
        elif order == 'ham_artichoke':
            ingredients.append(self.ingredientLocations['tomato'])
            ingredients.append(self.ingredientLocations['mozzarella'])
            ingredients.append(self.ingredientLocations['ham'])
            ingredients.append(self.ingredientLocations['artichoke'])
            ingredients.append(self.ingredientLocations['oven'])
        elif order == 'ham_mushroom':
            ingredients.append(self.ingredientLocations['mozzarella'])
            ingredients.append(self.ingredientLocations['ham'])
            ingredients.append(self.ingredientLocations['mushrooms'])
            ingredients.append(self.ingredientLocations['oven'])
        elif order == 'pepperoni':
            ingredients.append(self.ingredientLocations['tomato'])
            ingredients.append(self.ingredientLocations['mozzarella'])
            ingredients.append(self.ingredientLocations['basil'])
            ingredients.append(self.ingredientLocations['pepperoni'])
            ingredients.append(self.ingredientLocations['oven'])
        elif order == 'pepperoni_mushroom':
            ingredients.append(self.ingredientLocations['tomato'])
            ingredients.append(self.ingredientLocations['mozzarella'])
            ingredients.append(self.ingredientLocations['pepperoni'])
            ingredients.append(self.ingredientLocations['mushrooms'])
            ingredients.append(self.ingredientLocations['oven'])

        return ingredients

    def getIngredientLocations(self):
        print('Updating ingredient location coordinates...')
        locations = self.ingredientLocations

        if self.currentLevel == 1:
            locations['oven'] = self.getIngredientLocation('Assets/Ingredients/oven_button.png')
            locations['tomato'] = self.getIngredientLocation('Assets/Ingredients/tomato.png')
            locations['mozzarella'] = self.getIngredientLocation('Assets/Ingredients/mozzarella.png')
            locations['basil'] = self.getIngredientLocation('Assets/Ingredients/basil.png')
            locations['oregano'] = self.getIngredientLocation('Assets/Ingredients/oregano.png')

        if self.currentLevel == 2:
            locations['ham'] = self.getIngredientLocation('Assets/Ingredients/ham.png')
            locations['artichoke'] = self.getIngredientLocation('Assets/Ingredients/artichoke.png')

        if self.currentLevel == 3:
            locations['mushrooms'] = self.getIngredientLocation('Assets/Ingredients/mushrooms.png')

        if self.currentLevel == 4:
            locations['pepperoni'] = self.getIngredientLocation('Assets/Ingredients/pepperoni.png')

        self.ingredientLocations = locations

    def getIngredientLocation(self, ingredient) -> Point:
        purgedIngredientName = ingredientRegex.findall(ingredient)

        if purgedIngredientName[0] != None:
            print('Added coordinates for %s to dictionary...' % purgedIngredientName[0])

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
            # Macs use points and have to be divided by 2
            pyautogui.moveTo(button.x / 2, button.y / 2, duration=0.25)
            pyautogui.click(button.x / 2, button.y / 2) 

    def waitForButtonToClick(self, buttonName, checkInterval):
        waiting = True

        while waiting:
            button = pyautogui.locateCenterOnScreen(buttonName, confidence=confidence)

            if button == None:
                time.sleep(checkInterval)
            else:
                # Macs use points and have to be divided by 2
                pyautogui.moveTo(button.x / 2, button.y / 2, duration=0.25)
                pyautogui.click(button.x / 2, button.y / 2)
                waiting = False

def main():
    app = PizzaPartyBot()
    app.openBrowserAndStartGame()

    time.sleep(customerDelay) # Wait for first customer of first level

    while True:
        order = app.getNewOrder()

        if order == None:
            app.continueToNextLevel()
        else:
            app.prepareNewOrder(order)

if __name__ == '__main__':
    main()
