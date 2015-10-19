import urllib.request
from bs4 import BeautifulSoup

urlKs = 'https://www.kickstarter.com/projects/agfa/agfa-and-something-weird'
html = urllib.request.urlopen(urlKs).read()
soup = BeautifulSoup(html, 'html.parser')
title = soup.find_all("div", class_="NS_projects__header")[0].h2.a.text
datas = soup.find_all("data")
projectId = datas[0]['class']
temp = soup.find_all("div", class_="projectId")[0]
temp = soup.find_all("div", class_="ksr_page_timer poll stat")[0].contents[0]
temp1 = temp.text

backers = datas[0].text
pledged = datas[1].text
comments = datas[2].text
print(datas)
print('title:\t\t', title)
print('backers:\t', backers)
print('pledged:\t', pledged)
print('comments:\t', comments)
print(temp1)