import ParserFunctions
import csv
import time

if __name__ == "__main__":
    
    filterFile='filter'
    filterDict = ParserFunctions.buildFilterDict(filterFile)

    # batch
    fileName = 'Brea-urls'
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

    rows=ParserFunctions.buildDataRows(results)
    
    exportCsv=fileName+".csv"
    myFile = open(exportCsv, 'w')
    with myFile:
        writer = csv.writer(myFile)
        writer.writerows(rows)
         
    print("Writing complete")