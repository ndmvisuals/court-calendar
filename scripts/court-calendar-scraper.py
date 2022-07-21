### Libraries
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import requests
import re
from datetime import datetime
import pathlib

### Download Page and Make Soup
url = 'https://ecf.dcd.uscourts.gov/cgi-bin/CourtSched.pl'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')


### Grab Table and Date Information

table = soup.find("table", {"id":"ts"}) # html table


date = soup.find("b").text.split(":")[1] # date 

date = " ".join(date.split())
formatted_date = datetime.strptime(date, '%A, %B %d, %Y')



### Scrape HTML and Save as Dataframe

ls_table_tr = table.find_all("tr")
rows = []
for tr in ls_table_tr:
    row = []
    count = 0
    for child in tr.children:
        if count == 0:
            result = child.text.replace('\n', '')
            if result != "":
                 row.append(result)
        else: 

            try:
                row.append(child.text.replace('\n', ''))
            except:
                continue

    count = count + 1
    if len(row) > 0:
        rows.append(row)
df = pd.DataFrame(rows[1:], columns = rows[0])

### Format DataFrame

df[['Case Number', 'Title']] = df['Case Number and Title'].str.split(':', expand=True)
df["Date"] = formatted_date

### Save Data Frame


file_date = formatted_date.strftime("%Y-%m-%d")
path = pathlib.Path(f"../data/days/{file_date}-court_calendar.csv")
df.to_csv(path, index = False)