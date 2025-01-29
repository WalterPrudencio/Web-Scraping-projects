from selenium import webdriver
import pandas as pd
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys

def get_data(product_url, path):
    service = Service(path)
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-notifications')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-browser-side-navigation')
    options.add_argument("--log-level=3")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument('--disable-webgl')
    options.add_argument('--disable-software-rasterizer')
    options.add_argument('--disable-3d-apis')

    driver = webdriver.Chrome(service = service, options = options)
    driver.get(product_url)
    review_list =[]

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='s0-1-26-7-18-4-18[0]-x-feedback-detail-list-13-tabs-0']")))
        proceses_if = driver.find_element(By.XPATH, "//div[@id='s0-1-26-7-18-4-18[0]-x-feedback-detail-list-13-tabs-0']")
        if proceses_if:
            WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.fdbk-detail-list__tabbed-btn"))
            fb_link = driver.find_element(By.CSS_SELECTOR, "a.fdbk-detail-list__tabbed-btn")
            comments_url = fb_link.get_attribute("href")
            driver.get(comments_url)
            
            while True:
                WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.fdbk-container")))
                reviews = driver.find_elements(By.CSS_SELECTOR, "li.fdbk-container")

                for review in reviews:
                    rev = review.find_element(By.CSS_SELECTOR, ".fdbk-container__details__comment span").text.strip()
                    if rev:
                        review_list.append({"Review": rev})

                try:
                    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//a[@aria-label='Next page']")))
                    next_page = driver.find_element(By.XPATH, "//a[@aria-label='Next page']")
                    if next_page.is_displayed() and next_page.is_enabled():
                        next_page.click()
                        time.sleep(0.6)
                    else:
                        break
                except:
                    break
    except:
        print("No hay commentarios sobre este producto")
        print("There are no reviews about this product")
        driver.quit()
        sys.exit(1)

    df = pd.DataFrame(review_list)
    driver.quit()
    return df
