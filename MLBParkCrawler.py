import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime as dtime
import csv


# 변수 설정 
PATH = "" 
QUERY = "한동훈"
search_QUERY = urlencode({'query' : QUERY}, encoding = 'utf-8')
URL = f"https://mlbpark.donga.com/mp/b.php?search_select=stt&search_input=%ED%95%9C%EB%8F%99%ED%9B%88&x=0&y=0&select=stt&m=search&b=bullpen&query=%ED%95%9C%EB%8F%99%ED%9B%88" 


# 마지막 페이지까지 클릭 
def go_to_last_page(URL): 
# Set up Chrome options for headless mode
	chrome_options = Options()
	chrome_options.add_argument("--headless")  # Run in headless mode
	chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration for headless mode

	# Specify the path to the chromedriver executable
	chromedriver_path = '/home/jongwon/MEGA/Crawlers/MLBPark/chromedriver'

	# Initialize the webdriver with Chrome options
	driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)

	# Set implicit wait time
	driver.implicitly_wait(1)

	# Navigate to the URL
	driver.get(URL)

	wait = WebDriverWait(driver, 5)
	   
	while True :
		# class가 right인 버튼이 없을 때까지 계속 클릭 
		try :
			time.sleep(2)
			element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'right')))
			element.click()
			time.sleep(2)
		except TimeoutException:
			print("no pages left")
			break 

	html = driver.page_source
	soup = BeautifulSoup(html, 'lxml')
	#driver.quit()
	return soup


# 마지막 페이지 번호 알아내기 
def get_last_page(URL): 
	soup = go_to_last_page(URL)
	pagination = soup.find('div', {'class' : 'page'})
	pages = pagination.find_all("a")
	page_list = []
	for page in pages[1 :]:
		page_list.append(int(page.get_text(strip=True)))
	max_page = page_list[-1]
	print(f"총 {max_page} 개의 페이지가 있습니다.")
	return max_page
 	#return max_page
	#return 232


# 게시판 링크 모두 가져오기 
def get_boards(page_num): 
	boards = []
	for page in range(page_num):
		boards.append(f"https://mlbpark.donga.com/mp/b.php?p={30*page+1}&m=search&b=bullpen&query=한동훈&select=stt&subquery=&subselect=&user=") #30원래
		print(boards[-1])
	return boards
#max_page 원래는 page_num

# 게시글 링크 가져오기 
def get_posts(): 
	global QUERY
	global PAGES
	board_links = get_boards(PAGES)
	posts = []
	for board_link in board_links:
		# print(f"게시판 링크는 {board_link}") 
		req = requests.get(board_link)
		print(req.status_code) # ---개 나와야 함 
		soup = BeautifulSoup(req.text, 'lxml')
		tds = soup.find_all('div', {'class' : 'tit'})
		for td in tds:
			post = td.find('a', {'class' : 'txt'})
			if post is not None :
				posts.append(post['href'])
	print(f"총 {len(posts)} 개의 글 링크를 찾았습니다.")

# 게시글 링크 csv로 저장 
	post_file = open(f"MLBPARK_{QUERY}_{PAGES}pages_inner_links.csv", mode='w', encoding='utf-8')
	writer = csv.writer(post_file)
	for post in posts:
		writer.writerow([post])
	post_file.close()
	return posts



# 한 페이지에서 정보 가져오기 
def extract_info(URL, wait_time=1, delay_time=1): 
	try:
		options = webdriver.ChromeOptions()
		options.add_argument('--incognito')
		# Initialize the webdriver with Chrome options
		driver = webdriver.Chrome(options=options, executable_path=ChromeDriverManager().install())

		# Set implicit wait time
		driver.implicitly_wait(wait_time)

		# Navigate to the URL
		driver.get(URL)

		html = driver.page_source
		time.sleep(delay_time)

		soup = BeautifulSoup(html, 'lxml')

		title = soup.find('div', {'class' : 'titles'}).get_text(strip=True) 
		post_time = soup.find('div', {'class' :'text3'}).find('span', {'class' :'val'}).get_text(strip=True)
		post = soup.find('div', {'id' : 'contentDetail'}).get_text(strip=True)
  
		reply_cnt = int(soup.find('span', {'id' : 'replyCnt'}).get_text(strip=True).replace('\n', '').replace('\r', '').replace(',', ''))

		reply_content = ""
		if reply_cnt != 0 :
			replies = soup.find_all('span', {'class' : 're_txt'})
			for reply in replies:
				reply_content += reply.get_text(strip=True).replace('\n', '').replace('\r', '').replace('\t','') + "\n"
			

		print(URL, "완료")

		return {'title' : title, 'post_time' :post_time, 'post' : post, 'reply_cnt' : reply_cnt, 'reply_content' : reply_content}
	except Exception as e:
		print(f"에러발생: {e}")
		print(URL, "에러")
		pass

def get_contents(): 
	global mlbpark_results
	post_links = get_posts()
	for post_link in post_links:
		content = extract_info(post_link)
		if content is not None:
			append_to_file(f"MLBPARK_{QUERY}_{PAGES} pages.csv", content)
		else:
			append_to_file(f"MLBPARK_{QUERY}_{PAGES} pages.csv", {'title' : '', 'post_time' : '', 'post' : '', 'reply_cnt' : 0, 'reply_content' : ''})
	return print("모든 작업이 완료되었습니다.")


# 저장 파일 만드는 함수 
def save_to_file(): 
	global QUERY
	global PAGES
	file = open(f"MLBPARK_{QUERY}_{PAGES} pages.csv", mode='w', encoding='utf-8')
	writer = csv.writer(file)
	#writer.writerow(['site', 'title', 'user_id', 'post_time', 'post', 'view_cnt', 'recomm_cnt', 'reply_cnt', 'reply_content'])
	writer.writerow(['title', 'post_time', 'post', 'reply_content'])
	file.close()
	return file

# 파일 열어서 쓰는 함수 
def append_to_file(file_name, dictionary): 
	file = open(file_name, mode='a', encoding='utf-8') # 덮어 쓰기 
	writer = csv.writer(file)
	writer.writerow(list(dictionary.values()))
	file.close()
	return 


# 함수 실행 
PAGES = get_last_page(URL)

mlbpark_results = save_to_file()
get_contents()