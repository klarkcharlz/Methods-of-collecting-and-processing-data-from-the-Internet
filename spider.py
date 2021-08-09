import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)

driver.get('https://mail.ru/')

login = "study.ai_172@mail.ru"
password = "NextPassword172!?"

# from
# date
# title
# text

