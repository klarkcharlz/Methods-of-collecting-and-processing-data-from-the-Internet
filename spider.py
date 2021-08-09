from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

from time import sleep
from pprint import pprint


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
# иногда авторизация падает, не пойму из за чего ошибка, просто перезапустите скрипт
# тест ошибки "element not interactable", бывает 1 раз из 5 прмиерно
mail_pass = driver.find_element_by_class_name('password-input')
mail_pass.send_keys(password)
to_auth = driver.find_elements_by_css_selector('button[data-testid="login-to-mail"]')[0]
to_auth.click()
sleep(3)


# пролистываем всю почту и собираем ссылки
links = set()
letters = driver.find_elements_by_class_name('js-letter-list-item')
letter = letters[-1]
was_letter = None
while letter != was_letter:
    for letter in letters:
        links.add(letter.get_attribute("href"))
    actions = ActionChains(driver)
    actions.move_to_element(letter)
    actions.perform()
    was_letter = letter
    sleep(4)  # что бы письма успели появиться
    letters = driver.find_elements_by_class_name('js-letter-list-item')
    letter = letters[-1]

links = list(links)


# собираем данные
letter_data = []
for link in links:
    driver.get(link)
    # такая большая задержка потому что иногда страница загрузилась, а эллементы всеравно не появились
    # и программа падает
    sleep(4)
    try:
        date = driver.find_element_by_xpath("//div[@class='letter__date']").text
        from_ = driver.find_element_by_xpath("//span[@class='letter-contact']").get_attribute("title")
        title = driver.find_element_by_xpath("//h2[@class='thread__subject']").text
        text = driver.find_element_by_xpath("//div[@class='letter__body']").text
    except Exception as err:
        print(f"{type(err)}:\n{err}.")
    else:
        letter_data.append({
            'title': title,
            "from": from_,
            "date": date,
            "text": text
        })
