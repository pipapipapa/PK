from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from kitties import ImageSearch


def driver_prep():
    driver = webdriver.Chrome()
    driver.get("https://vk.com/im?sel=c37")

    sleep(15)
    driver.get("https://vk.com/im?sel=c37")
    sleep(30)

    html = driver.find_element(By.TAG_NAME, 'html')

    SCROLL_PAUSE_TIME = 2

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        html.send_keys(Keys.HOME)
        sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    return driver


def extract_image_urls(driver):
    image_urls = []
    pics = driver.find_elements(By.CSS_SELECTOR, '[aria-label="фотография"]')
    for pic in pics:
        junk = pic.get_attribute('onclick')
        if junk:
            junk = junk[junk.find('http'):]
            junk = junk[:junk.find('"')]
            junk = junk.replace('\\/', '/')
            image_urls.append(junk)
    return image_urls


driver = driver_prep()
image_urls = extract_image_urls(driver)

print(image_urls)

for e in image_urls:
    I = ImageSearch()
    I.add_to_db(e)
