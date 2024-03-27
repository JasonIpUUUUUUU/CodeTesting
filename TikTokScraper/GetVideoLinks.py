from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

chrome_options = Options()
chrome_options.add_argument("--incognito")
linksFile = 'Links.txt'

driver = webdriver.Chrome(options=chrome_options)

repeatTimes = 3

for i in range(repeatTimes):
    driver.get("https://www.xiaohongshu.com/explore?channel_id=homefeed.fashion_v3")

    wait = WebDriverWait(driver, 20)
    time.sleep(1)
    elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.cover.ld.mask")))

    action = ActionChains(driver)
    action.move_by_offset(100, 100).click().perform()
    
    with open(linksFile, 'a') as file:
        for element in elements:
            href = element.get_attribute("href")
            if href:
                file.write(href + '\n')
driver.quit()

