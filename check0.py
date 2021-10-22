import os
import glob
import pandas as pd

alphabet = ""
path = glob.glob(f'A:\\GitHub\\newsCurator\\BusinessExtract\\{alphabet}*\\*\\*.txt')


parseError = []

for i in path:
    if os.path.getsize(i) == 0:
        infos = i.split("\\")
        ticker = infos[4]
        cik = infos[-1][0:10]
        year = infos[-1][11:13]
        filename = infos[-1]
        parseError.append([ticker, cik, year, filename])


df = pd.DataFrame(parseError, columns = ["ticker","cik","year","filename"])
df.to_csv(f"A:\\GitHub\\newsCurator\\errorList\\parseError_{alphabet}.csv", encoding='utf-8-sig', index=False)
