from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException   
import time
import os

from web_scraper import DataCollection
from web_scraper import CRD

def main():

	# Get all the text data and meta data from the first community forum
	c = CRD()
	c.login_site()
	sf_df = self.parse_subforums()
	thread_df, r_threads = self.parse_all_threads(sf_df)
	complete_df, r_sites = self.parse_text_meta(thread_df, toCSV = True, save_as= 'CRD_df')
	
	# Save all the threads and sites that were not collected 
	d = {'Restricted_Threads': r_threads, 'Restricted_Sites': r_sites}
	self.gen_CSV(d, 'CRD_Restricted_Links')
	c.deactivate_driver()



if __name__ == "__main__":
	start_time = time.time()
	main()
	print("--- %s seconds ---" % round((time.time() - start_time)))


