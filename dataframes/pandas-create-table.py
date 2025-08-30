import random
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

user_agent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11.5; rv:90.0) Gecko/20100101 Firefox/90.0',
    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
]

data = []

# set url
url = 'https://theathletic.com/4214078/2023/02/22/nfl-rankings-offensive-line-depth-chart/'

# call open browser function
chrome_options = Options()
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.headless = True
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
userAgent = random.choice(user_agent_list)
chrome_options.add_argument(f'user-agent={userAgent}')
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
driver.get(url)

# login to website
sign_in_link = driver.	find_element(By.LINK_TEXT, ‘link_text’)
sign_in_link.click()

username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'Login')))
password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'Password')))
username.send_keys('your_username')
password.send_keys('your_password')

driver.	find_element(By.ID, "loginSubmit").click()
time.sleep(2)

innerHTML = driver.page_source
soup = BeautifulSoup(innerHTML, "html.parser")

# Find the table
table = soup.find("div", {"id": "tab_content_history"})
table = table.find("div", {"class": "tab__content__item"})
table_body = table.find('tbody')

rows = table_body.find_all('tr')

for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols])


df = pd.DataFrame(data[1:])
df.columns = ['Time', 'Type', 'Volume', 'Symbol', 'Price', 'Time', 'Price', 'Commission', 'Swap', 'Profit']
print(df)

driver.quit()
