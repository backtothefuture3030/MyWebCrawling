import requests
from bs4 import BeautifulSoup
import re
import time






def create_soup(url):
    headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"}
    res = requests.get(url,headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text,"lxml")
    return soup

def print_news(index,title,link):
    print("{}. {}".format(index+1,title))
    print("  (링크 : {})".format(link))

def scrape_weather():
    print("[오늘의 날씨]")
    url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EB%8C%80%EC%97%B0%EB%8F%99%EB%82%A0%EC%94%A8&oquery=%EB%B6%80%EC%82%B0%EB%82%A0%EC%94%A8&tqi=hZrxKlp0Jy0ssLClguhssssstZw-282472"
    soup = create_soup(url)
    cast = soup.find("p",attrs={"class":"cast_txt"}).get_text() # 비, 어제보다 4˚ 낮아요
    curr_temp = soup.find("p",attrs={"class":"info_temperature"}).get_text().replace("도씨","") #현재 날씨에 20 도씨 C이렇게 있는거를 도씨를 지우는 역할
    min_temp = soup.find("span",attrs={"class":"min"}).get_text() #최저온도
    max_temp = soup.find("span",attrs={"class":"max"}).get_text()
    morning_rain_rate = soup.find("span",attrs={"class":"point_time morning"}).get_text().strip() # strip으로 공백제거
    afternoon_rain_rate = soup.find("span",attrs={"class":"point_time afternoon"}).get_text().strip()

    dust = soup.find("dl", attrs={"class":"indicator"})
    pm10 = dust.find_all("dd")[0].get_text()
    pm25 = dust.find_all("dd")[1].get_text()

   
    #출력
    print(cast)
    print("현재 {} (최저 {} / 최고 {})".format(curr_temp,min_temp,max_temp))
    print("오전 {} / 오후 {}".format(morning_rain_rate,afternoon_rain_rate))
    print()
    print("미세먼지 {}".format(pm10))
    print("초미세먼지 {}".format(pm25))
    print()

def scrape_headline_news():
    print("[헤드라인 뉴스]")
    url = "https://news.naver.com"
    soup = create_soup(url)
    news_list = soup.find("ul",attrs={"class":"hdline_article_list"}).find_all("li",limit=3)  # 3개 까지만 불러오도록 설정
    for index, news in enumerate(news_list):
        #title = news.div.a.get_text() 아래랑 같음
        title = news.find("a").get_text().strip()
        link = url + news.find("a")["href"]
        print_news(index,title,link)
    print()

def scrape_it_news():
    print("[IT 뉴스]")
    url = "https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=105&sid2=230"
    soup = create_soup(url)
    news_list = soup.find("ul",attrs={"class":"type06_headline"}).find_all("li",limit=3)
    for index, news in enumerate(news_list):
        a_idx=0
        img = news.find("img")
        if img:
            a_idx=1 # 이미지 태그가있으면 1번째 img태그의 정보를 사용한다

        a_tag = news.find_all("a")[a_idx]
        title = a_tag.get_text().strip()
        link = a_tag["href"]
        print_news(index,title,link)
    print()

def scrape_english():
    print("[오늘의 영어 회화]")
    url = "https://www.hackers.co.kr/?c=s_eng/eng_contents/I_others_english&keywd=haceng_submain_lnb_eng_I_others_english&logger_kw=haceng_submain_lnb_eng_I_others_english#;"
    soup = create_soup(url)
    sentences = soup.find_all("div", attrs = {"id":re.compile("^conv_kor_t")})
    print("(영어 지문)")
    for sentence in sentences[len(sentences)//2:]: # 8문장이 있다고 가정할때, 인덱스 기준 4~7 까지 잘라서 가져와야됨 
        print(sentence.get_text().strip())

    print("(한글 지문)")
    for sentence in sentences[0:len(sentences)//2]:
        print(sentence.get_text().strip())
    

def scrape_towweather():
    print("[내일의 날씨]")
    url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EB%82%B4%EC%9D%BC+%EB%8C%80%EC%97%B0%EB%8F%99+%EB%82%A0%EC%94%A8&oquery=%EB%82%B4%EC%9D%BC%EB%82%A0%EC%94%A8&tqi=hat%2Fgwp0J1ZssfsHENRssssstsl-129218"
    soup = create_soup(url)
    morning1_rain_rate = soup.find_all("span",attrs={"class":"todaytemp"})[1].get_text().strip() # strip으로 공백제거
    afternoon1_rain_rate = soup.find_all("span",attrs={"class":"todaytemp"})[2].get_text().strip()
    morning = soup.find_all("span",attrs={"class":"point_time morning"})[1].get_text().strip()
    afternoon = soup.find_all("span",attrs={"class":"point_time afternoon"})[2].get_text().strip()



    print("오전 {}도/ 오후 {}도".format(morning1_rain_rate,afternoon1_rain_rate))
    print()
    print("오전 {} / 오후 {}".format(morning,afternoon))
    print()
    print()
    
    a = input("종료하시려면 아무키나 입력하세요")
    if a:
        quit()

if __name__ == "__main__":
    scrape_weather() # 오늘의 날씨정보 가져오기
    scrape_headline_news() #헤드라인 뉴스정보
    scrape_it_news()
    scrape_english()
    scrape_towweather()
    
    
