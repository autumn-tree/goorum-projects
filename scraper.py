from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def scrape(url):
    driver = webdriver.Chrome()
    driver.get(url)

    time.sleep(5)  # allow dynamic content to load

    elements = driver.find_elements(By.TAG_NAME, "h3")

    count = 0
    for e in elements:
        text = e.text.strip()
        if text:
            print(text)
            count += 1
        if count == 10:
            break

    driver.quit()

if __name__ == "__main__":
    url = "https://naver.com"
    scrape(url)