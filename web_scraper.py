from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException   
import time
import os


class DataCollection: 

	def __init__(self):
		self.driver =  None

	def activate_driver(self):
		'''Create webdriver instance.'''
		chrome_options = webdriver.ChromeOptions()
		chrome_options.add_argument('--headless')
		self.driver = webdriver.Chrome('../chromedriver', options = chrome_options)
		print('Driver activated.')
		return self.driver

	def check_exists_by_xpath(self, xpath):
		'''Determine existence of xpath element.'''
		try:
			self.driver.find_element_by_xpath(xpath)
		except NoSuchElementException:
			return False
		return True

	def check_exists_by_css(self, css):
		'''Determine existence of css element.'''
		try:
			self.driver.find_element_by_css_selector(css)
		except NoSuchElementException:
			return False
		return True

	def is_restricted(self, link):
		'''Determine if site is restricted.'''
		if 'unread' in link:
			return True
		else:
			return False

	def correct_restricted(self, link):
		'''Remove restricting label in weblink string.'''
		corrected = link.replace('unread','')
		return corrected

	def deactivate_driver(self):
		'''Close webdriver instance.'''
		self.driver.close()
		print('Driver deactivated.')

	def gen_CSV(self, d, save_as):
		'''Produce CSV file of dataframe object.'''
		df = pd.DataFrame(d)
		df.to_csv("{}.csv".format(save_as)) 
		print('CSV ouputted.')

	

