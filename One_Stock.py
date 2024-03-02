import yfinance as yf
import pandas as pd
import csv
from datetime import datetime

CSVFile = open("first_data.csv","w")
CSVFile.writelines("TCKR" + "," + " 10yr Avg. Growth" + "," " Portfolio%" + "\n")

JanStartDate = "2013-01-01"
JanEndDate = "2013-01-05"
DecStartDate = "2013-12-25"
DecEndDate = "2013-12-31"





SPNames = open("S&PFile.csv", "r")
lines = SPNames.readlines()
lines = lines[4:]

line = lines[1].strip()
columns = line.split(",")
TCKR = columns[2]
weight = columns[3]
if TCKR != TCKR.upper():
    TCKR = columns[3]
    weight = columns[4]

# for line in lines[2:]:
#     line = line.strip()
#     columns = line.split(",")

growthList = []
for count in range(10):
    data = yf.download(TCKR, JanStartDate, JanEndDate)
    data2 = yf.download(TCKR, DecStartDate, DecEndDate)
    open_price = data.iloc[0]["Open"]
    close_price = data2.iloc[-1]["Close"]
    growth = (close_price-open_price)/open_price
    # Export DataFrame to CSV
    #print(open_price)
    #print(close_price)
    #print(growth)
    growthList.append(growth)
    print(growthList)

    date_object1 = datetime.strptime(JanStartDate, "%Y-%m-%d")
    new_date_object1 = date_object1.replace(year=date_object1.year + 1)
    JanStartDate = new_date_object1.strftime("%Y-%m-%d")

    date_object2 = datetime.strptime(JanEndDate, "%Y-%m-%d")
    new_date_object2 = date_object2.replace(year=date_object2.year + 1)
    JanEndDate = new_date_object2.strftime("%Y-%m-%d")

    date_object3 = datetime.strptime(DecStartDate, "%Y-%m-%d")
    new_date_object3 = date_object3.replace(year=date_object3.year + 1)
    DecStartDate = new_date_object3.strftime("%Y-%m-%d")

    date_object4 = datetime.strptime(DecEndDate, "%Y-%m-%d")
    new_date_object4 = date_object4.replace(year=date_object4.year + 1)
    DecEndDate = new_date_object4.strftime("%Y-%m-%d")
    count += 1

averagedGrowth = sum(growthList)/len(growthList)
formattedAGrowth = "{:.2%}".format(averagedGrowth)
print(averagedGrowth)
print(formattedAGrowth)
CSVFile = open("first_data.csv","a")
CSVFile.writelines(TCKR + ", " + formattedAGrowth + ", " + weight + "\n")
SPNames.close()