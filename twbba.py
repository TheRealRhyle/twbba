from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from pymsgbox import *
import time
import os

PATH = os.getcwd() + "\webdriver\chromedriver.exe"

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(executable_path=PATH, options=options)

# driver = webdriver.Chrome(PATH)

def goto_twitch(username):
    driver.get(f"https://dashboard.twitch.tv/u/{username}/settings/moderation/blocked-terms")
    logged_in = confirm(text=f"{username}, you will need to manually log into the Chrome window that just opened.", title='Confirm Login', buttons=['Logged in!', 'Get me outta here!'])
    
    if logged_in.lower() == 'logged in!':
        print(f"Thank you {username}, beginning to add items to your automod word list.")
        add_words()
    else:
        driver.quit()
        sys.exit()

def add_words():
    search = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/div[2]/div[2]/main/div/div[3]/div/div/div[2]/div[3]/div/div/div[2]/div/div/div/div[1]/div/div[1]/div[2]/div/div/input")
    with open(os.getcwd() + "\wordlists\wordlist.txt", "r") as wl:
        words = wl.readlines()
    words = [word.strip('\n') for word in words]
    for word in words:
        search.send_keys(word)
        driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/div[2]/div[2]/main/div/div[3]/div/div/div[2]/div[3]/div/div/div[2]/div/div/div/div[1]/div/div[1]/div[3]/div/div/div/div/div[3]/div[2]/div/div[1]/button").click()
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="root"]/div[3]/div/div/div/div[2]/main/div/div[3]/div/div/div[2]/div[3]/div/div/div[2]/div/div/div/div[1]/div/div[1]/div[3]/div/div/div/div/div[3]/div[2]/div/div[2]/div/div/div/div/button[2]/div').click()
        time.sleep(1)
        driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/main/div/div[3]/div/div/div[2]/div[3]/div/div/div[2]/div/div/div/div[1]/div/div[1]/div[2]/div[2]/button/div/div').click()
        time.sleep(1)
        words.remove(word)

# wordbar:
# <input aria-label="Add term" type="search" class="sc-fzoant sc-fznzqM bkFJan ihwMMb sc-AxmLO tw-input" placeholder="Enter words or phrases" autocapitalize="none" autocorrect="off" data-a-target="tw-input" value="">
uname = prompt(text='Twitch username:', title='TWBBA')

# user = input("twitch username: ")
goto_twitch(uname)
driver.quit()


