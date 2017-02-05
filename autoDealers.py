import requests
import urllib
from bs4 import BeautifulSoup
import re
import nltk
import csv

f = open('C:\\Anaconda2\\myscripts\\axisHackathon\\delhi_dealers_justdial_links.csv', 'rt')	
w = open('C:\\Anaconda2\\myscripts\\axisHackathon\\delhi_output.csv', 'wb')
spamwriter = csv.writer(w, delimiter=',',quotechar='|')	
headers = {
    'Accept': "*/*",
    'User-Agent': "autoDealers.py",
    'X-Love': "hey sysadmin! you're awesome! <3"
}

# crawl web to make FX corpus
def crawl(url):
	response = requests.get(url,headers=headers)
	soup = BeautifulSoup(response.text, "html.parser")
	try:
		dealer_name = soup.find("span", class_="fn").text
	except:
		dealer_name = "NONAME"
	
	try:
		total_rating = soup.find("span", class_="value-titles").text
	except:
		total_rating = 0
		
	try:
		total_votes = soup.find("span", class_="votes").text
	except:
		total_votes = 0
		
	try:
		year_divs = soup.find_all("ul",class_="alstdul")
		year_established = year_divs[len(year_divs)-1].find("li").text
		year_established = int(year_established)
	except:
		year_established = "NA"
	
	try:
		websiteURL = "none"
		websiteLinks = soup.find_all("span", class_="mreinfp comp-text")
		websiteLink =websiteLinks[len(websiteLinks)-1].find("a")
		if(websiteLink and websiteLink.has_attr('href')):
			websiteURL = websiteLink['href']
	except:
		websiteURL = "none"
		
	try:
		domain = websiteURL.split("//")[-1].split("/")[0]
		print domain
		resTxt = requests.get("http://www.alexa.com/siteinfo/"+domain).text
		#resTxt = requests.get("http://www.trafficestimate.com/"+domain).text
		#trafficEstimate = BeautifulSoup(resTxt, "html.parser")
		#alexaRank = trafficEstimate.find("td",id="ctl00_cphMainContent_tcAlexaRank").text
		alexaPage = BeautifulSoup(resTxt, "html.parser")
		alexaStats = alexaPage.find_all("strong",class_="metrics-data align-vmiddle")
		try:
			alexaRank = int(alexaStats[0].text.strip().replace(",",""))
		except:
			alexaRank = 99999999
			
		try:
			pageViewsPerVisitor = float(alexaStats[2].text.strip())
		except:
			pageViewsPerVisitor = 0
			
		try:
			alexaTime = alexaStats[3].text.strip().split(":")
			dailyTimeOnSiteInSeconds = int(alexaTime[0])*60 + int(alexaTime[1])
		except:
			dailyTimeOnSiteInSeconds = 0
		
	except:
		print "website doesnt exist"
		
	print dealer_name, total_rating, total_votes, year_established, alexaRank, pageViewsPerVisitor, dailyTimeOnSiteInSeconds, websiteURL, "\n"
	spamwriter.writerow([dealer_name,total_rating,total_votes,year_established,alexaRank,pageViewsPerVisitor,dailyTimeOnSiteInSeconds,websiteURL])
	
def begin():
	
	spamwriter = csv.writer(w, delimiter=',',quotechar='|')	

	reader = csv.reader(f)
	
	for row in reader:
		print "crawling : " ,row[0]
		crawl(row[0])
			



begin()



