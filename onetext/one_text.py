import onetext.constants as const
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class OneText(webdriver.Chrome):
    def __init__(self, driver_path=const.PATH_TO_CHROME_DRIVER, teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        super(OneText, self).__init__()
        self.implicitly_wait(6) #waiting for 6s

    def __exit__(self, *args) -> None:
        if self.teardown:
            self.quit()

    def land_first_page(self, grammarly_enabled=True):
        self.get(const.ONE_TEXT_URL) #opening the website

    def input_data_to_field(self, data="Please Input something"):
        self.implicitly_wait(6)
        fieldElement = self.find_element(By.CSS_SELECTOR, 'textarea[name="user-text"]')
        fieldElement.click()
        fieldElement.send_keys(Keys.COMMAND + 'A')
        fieldElement.send_keys(Keys.DELETE)
        fieldElement.send_keys(data)

    def check_for_plagiarism(self):
        checkBtn = self.find_element_by_class_name('btn_large')
        checkBtn.click()
        self.implicitly_wait(295)
        scoreElement = self.find_element_by_id('unique-value')
        score = scoreElement.get_attribute('innerHTML')
        newTestBtn = self.find_element_by_id('act-new-check')
        newTestBtn.click()
        return score