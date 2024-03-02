import yfinance as yf
import pandas_datareader.data as web
import pandas as pd
import datetime as dt

#make interactive
start10 = "2014-01-01"
end10 = "2023-12-31"

x = 3
search = []
#make the file be pulled from the website
SPNames = open("S&PFile.csv", "r")
lines = SPNames.readlines()
lines = lines[4:]
for line in lines[1:]:
    line = line.strip()
    columns = line.split(",")
    print(columns)
    TCKR = columns[2]
    if "Inc" in TCKR:
        TCKR = columns[3]
    elif TCKR != TCKR.upper():
        TCKR = columns[3]
    TCKR = TCKR.replace(".","-")
    print(TCKR)
    search.append(yf.download(TCKR, start10,end10))
    #data = open("SPDataStorage.csv", "w")
    #data.writelines(search)

    #data.writelines("\n"*3)
#print(search)
#data.writelines(search)
print(search)
df = pd.DataFrame(search)
df.to_csv("SPDataStorage.csv", mode = "w", index=False, header= False )
SPNames.close()
#data.close()




#print(df.head())