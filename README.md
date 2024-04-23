# MLBPark Crawler
### Crawler for Korean Forum Website 'MLBPark':

### Required Libaries:
- beautifulsoup
- selenium
  
This crawler will gather all posts based on the search query, as well as its post comments.

It uses beautifulsoup in conjunction with selenium, please install if you have not done so already:

```
pip install beautifulsoup4
pip install -U selenium

```

There are a few lines you will need to manually enter, as MLBPark encodes its URL. You will need to copy and paste from the actual website. 

Here is where you will need to edit:
```
# 변수 설정 
QUERY = "한동훈"
search_QUERY = urlencode({'query' : QUERY}, encoding = 'utf-8')
URL = f"https://mlbpark.donga.com/mp/b.php?search_select=stt&search_input=%ED%95%9C%EB%8F%99%ED%9B%88&x=0&y=0&select=stt&m=search&b=bullpen&query=%ED%95%9C%EB%8F%99%ED%9B%88" 
```

The QUERY variable is simply your search term. The URL however, you will have to search on MLBPark yourself manually and then copy and paste the URL into the URL variable. Unfortunately this is the best way to do so because of how the website is configured at the moment.

The resulting CSV will be 'MLBPARK_{SearchTERM}_48pages_inner_links.csv' and 'MLBPARK_{SearchTERM}_48 pages.csv'. The former is the collection of the individual post URLs, and the latter is the collection of the post text and comment text for all posts that were in the result of the search.

### Using ChromeDriver: 
Make sure you have downloaded the latest ChromeDriver file, which you can find [here](https://chromedriver.chromium.org/getting-started), make sure to get the correct one for your OS and Chrome version. It may be necessary to update your Chrome as well.

```
driver = webdriver.Chrome(options=options, executable_path=ChromeDriverManager().install())
```

This is to create a driver instance in **Linux**. You will have to change this line if your OS is NOT linux. 

For example, this would be what you would change it to in **Windows**:
```
# Specify the path to the ChromeDriver executable if not added to PATH
chrome_driver_path = 'path/to/chromedriver.exe'

# Create ChromeDriver instance
driver = webdriver.Chrome(executable_path=chrome_driver_path)
```

# MLBPark 크롤러
### 한국 포럼 웹사이트 'MLBPark'을 위한 크롤러:

### 필요한 라이브러리:
- beautifulsoup


이 크롤러는 검색어에 기반하여 모든 게시물과 해당 게시물의 댓글을 수집합니다.

beautifulsoup과 selenium을 사용하며, 아직 설치하지 않은 경우 다음 명령을 실행하여 설치하세요:

```
pip install beautifulsoup4
pip install -U selenium

```

MLBPark은 URL을 인코딩하므로 수동으로 몇 줄을 입력해야 합니다. 여기가 편집해야 할 곳입니다:
```
# 변수 설정 
QUERY = "한동훈"
search_QUERY = urlencode({'query' : QUERY}, encoding = 'utf-8')
URL = f"https://mlbpark.donga.com/mp/b.php?search_select=stt&search_input=%ED%95%9C%EB%8F%99%ED%9B%88&x=0&y=0&select=stt&m=search&b=bullpen&query=%ED%95%9C%EB%8F%99%ED%9B%88" 

```

QUERY 변수는 단순히 검색어입니다. 그러나 URL은 MLBPark에서 직접 검색하고 URL을 복사하여 URL 변수에 붙여넣어야 합니다. 현재 웹사이트 구성상으로 인해 이 방법이 가장 좋은 방법입니다.

결과 CSV 파일은 'MLBPARK_{검색어}_48pages_inner_links.csv' 및 'MLBPARK_{검색어}_48 pages.csv'입니다. 전자는 개별 게시물 URL의 모음이며, 후자는 검색 결과의 모든 게시물에 대한 게시물 텍스트와 댓글 텍스트의 모음입니다.

### ChromeDriver 사용전: 
최신 ChromeDriver 파일을 다운로드했는지 확인하세요. 여기에서 찾을 수 있습니다. 사용 중인 OS 및 Chrome 버전에 맞는 것을 가져오세요. Chrome을 업데이트해야 할 수도 있습니다.

리눅스로 드라이버 인스턴스 만들기: 
```
driver = webdriver.Chrome(options=options, executable_path=ChromeDriverManager().install())
```

이것은 **리눅스**에서 드라이버 인스턴스를 만드는 것입니다. 사용 중인 OS가 리눅스가 아닌 경우 이 줄을 변경해야 합니다.

예를 들어, **윈도우**에서는 다음과 같이 변경해야 합니다:
```
# Specify the path to the ChromeDriver executable if not added to PATH
chrome_driver_path = 'path/to/chromedriver.exe'

# Create ChromeDriver instance
driver = webdriver.Chrome(executable_path=chrome_driver_path)
```
