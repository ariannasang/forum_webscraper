from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException   
import time
import os

from webscraper import DataCollection

class CRD(DataCollection):

	def __init__(self):
		self.driver = super().activate_driver()

	def login_site(self):
		'''Navigate webdriver through the website's account portal.'''
		doll_site = #hidden
		un = #hidden
		pw = #hidden

		self.driver.get(doll_site)
		self.driver.find_element_by_css_selector('.p-navgroup-link--logIn').click()
		time.sleep(3)
		self.driver.find_element_by_name("login").send_keys(un)
		time.sleep(1)
		self.driver.find_element_by_name("password").send_keys(pw)
		time.sleep(1)
		self.driver.find_element_by_css_selector('.button--icon--login').click()
		print('Login complete.')
		return self.driver

	def parse_subforums(self, toCSV = False, save_as  = None):
		'''Collect all subforum links from the forum's main page.'''
		sf_element = '//h3[@class="node-title"]/a'

		subforums = self.driver.find_elements_by_xpath(sf_element)
		sfNames = []
		sfLinks = [] 

		for sf in subforums:
			x = sf.text
			sfNames.append(x)
			y = sf.get_attribute("href")
			sfLinks.append(y)

		d = {'Subforum_Name': sfNames, 'Subforum_Link':sfLinks  }
		df = pd.DataFrame(d)
		
		if toCSV == True:
			self.gen_CSV(d, save_as)

		print('Subforums collected.')

		return df

	def count_aux_pages(self, link):
		'''Count the number of auxillary webpages of a link.'''

		self.driver.get(link)
		css_1 = '.pageNav-jump--next'
		css_2 = 'ul.pageNav-main > li.pageNav-page > a'

		if self.check_exists_by_css(css_1)==True:
			pages = self.driver.find_elements_by_css_selector(css_2)
			num = int(pages[-1].text)
			return num 
		else:
			return 1

	def aux_pages(self, link, n_aux_pages):
		'''Generate links for auxilllary webpages of a link.'''
		counter = 0
		page_num = 1
		links = [link]
		while counter < n_aux_pages:
			page_num +=1
			next_page = '{}page-{}'.format(link, page_num)
			links.append(next_page)
			counter+=1
		return links

	def parse_threads_per_sf(self, sf_link):
		'''Collect all thread names and thread links from a subforum.'''
		
		tNames = []
		tLinks = []
		thread_xpath = '//div[@class = "structItem-title"]/a'

		self.driver.get(sf_link)
		n_aux_pages = self.count_aux_pages(sf_link)
		sf_aux_pages = self.aux_pages(sf_link, n_aux_pages)

		for l in sf_aux_pages:
			self.driver.get(l)
			threads = self.driver.find_elements_by_xpath(thread_xpath)		

			for thread in threads:
				n = thread.text
				tNames.append(n)
				l = thread.get_attribute("href")
				tLinks.append(l)

		return tNames, tLinks


	def parse_all_threads(self, df, toCSV= False, save_as= None, update_counter = 1):
		'''Collect all thread names and thread links.'''

		tNames = []
		tLinks = []
		sfNames = []
		problem_sites = []

		counter = update_counter
		for sf_link in df['Subforum_Link']:

			names, links = self.parse_threads_per_sf(sf_link)

			if len(names) == len(links):
				for n in names:
					tNames.append(n)
					sfNames.append(df['Subforum_Name'][counter])
				for l in links:
					tLinks.append(l)
			else:
				problem_sites.append(sf_link)
			counter+=1

		d = {'Subforum_Names': sfNames, 'Thread_Names': tNames, 'Thread_Links': tLinks}
		df = pd.DataFrame(d)


		if toCSV == True:
			self.gen_CSV(d, save_as)

		return df, problem_sites

	def parse_text_meta(self, df, toCSV = False, save_as = None):
		''' Collect comments, timestamps, member status and username from thread links.'''

		# Containers
		comments = []
		timestamps = []
		member_status = []
		tn = []
		profiles = []
		problem_sites = []

		# Assign element identifiers
		thread_identifier = '.p-breadcrumbs:nth-child(1) li:nth-child(4) span'
		thread_name_identifier = '.p-title-value'
		comment_identifier = '.js-selectToQuote .bbWrapper'
		timestamp_identifier = '.message-attribution-main .u-dt'
		ms_identifier = '.message-userTitle'
		profile_identifier = '.message-name .username'

		# Cycle through all thread links
		for thread_link in df['Thread_Links']:

			if self.is_restricted(thread_link) == True:
				thread_link = self.correct_restricted(thread_link)

			n_aux_pages = self.count_aux_pages(thread_link)
			aux_pages = self.aux_pages(thread_link, n_aux_pages)

			#Cycle through all auxillary pages of thread link 
			for page in aux_pages:
				self.driver.get(page)

				if self.check_exists_by_css(thread_identifier) == True:
					c_elements = self.driver.find_elements_by_css_selector(comment_identifier)
					t_elements = self.driver.find_elements_by_css_selector(timestamp_identifier)
					ms_elements = self.driver.find_elements_by_css_selector(ms_identifier)
					thread_name = self.driver.find_element_by_css_selector(thread_name_identifier)
					profile_elements = self.driver.find_elements_by_css_selector(profile_identifier)

					if len(c_elements) != len(t_elements):
						problem_sites.append(page)
					else:
						for a in c_elements:
							comments.append(a.text)
							tn.append(thread_name.text)
						for b in t_elements:
							timestamps.append(b.text)
						for c in ms_elements:
							member_status.append(c.text)
						for d in profile_elements:
							profiles.append(d.text)
				else:
					problem_sites.append(page)

		print('Scraper complete.')
		print('LENGTHS- Thread names: {}, Comments: {}, Member status: {}, Timestamps: {}, Usernames: {}').format(len(tn), len(comments). len(member_status), len(timestamps), len(profiles))
		d = {'Thread_Names': tn, 'Usernames': profiles, 'Member_Status': member_status, 'Timestamps': timestamps, 'Comments': comments }
		df = pd.DataFrame(d)

		if toCSV == True:
			self.gen_CSV(d, save_as)

		return df, problem_sites
