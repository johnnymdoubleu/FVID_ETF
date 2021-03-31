from ipoClass import Scrapper
import time


print('Wait while loading ======================>')
print('Opening www.38.co.kr')
print('Opening Investing.com')
sr = Scrapper()
time.sleep(1)

sr.open38()

time.sleep(0.5)
data = []
for i in range(0,2):
    ipo =sr.getIPO()
    print("mapping to NAVER finance")
    code = sr.searchNaver(ipo)
    for j in range(0, len(ipo)) :
        mapping = {ipo[j] : code[j]}
        data.append(mapping)
    print("turning to page %s"%sr.nextPage())

print('\n\n')
print(data)

sr.shutdown()
