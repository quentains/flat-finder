from time import sleep
from datetime import datetime
import pickle
import os

from selenium import webdriver
from bs4 import BeautifulSoup

from pushbullet import Pushbullet
from pyvirtualdisplay import Display

def scrap(url) :
	driver = webdriver.Firefox()
	driver.implicitly_wait(5)
	driver.get(url)
	source_page = BeautifulSoup(driver.page_source, 'html.parser')
	driver.quit()

	return source_page

def notify(link) :
	push = pb.push_link("Nouvel appart !", link)

def update(page) :

	data_file = 'data.txt'

	# Get already known links
	try:
	    links = pickle.load(open(data_file, "rb"))
	except:
	    links = []

	# Looking for new links
	apparts = page.find_all('a', attrs={"class": "card__title-link"})
	for appart in apparts:
	    link = appart.get('href')
	    link = link[:link.index("?")]
	    if link not in links:
	        links.append(link)
	        print("[+] NEW : " + link)

	        notify(link)

	# Update links list
	pickle.dump(links, open(data_file, "wb"))


if __name__ == '__main__':

	if os.getenv('API_KEY') is None :
		print("API_KEY not defined")
		exit()
		
	pb = Pushbullet(os.getenv('API_KEY'))

	display = Display(visible=0, size=(800, 600))
	display.start()

	while True :
		
		now = datetime.now()
		print("[{}] Scraping...".format(now.strftime("%d/%m/%Y %H:%M:%S")))

		source_page = scrap("https://www.immoweb.be/fr/recherche/appartement/a-louer/gembloux/5030?countries=BE&orderBy=newest")
		update(source_page)
		
		sleep(60*15)
