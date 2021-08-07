from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pymsgbox import *
import time
import os

PATH = os.getcwd() + "\webdriver\chromedriver.exe"

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(executable_path=PATH, options=options)

# driver = webdriver.Chrome(PATH)

def goto_twitch(username):
    wordcount = 0
    driver.get(f"https://dashboard.twitch.tv/u/{username}/settings/moderation/blocked-terms")
    logged_in = confirm(text=f"{username}, you will need to manually log into the Chrome window that just opened.", title='Confirm Login', buttons=['Logged in!', 'Get me outta here!'])
    
    if logged_in.lower() == 'logged in!':
        return add_words(wordcount)
    else:
        driver.quit()
        sys.exit()

def add_words(wordcount):
    search = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/div[2]/div[2]/main/div/div[3]/div/div/div[2]/div[3]/div/div/div[2]/div/div/div/div[1]/div/div[1]/div[2]/div/div/input")
    with open(os.getcwd() + "\wordlists\wordlist.txt", "r") as wl:
        words = wl.readlines()
    words = [word.strip('\n') for word in words]
    for word in words:
        search.send_keys(word)
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[3]/div/div/div[2]/div[2]/main/div/div[3]/div/div/div[2]/div[3]/div/div/div[2]/div/div/div/div[1]/div/div[1]/div[3]/div/div/div/div/div[3]/div[2]/div/div[1]/button"))
        )
        element.click()

        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div[3]/div/div/div/div[2]/main/div/div[3]/div/div/div[2]/div[3]/div/div/div[2]/div/div/div/div[1]/div/div[1]/div[3]/div/div/div/div/div[3]/div[2]/div/div[2]/div/div/div/div/button[2]/div'))
        )
        element.click()
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[3]/div/div/div[2]/div[2]/main/div/div[3]/div/div/div[2]/div[3]/div/div/div[2]/div/div/div/div[1]/div/div[1]/div[2]/div[2]/button/div/div"))
            )
            element.click()
            search.clear()
            wordcount += 1
        except TimeoutException:
            search.clear()
            continue
    return wordcount

if __name__ == "__main__":
    
    start_time = time.time()
    uname = prompt(text='Twitch username:', title='TWBBA')
    wordcount = goto_twitch(uname)
    with open(os.getcwd() + "\\result_log.txt",'w') as lg:
        lg.write(f"{wordcount} words added in {time.time() - start_time} seconds.")
    driver.quit()


