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
	date = datetime.datetime.now().strftime("%b_%d")
	try:
		os.makedirs(os.getcwd() + '/images/' + hashtag + '_pictures_' + date)
	except OSError as e:
		if e.errno != errno.EEXIST:
			print("Folder /images/" + hashtag + "_pictures_" + date + "already exists!")
			pass
	return os.getcwd() + '/images/' + hashtag + '_pictures_' + date

# returns list of plaintext of bodies
# iterates until timelimit is reached
def get_webpage_from_hashtag(hashtag, timelimit):
	
	browser = webdriver.Chrome(ChromeDriverManager().install())
	browser.get('https://www.instagram.com/explore/tags/' + hashtag + '/')
	
	bodyList = []

	wait_for_load_time = 2.5

	last_height = browser.execute_script("return document.body.scrollHeight")
	
	ctr = 1
	while(True):
		browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

		time.sleep(wait_for_load_time)

		new_height = browser.execute_script("return document.body.scrollHeight")

		if new_height == last_height:
			break
		last_height = new_height

		ctr += 1
		
		bodyList.append(browser.execute_script("return document.body.innerHTML"))
		
		if(ctr == int(timelimit/wait_for_load_time)):
			break

	# instagram dynamically removes elements from the body depending on location of browser on page
	# need to load html, scroll, then load html again
	browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	
	bodyList.append(browser.execute_script("return document.body.innerHTML"))

	browser.quit()

	return bodyList

# downloads all pics from specified hashtag into a folder
def get_most_recent_pics(hashtag, timelimit):
	folderName = create_folder(hashtag) # create folder and get name for image storage location
	bodyList = get_webpage_from_hashtag(hashtag, timelimit) # get plaintext of insta page

	scrapedImages = set()

	count = 0
	for body in bodyList:

		soup = BeautifulSoup(body, 'html.parser')
		picThumbnails = soup.select('span[id^="react-root"] section main article div div div div a')

		for thumb in picThumbnails:
			linkToPic = thumb.attrs['href']
			linkToPic = linkToPic.replace('/', '_')

			if linkToPic in scrapedImages: # avoid downloading same pic
				continue
			else:
				scrapedImages.add(linkToPic)

			pic = thumb.select('div[class^="KL4Bh"] img')

			imgUrl = ""
			try:
				imgUrl = pic[0].attrs['srcset'] # check if has image link, just safety net
			except KeyError as e:
				continue

			diffPics = imgUrl.split(',')

			imagepath = folderName + '/' + linkToPic + '.jpg'
			urlretrieve(diffPics[len(diffPics) - 1].split(' ')[0], imagepath)
			count += 1

	print("Num pics: %d" % count)

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


if __name__ == '__main__':	
	uinput = input("Enter hashtag: ")
	timelimit = int(input("Enter time limit: "))

	get_most_recent_pics(uinput, timelimit)
	# get_highquality_pics(uinput, timelimit)






