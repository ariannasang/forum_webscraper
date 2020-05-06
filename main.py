from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException   
import time
import os

from web_scraper import DataCollection
from subclass_crd import CRD

def main():

	c = CRD()
	
	# Enter site
	args = c.optional_credentials()
	un, pw = c.determine_credentials(args, path = './data/CRD.pw')
	c.login_site(un, pw)

	# Get all the text data and meta data from the first community forum
	sf_df = c.parse_subforums()
	thread_df, r_threads = c.parse_all_threads(sf_df)
	complete_df, r_sites = c.parse_all_text_meta(thread_df, toCSV = True, save_as= 'CRD_df')
	
	# Save all the threads and sites that were not collected 
	d = {'Restricted_Threads': r_threads, 'Restricted_Sites': r_sites}
	c.gen_CSV(d, 'CRD_Restricted_Links')
	c.deactivate_driver()


if __name__ == "__main__":
	start_time = time.time()
	main()
	print("--- %s seconds ---" % round((time.time() - start_time)))


