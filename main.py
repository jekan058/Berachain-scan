from logging_and_ascii import log_scanning, print_ascii_art
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import time

options = Options()
options.headless = True

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def get_transaction_count(address):
    url = f"https://artio.beratrail.io/address/{address}"
    driver.get(url)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.badge.badge-pill.badge-secondary"))
        )
        time.sleep(2)
        transaction_count_element = driver.find_element(By.CSS_SELECTOR, "span.badge.badge-pill.badge-secondary")
        return transaction_count_element.text.strip()
    except Exception as e:
        print(e)
        return "Element not found or error"

print_ascii_art()

with open('Address.txt', 'r') as file:
    addresses = file.read().splitlines()

transactions = []
for address in addresses:
    log_scanning(address)
    transaction = get_transaction_count(address)
    transactions.append(transaction)

driver.implicitly_wait(3)
driver.quit()

df = pd.DataFrame(list(zip(addresses, transactions)), columns=["Address", "Transactions"])
df.to_excel('transactions.xlsx', index=False)