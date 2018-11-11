import ParserFunctions
import csv
import time
from pymongo import MongoClient


if __name__ == "__main__":
    
    filterFile='filter'
    filterDict = ParserFunctions.buildFilterDict(filterFile)

    client = MongoClient()
    client = MongoClient('localhost', 27017)
    jobDB = client["jobDB"]
    jobRow = jobDB["jobRow"]

    # batch
    fileName = 'Riverside-urls'
    urls = ParserFunctions.readUrls(fileName)
    distinct_urls = set(urls)
    # print myset
    results=[]
    counter=0
    for url in distinct_urls:
        counter+=1
        print (counter)
        time.sleep(2)
        result=ParserFunctions.ReadHtml(url, filterDict)
        results.append(result)
        resultDict=ParserFunctions.buildDataDict(result)
        jobRow.insert_one(resultDict)
        if counter >5: break

    # rows=ParserFunctions.buildDataRows(results)
    # exportCsv=fileName+".csv"
    # myFile = open(exportCsv, 'w')
    # with myFile:
    #     writer = csv.writer(myFile)
    #     writer.writerows(rows)
    # print("Writing complete")