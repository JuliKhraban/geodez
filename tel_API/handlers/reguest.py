import re
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common import NoSuchElementException, ElementNotInteractableException
from state.info import UserInfoState
from loader import bot
from telebot.types import Message
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

data_my_number ='500000000001002474'  """Для примера"""

def search_number(message:Message, number):
    chrome_options = Options()
    #chrome_options.page_load_strategy = 'normal'
    chrome_options.add_argument("--headless")
    browser = webdriver.Chrome(options=chrome_options)
    #browser.maximize_window()
    bot.set_state(message.from_user.id, UserInfoState.search_number, message.chat.id)

    browser.get('https://map.nca.by/search')
    search_input = browser.find_element(By.XPATH,'/html/body/div/div[1]/div/div/main/div/div[1]/header/div/form/div[1]/div[1]/div/div/div[1]/input')
    errors = [NoSuchElementException, ElementNotInteractableException]
    wait = WebDriverWait(browser, timeout=2, poll_frequency=.2, ignored_exceptions=errors)
    try:
        wait.until(lambda d: search_input.send_keys(number) or True)
        search_input_button = browser.find_element(By.XPATH, '/html/body/div/div[1]/div/div/main/div/div[1]/header/div/form/div[1]/button')
        wait.until(lambda d: search_input_button.click() or True)
        result = wait.until(lambda d: browser.find_element(By.XPATH, '/html/body/div/div[1]/div/div/main/div/span/div/aside/'
                                                                         'div[1]/div[2]/div[2]/div/div/div/div/div[2]/div/div/div/div/div[2]/div/div[1]/span/span[2]') or True )
        print(result.text)
        str = re.sub(r'', '', result.text)
        browser.close()
        return str
    except:
        return 'Не найден, так как не правильно указан кадастровый номер'






