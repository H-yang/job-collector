from bs4 import BeautifulSoup
import urllib2
import re


def getAllUrls(location, pages):
    file_name = location+"-urls"
    file = open(file_name,"w") 
    for i in range(0,pages):
        print ('Page#', i+1)
        pageNum = i+1
        writeTxt = 'Page# ' + str(pageNum) + '\n'
        file.write(writeTxt)
        pageIndex=10*i
        url = 'https://www.indeed.com/jobs?q=software%20engineer&l='+location+'%20CA&radius=10&start='+str(pageIndex)
        # print (url)
        html_page = urllib2.urlopen(url)
        soup = BeautifulSoup(html_page)
        counter=0
        for link in soup.findAll('a'):
            linkStr=str(link.get('href'))
            if '/company' in linkStr or '/rc' in linkStr or '/pagead' in linkStr:
                print (linkStr)
                actualLink='https://www.indeed.com'+linkStr
                file.write(actualLink+"\n")
                counter+=1
        print ('total: ', counter)
    file.close()
        
if __name__ == "__main__":
    location="Brea"
    pages=10
    getAllUrls(location, pages)