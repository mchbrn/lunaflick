import os
import requests
from PIL import Image 
from io import BytesIO 

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def apply_fx(fx, dir_unproc, dir_proc):
    driver = webdriver.Firefox()
    driver.get("https://www2.lunapic.com/editor/?action=" + fx)

    # consent to cookies
    try:
        WebDriverWait(driver, 200).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".fc-cta-consent"))
                )
    finally:
        driver.find_element(By.CSS_SELECTOR, ".fc-cta-consent").click()

    current = ""

    for file in sorted(os.listdir(dir_unproc)):
        current = file

        path = os.path.join(dir_unproc, file)
        if os.path.isfile(path):
            driver.find_element(By.NAME, "upload-image").send_keys(path)

            # save processed img
            try:
                element_found = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "#myimagee"))
                        )
            finally:
                if element_found:
                    print("element found")
                else:
                    print("no element")

                src = driver.find_element(By.CSS_SELECTOR, "#myimage").get_attribute("src")
                req = requests.get(src)

                img = Image.open(BytesIO(req.content))
                img.save(dir_proc + file)

            # close img
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + "x") 

            # confirm clos img
            try:
                WebDriverWait(driver, 200).until(
                        EC.presence_of_element_located((By.XPATH, "/html/body/div/div[13]/div/center/form/table[1]/tbody/tr/td[1]/b/b/input"))
                        )
            finally:
                driver.find_element(By.XPATH, "/html/body/div/div[13]/div/center/form/table[1]/tbody/tr/td[1]/b/b/input").click()


        driver.get("https://www2.lunapic.com/editor/?action=" + fx)

    driver.close()
