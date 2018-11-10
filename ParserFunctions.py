from bs4 import BeautifulSoup
import urllib2
import re
import ResultClass
from collections import defaultdict
from datetime import datetime, timedelta
import csv


def buildFilter(filterFile):
    with open(filterFile, "r") as ins:
        array = []
        for line in ins:
            line=line.rstrip('\n')
            if '#' in line:
                continue
            if len(line) == 0:
                continue
            array.append(line)
    # for i in array:
    #     print (i)
    return array

def buildFilterDict(filterFile):
    with open(filterFile, "r") as ins:
        array = []
        for line in ins:
            line=line.rstrip('\n')
            if len(line) == 0:
                continue
            array.append(line)
    filterDict = {}
    currentKey=''
    for i in range(0,len(array)):
        if '*' in array[i]:
            if array[i] not in filterDict:
                filterDict[array[i]]=['']
                currentKey=array[i]
        else:
            filterDict[currentKey].append(array[i])
            
    for v in filterDict.values():
        if ('') in v:
            v.remove('')
    return filterDict


def readUrls(urlsFile):
    with open(urlsFile, "r") as ins:
        array = []
        for line in ins:
            line=line.rstrip('\n')
            if '#' in line:
                continue
            if len(line) == 0:
                continue
            array.append(line)
    # for i in array:
    #     print (i)
    return array

def ReadHtml(url, filters):
    
    result=ResultClass.Result()
    page_html = urllib2.urlopen(url)
    soup = BeautifulSoup(page_html)
    # print (url)
    
    companyName = soup.find_all("div", class_="icl-u-lg-mr--sm icl-u-xs-mr--xs")
    try:
        result.companyName = companyName[0].text
    except:
        result.companyName = ''
    
    
    jobTitle = soup.find_all("h3", class_="icl-u-xs-mb--xs icl-u-xs-mt--none jobsearch-JobInfoHeader-title")
    try:
        result.jobTitle= jobTitle[0].text
    except:
        result.jobTitle=''
        
        
    location = soup.title.string
    try:
        result.jobTitle= soup.title.string
        result.location= getLocation(location) #get between-
    except:
        result.location=''
    
    
    footer=soup.find_all("div", class_="jobsearch-JobMetadataFooter")
    try:
        result.postedOn=postDaysAgo(footer[0].text)
        
    except:
        result.postedOn=''
    
    result.url=url
    if 'pagead' in url:
        result.isAd=True
    result.enterDate=(datetime.now()- timedelta(hours=8)).strftime("%m/%d/%Y")

    description = soup.find_all("div", class_="jobsearch-JobComponent-description icl-u-xs-mt--md")
    description= str(description).lower()
    
    result.experience=findExperience(description)
    
    
    for (key,values) in filters.items():
        for value in values:
            value=value.lower()
            inHtml = value in description
            # print (key, value, inHtml)
            if inHtml:
                if 'headHunter' in key:
                    result.headHunter=True
                if 'noH1b' in key:
                    result.isOnNOH1BList=True
                if 'jobType' in key:
                    result.jobType=value
                if 'skillSets' in key:
                    result.skillSets.append(value)
                if 'visaKeyword' in key:
                    result.visaKeywords.append(value)
                if 'notPrefer' in key:
                    result.notPrefer.append(value)
    
    return result
    
def postDaysAgo(footerStr):
    try:
        postedOn=footerStr[:footerStr.index("days ago")] + "days ago"
    except:
        postedOn=footerStr[:footerStr.index("day ago")] + "day ago"
    return postedOn
    
    
def getLocation(locationStr):
    # "Sr Software Engineer I - Fullerton, CA 92833 - Indeed.com"
    c='-'
    index=[pos for pos, char in enumerate(locationStr) if char == c]
    return locationStr[index[0]+1:index[1]]

def export(rowList):
    with open('filename', 'wb') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(rowList)

def findExperience(description):
    try:
        test = re.match("\d+\+?\s+(.*)(?:months?|years?)", description)
        return str(test.group())
    except:
        return ''
    # if test:
    #   print "matchObj.group() : ", test.group()
    #   print "matchObj.group(1) : ", test.group(1)
    #   print "matchObj.group(2) : ", test.group(2)
    # else:
    #   print "No match!!"
def buildDataRows(results):
    rows=[]
    header=['Company', 'JobTitle', 'isHeadHunter', 'Location', 'PostedOn', 'isOnNOH1BList',\
            'VisaKeywords', 'Applied', 'isAd', 'Experience', 'JobType',\
            'NotPrefer', 'SkillSets', 'EnterDate', 'url']
    rows.append(header)
    
    for r in results:
        row=[r.companyName.encode('utf8'), r.jobTitle.encode('utf8'), r.isHeadHunter, \
            r.location.encode('utf8'), r.postedOn.encode('utf8'), r.isOnNOH1BList, \
            str(r.visaKeywords).encode('utf8'), r.applied, r.isAd, \
            r.experience.encode('utf8'), str(r.jobType).encode('utf8'), \
            str(r.notPrefer).encode('utf8'), str(r.skillSets).encode('utf8'), r.enterDate.encode('utf8'), r.url.encode('utf8')]
        rows.append(row)
    return rows