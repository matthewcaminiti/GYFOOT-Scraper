from bs4 import BeautifulSoup
import requests
from urllib.parse import quote, unquote
from urllib.request import urlretrieve
import os, errno
import datetime
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

#if you want to dynamically create folders
# returns the full path of new/existing folder
def create_folder(hashtag): 
	date = datetime.datetime.now().strftime("%b_%d") # get the datetime in a string as the specified format
	try:
		os.makedirs(os.getcwd() + '/' + hashtag + '_pictures_' + date) # try to create the folder in the current directory with specific name
	except OSError as e:
		if e.errno != errno.EEXIST: # will throw this error if the folder exists, so no need to make
			print("Folder /" + hashtag + "_pictures_" + date + "already exists!")
			pass # non-crashing error so just move on
	return os.getcwd() + '/' + hashtag + '_pictures_' + date # return the full path of the folder

# returns list of plaintext of bodies
# iterates until timelimit is reached
def get_webpage_from_hashtag(hashtag, timelimit):
	
	browser = webdriver.Chrome(ChromeDriverManager().install()) # open the webbrowser and install driver if doesn't exist
	browser.get('https://www.instagram.com/explore/tags/' + hashtag + '/') # load hashtag page
	
	bodyList = [] # list of html plaintext

	wait_for_load_time = 2.5 # how long to wait for page and failsafes

	last_height = browser.execute_script("return document.body.scrollHeight")
	
	# yeet = 1
	start = datetime.datetime.now() # used for setting time limit -- OBSOLETE

	while(True): # loop to scroll to bottom of document and dynamically grab html plaintext

		browser.execute_script("window.scrollTo(0, document.body.scrollHeight);") # scroll to bottom of current html

		time.sleep(wait_for_load_time) # wait to load next

		new_height = browser.execute_script("return document.body.scrollHeight") # get next bottom of html

		if new_height == last_height: # if nothing new is loaded, should have same heights (possibly at bottom of html)
			time.sleep(wait_for_load_time * 2) # failsafe 1 in case of slow internet
			new_height = browser.execute_script("return document.body.scrollHeight")
			if(new_height == last_height): # check again
				time.sleep(wait_for_load_time * 2) # failsafe 2 in case of hella slow internet
				new_height = browser.execute_script("return document.body.scrollHeight")
				if(new_height == last_height): # if it hasn't loaded in this time, you need to upgrade your internet or it is at bottom of page
					print('reached "bottom"\a')
					break

		last_height = new_height # not at bottom of document so load next height

		# yeet += 1
		
		bodyList.append(browser.execute_script("return document.body.innerHTML")) # add the current html plaintext to list of html plaintext
		
		# OLD CODE THAT WAS FOR SETTING A TIME LIMIT
		# current = datetime.datetime.now()
		# timeDiff = current - start
		# if(timeDiff.total_seconds() >= timelimit*60):
			# break
		# if(yeet == int(timelimit/wait_for_load_time)):
			# break

	browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	
	bodyList.append(browser.execute_script("return document.body.innerHTML"))

	browser.quit()

	return bodyList # return list of html plaintext for parsing

# downloads all pics from specified hashtag into a folder
def get_most_recent_pics(hashtag, timelimit):
	folderName = create_folder(hashtag) # create folder and get name for image storage location
	bodyList = get_webpage_from_hashtag(hashtag, timelimit) # get list of plaintexts of insta page

	scrapedImages = set() # set of image linkds to avoid dl'ing duplicates

	lenList = len(bodyList)
	count = 0
	for body in bodyList:

		soup = BeautifulSoup(body, 'html.parser') # spawn a soup for the current html plaintext
		picThumbnails = soup.select('span[id^="react-root"] section main article div div div div a') # find the damn pics

		for thumb in picThumbnails:
			linkToPic = thumb.attrs['href'] # get link to pic attribute
			linkToPic = linkToPic.replace('/', '_') # clean that bitch up

			if linkToPic in scrapedImages: # avoid downloading same pic
				continue
			else:
				scrapedImages.add(linkToPic) # add to set since not in set

			pic = thumb.select('div[class^="KL4Bh"] img') # get the pic

			imgUrl = ""
			try:
				imgUrl = pic[0].attrs['srcset'] # check if has image link, just safety net
			except KeyError as e:
				continue

			diffPics = imgUrl.split(',')

			imagepath = folderName + '/' + linkToPic + '.jpg'
			urlretrieve(diffPics[len(diffPics) - 1].split(' ')[0], imagepath) # download the pic with specified name imagepath
			count += 1
			print("%s out of %s" % (count, lenList))

	print("Num pics: %d" % count)
'''
def get_highquality_pics(hashtag, timelimie):
	
	browser = webdriver.Chrome(ChromeDriverManager().install())
	browser.get('https://www.instagram.com/explore/tags/' + hashtag + '/')

	scrapedImages = set()

	wait_for_load_time = 2.5

	last_height = browser.execute_script("return document.body.scrollHeight")
	
	yeet = 1
	while(True):
		browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

		time.sleep(wait_for_load_time)

		new_height = browser.execute_script("return document.body.scrollHeight")

		if new_height == last_height:
			break
		last_height = new_height

		yeet += 1
		
		# need to click on every image, get html, then scrape and dl
		images = browser.find_elements_by_xpath("//div[contains(@class,'v1Nh3 kIKUG  _bz0w')]")
		print(len(images))
		for image in images:
			a = image.find_element_by_tag_name('a')
			print("%s\n" % a.value_of_css_property('href'))
			# print("%s\n" % type(image))

		innerHtml = browser.execute_script("return document.body.innerHTML")
		
		soup = BeautifulSoup(innerHtml, 'html.parser')


		if(yeet == int(timelimit/wait_for_load_time)):
			break
'''	

uinput = input("Enter hashtag: ")
# timelimit = int(raw_input("Enter time limit (in minutes): "))
timelimit = 0

get_most_recent_pics(uinput, timelimit)
# get_highquality_pics(uinput, timelimit)






