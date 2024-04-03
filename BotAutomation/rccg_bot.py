from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
from dotenv import load_dotenv

load_dotenv(override=True)

USER = os.getenv("USERNAME")
PASSSWORD = os.getenv("PASSWORD")

print(USER)
print(PASSSWORD)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

class RccgSol():
    def __init__(self) -> None:
        self.youtube_url = 'https://www.youtube.com/'
        self.driver = webdriver.Chrome(options=chrome_options)

    def open_youtube(self, searched_name=str):
        driver = self.driver
        driver.get(self.youtube_url)
        time.sleep(3)
        search_bar = driver.find_element(By.NAME, value="search_query")
        time.sleep(3)
        search_bar.send_keys(searched_name)
        search_btn = driver.find_element(By.ID, value="search-icon-legacy")
        search_btn.click()
        time.sleep(7)
        more_options = driver.find_element(By.XPATH, value="/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-shelf-renderer[1]/div[1]/div[2]/ytd-vertical-list-renderer/div[1]/ytd-video-renderer[1]/div[1]/div/div[1]/div/div/ytd-menu-renderer/yt-icon-button/button")
        more_options.click()
        time.sleep(2)
        share_button = driver.find_element(By.XPATH, value="/html/body/ytd-app/ytd-popup-container/tp-yt-iron-dropdown/div/ytd-menu-popup-renderer/tp-yt-paper-listbox/ytd-menu-service-item-renderer[2]/tp-yt-paper-item")
        share_button.click()
        time.sleep(2)
        copy_link = driver.find_element(By.XPATH, value="/html/body/ytd-app/ytd-popup-container/tp-yt-paper-dialog/ytd-unified-share-panel-renderer/div[2]/yt-third-party-network-section-renderer/div[2]/yt-copy-link-renderer/div/yt-button-renderer/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]")
        copy_link.click()
        time.sleep(1)
        if copy_link:
            return True

    def open_rccg_sol(self, title_theme=str, position=int, user_date=str):
        driver = self.driver
        driver.get("https://rccg-sol.com/")
        time.sleep(5)
        log_in = driver.find_element(By.XPATH, value="/html/body/nav/ul/li[5]/a")
        log_in.click()
        time.sleep(3)
        user_name = driver.find_element(By.XPATH, value="/html/body/div/div[2]/form/input")
        user_name.send_keys(USER)
        user_password = driver.find_element(By.XPATH, value="/html/body/div/div[2]/form/div/input")
        user_password.send_keys(PASSSWORD)
        submit_button = driver.find_element(By.XPATH, value="/html/body/div/div[2]/form/button")
        submit_button.click()

        time.sleep(5)
        # ONCE LOGGED IN
        media_link = driver.find_element(By.XPATH, value="/html/body/nav/ul/li[4]/a")
        media_link.click()

        time.sleep(5)
        add_video = driver.find_element(By.XPATH, value="/html/body/div/button[2]")
        add_video.click()

        # Auto scroll to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)


        # FILL FORMS
        title = driver.find_element(By.XPATH, value='/html/body/div/div[2]/form/input[1]')
        title.send_keys(title_theme)
        time.sleep(0.5)

        program = driver.find_element(By.XPATH, value=f'/html/body/div/div[2]/form/select/option[{position}]')
        program.click()
        time.sleep(0.5)

        date_input=driver.find_element(By.XPATH, value="/html/body/div/div[2]/form/input[2]")
        date_input.send_keys(user_date)
        time.sleep(0.5)

        youtube_link = driver.find_element(By.XPATH, value="/html/body/div/div[2]/form/input[3]")
        youtube_link.send_keys(Keys.CONTROL, "v")
        time.sleep(0.5)

        # Post Video
        submit = driver.find_element(By.XPATH, value="/html/body/div/div[2]/form/button")
        submit.click()
        time.sleep(1)
        driver.close()
