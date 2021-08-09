from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep


login = "study.ai_172"
password = "NextPassword172!?"

chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)

driver.get('https://mail.ru/')

# вводим логин
mail_name = driver.find_element_by_class_name('email-input')
mail_name.click()
mail_name.send_keys(login)
sleep(1)
to_pass = driver.find_elements_by_css_selector('button[data-testid="enter-password"]')[0]
to_pass.click()

# вводим пароль
mail_pass = driver.find_element_by_class_name('password-input')
mail_pass.send_keys(password)
to_auth = driver.find_elements_by_css_selector('button[data-testid="login-to-mail"]')[0]
to_auth.click()
sleep(1)


letter = driver.find_elements_by_class_name('js-letter-list-item')
was_letter = None
# пролистываем всю почту
while letter != was_letter:
    actions = ActionChains(driver)
    actions.move_to_element(letter[-1])
    actions.perform()
    was_letter = letter
    letter = driver.find_elements_by_class_name('js-letter-list-item')

print("ВСЁ")
