import grammarly.constants as const
import grammarly.secretConst as sec_const
import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class Grammarly(webdriver.Chrome):
    def __init__(self, driver_path=const.PATH_TO_CHROME_DRIVER, teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        super(Grammarly, self).__init__()
        self.implicitly_wait(6) #waiting for 6s

    def clear(self):
        fieldElement = self.find_element_by_class_name('_9c5f1d66-denali-editor-editor')
        fieldElement.click()
        fieldElement.send_keys(Keys.COMMAND + 'A')
        fieldElement.send_keys(Keys.DELETE)
        time.sleep(7)

    def clear_and_logout(self):
        fieldElement = self.find_element_by_class_name('_9c5f1d66-denali-editor-editor')
        fieldElement.click()
        fieldElement.send_keys(Keys.COMMAND + 'A')
        fieldElement.send_keys(Keys.DELETE)
        fieldElement.send_keys("Do not delete this file. It is for a bot")
        time.sleep(7)
        try:
            self.get(const.MAIN_PAGE_URL) #opening the website, the Grammarly Login page
        except:
            self.switch_to.alert.accept()
        #self.switch_to_alert().accept()
        self.implicitly_wait(10)
        logOutBtn = self.find_element_by_css_selector('div[data-name="logout-lnk"]')
        logOutBtn.click()

    def __exit__(self, *args) -> None:
        if self.teardown:
            self.clear()
            self.quit()

    def land_first_page(self):
        self.get(const.URL) #opening the website, the Grammarly Login page
        link = self.find_element(By.LINK_TEXT, 'Log in')
        link.click()

    def give_credentials_and_login(self, premium=False):
        self.implicitly_wait(5)
        emailElement = self.find_element_by_id('email')
        emailElement.click()
        if not premium:
            emailElement.send_keys(sec_const.ACC_EMAIL)
        else:
            emailElement.send_keys(sec_const.PREM_ACC_EMAIL)
        submitElement = self.find_element_by_css_selector(
            'button[data-qa="btnLogin"]'
        )
        submitElement.click()
        self.implicitly_wait(5)
        passwordElement = self.find_element_by_id('password')
        passwordElement.click()
        if not premium:
            passwordElement.send_keys(sec_const.ACC_PASSWORD)
        else:
            passwordElement.send_keys(sec_const.PREM_ACC_PASSWORD)
        submitElement.click()
        time.sleep(20)

    def open_demo_file(self):
        self.implicitly_wait(10)
        demoFileBtn = self.find_element_by_css_selector(
            'a[data-name-id="1494732814"]'
        )
        demoFileBtn.click()

    def input_data_to_field(self, data="Please Input something"):
        fieldElement = self.find_element_by_class_name('_9c5f1d66-denali-editor-editor')
        fieldElement.click()
        fieldElement.send_keys(Keys.COMMAND + 'A')
        fieldElement.send_keys(Keys.DELETE)
        fieldElement.send_keys(data)

    def get_score_and_check(self, passing_mark):
        self.implicitly_wait(10)
        #scoreValElement = self.find_element_by_class_name('_5da3baf5-header-performanceScoreA11yContrast')
        scoreValElement = self.find_element_by_class_name('_48adf116-header-performanceScore')
        scoreVal = scoreValElement.get_attribute('innerHTML')
        statusElement = self.find_element_by_class_name('f1vn8v6g')
        print(statusElement.text)
        scoreVal = int(scoreVal)
        if scoreVal < passing_mark:
            return [False, scoreVal]
        else:
            return [True, scoreVal]

    def land_premium_account_page(self):
        fieldElement = self.find_element_by_class_name('_9c5f1d66-denali-editor-editor')
        fieldElement.click()
        fieldElement.send_keys(Keys.COMMAND + 'A')
        fieldElement.send_keys(Keys.DELETE)
        time.sleep(8)
        self.get(const.MAIN_PAGE_URL) #opening the website, the Grammarly Login page
        #self.switch_to_alert().accept()
        self.implicitly_wait(10)
        logOutBtn = self.find_element_by_css_selector('div[data-name="logout-lnk"]')
        logOutBtn.click()
        self.implicitly_wait(7)
        link = self.find_element(By.LINK_TEXT, 'Log in')
        link.click()
        self.give_credentials_and_login(premium=True)
        self.implicitly_wait(15)
        demoFileBtn = self.find_element_by_css_selector(
            'a[data-name-id="1494311420"]'
        )
        demoFileBtn.click()

    def input_data_to_field_in_premium_account(self, data="Please Input something"):
        fieldElement = self.find_element_by_class_name('_9c5f1d66-denali-editor-editor')
        fieldElement.click()
        fieldElement.send_keys(Keys.COMMAND + 'A')
        fieldElement.send_keys(Keys.DELETE)
        fieldElement.send_keys(data)

    def click_on_plagiarism_and_get_score(self, initial=True):
        time.sleep(10)
        #plagiarismBtn = self.find_element_by_class_name('_0485f5a1-document_actions-plagiarismBtn')
        if initial:
            plagiarismBtn = self.find_element_by_xpath('//*[@id="page"]/div/div[2]/div[2]/div/div[4]/div[2]/div/div[2]/div/div[2]/div/div[4]/div[3]')
            plagiarismBtn.click()
        time.sleep(40)
        #plagiarismScoreElement = self.find_element_by_css_selector('span[class="percent_f1qrek1k"]')
        #plagiarismScoreElement = self.find_element_by_xpath('//*[@id="page"]/div/div[2]/div[2]/div/div[4]/div[3]/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/svg/text/text()[1]')
        #plagiarismScoreElement = self.find_element_by_xpath('//*[@id="page"]/div/div[2]/div[2]/div/div[4]/div[3]/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/svg/text')
        #plagiarismScoreElement = self.find_element_by_xpath('//*[@id="page"]/div/div[2]/div[2]/div/div[4]/div[2]/div/div[2]/div/div[2]/div/div[4]/div[3]/div/div[2]/div/svg/text/text()')
        plagiarismScoreElement = self.find_element_by_class_name('plagiarismCounterContent_f10crefn')
        plagiarismScore = plagiarismScoreElement.get_attribute('innerHTML')
        return plagiarismScore


'''
class GrammarlyPremium(webdriver.Chrome):
    def __init__(self, driver_path=const.PATH_TO_CHROME_DRIVER, teardown=True):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        super(Grammarly, self).__init__()
        self.implicitly_wait(6) #waiting for 6s

    def __exit__(self, *args) -> None:
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.URL) #opening the website, the Grammarly Login page
        link = self.find_element(By.LINK_TEXT, 'Log in')
        link.click()
'''