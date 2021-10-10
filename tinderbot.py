# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions as selenium_exceptions
from pyvirtualdisplay import Display
from time import sleep


class Tinderbot:

    def __init__(self):
        #self.display = Display()
        #self.display.start()
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--verbose")
        chrome_options.add_argument("--log-path=/home/pi/Desktop/chromedriver.log")
        chrome_options.add_argument("--disable-notifications")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait10 = WebDriverWait(self.driver, 10)
        self.wait3 = WebDriverWait(self.driver, 3)
        return


    def login_with_fb(self, username, password):
        start_url = "https://tinder.onelink.me/9K8a/3d4abb81"
        # self.driver.implicitly_wait(10)
        self.driver.get(start_url)
        self.main_page = self.driver.current_window_handle

        self.wait10.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Log ind med Facebook']")))
        self.driver.find_element_by_xpath("//button[@aria-label='Log ind med Facebook']").click()

        # Switch to facebook login window
        sleep(3)
        try:
            self.driver.switch_to.window(self.driver.window_handles[2])
        except IndexError:
            self.driver.switch_to.window(self.driver.window_handles[1])

        # Accept cookies
        accept_button = self.wait10.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-cookiebanner='accept_button']")))
        accept_button.click()

        # Find login form and log in by sending login credentials
        username_form = self.driver.find_element_by_id("email")
        password_form = self.driver.find_element_by_id("pass")
        username_form.send_keys(username)
        password_form.send_keys(password)
        self.driver.find_element_by_name("login").click()

        # Switch back to tinder window
        self.driver.switch_to.window(self.main_page)
        return

    def prepare_for_swiping(self):
        # Accept cookies
        self.driver.find_elements_by_class_name("button--outline")[0].click()

        try:
            decline_button = self.wait3.until(EC.element_to_be_clickable((By.XPATH,"//span[text()='Måske senere']/parent::button")))
            decline_button.click()
        except:
            pass

        return

    def refresh_tinder(self):
        self.driver.get("https://tinder.com")

    def like(self):
        button_is_clickable = False
        while not button_is_clickable:
            try:
                like_button = self.wait10.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Synes godt om']/..")))
                like_button.click()
                button_is_clickable = True
            except:
                sleep(1)
                continue
        return

    def dislike(self):
        button_is_clickable = False
        while not button_is_clickable:
            try:
                dislike_button = self.wait10.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Niks']/..")))
                dislike_button.click()
                button_is_clickable = True
            except:
                sleep(1)
                continue
        return

    def superlike(self):
        superlike_button = self.wait10.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Superlike']/..")))
        button_is_clickable = False
        while not button_is_clickable:
            try:
                superlike_button.click()
                button_is_clickable = True
            except:
                sleep(1)
        return
    
    def check_for_match(self):
        try:
            self.wait10.until(EC.visibility_of_element_located((By.XPATH,"//div[text()='Det er et match!']")))
        except:
            return False
        return True

    def close_match(self):
        self.driver.find_element_by_xpath("//button[@title='Tilbage til Tinder']").click()
        return

    def check_for_empty_swipe(self):
        try:
            self.driver.find_element_by_xpath("//div[text()[contains(.,'Vi er løbet tør')]]")
            return True
        except:
            return False

    def check_for_no_likes_left(self):
        try:
            self.wait3.until(EC.visibility_of_element_located((By.XPATH,"//h3[text()='Du er løbet tør for synes godt om!']")))
            return True
        except:
            return False

    def autolike(self, iterations):
        print("autolike is running...")

        for i in range(iterations):
            try:
                self.like()
                print("{}th like".format(i+1))
            except selenium_exceptions.ElementClickInterceptedException:
                if self.check_for_match():
                    print("It's a match!")
                    self.close_match()
                else: 
                    try:
                        self.driver.find_element_by_xpath("//span[text()='Ikke interesseret']/parent::button")
                    except:
                        try:
                            self.driver.find_element_by_xpath("//span[text()='Måske senere']/parent::button")       
                        except:             
                            self.driver.save_screenshot('error.png')

        print("autolike stopped.")
        return
            
    def stop(self):
        self.driver.quit()
        #self.display.stop()
