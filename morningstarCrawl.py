from morningstarClass import Scrapper
import time

print('logging in ======================>')
sr = Scrapper()
time.sleep(2)
print('Gathering ETF codes list from Naver Finance...')
codes = sr.getCode()
print('\n\n')

# codes = ['174350', '245350', '261220', '105780', '152500', '139660', '280320', '244670', '307620', '140700', '205720', '234310', '304940', '267440', '310080', '292590', '292130', '105010', '251890', '309180']

noResult = []

for code in codes:
    try :
        time.sleep(2)
        print('Reading in code : ' + code + ' ...')
        sr.searchETF(code)
        print('Searching for results of ' + sr.getETFname() + '...')

        time.sleep(3)
        quote = sr.getQuote(code)
        print('Retrieving information from Quote tab...')
        time.sleep(2)
        performance = sr.getPerformance(code)
        trailing = sr.getTrailing(code)
        print('Retrieving information from Performance tab...')
        time.sleep(2)
        print('Retrieving information from Risk tab...')
        risk=sr.getRisk(code)

        print('Retrieving information from Portfolio tab...')
        time.sleep(2)
        asset=sr.getAssetAllo(code)
        style=sr.getStockStyle(code)
        sectors=sr.getSectors(code)
        sustain=sr.getSustain(code)
        holdings = sr.getHoldings(code)

        print('finished retrieval \nprinting results... \n\n')
        print('Loading information from Quote tab... \n')
        print(quote),print('\n')
        print('Loading information from Performance tab...\n')
        print(performance),print('\n'),print(trailing),print('\n')
        print('Loading information from Risk tab...\n')
        print(risk),print('\n')
        print('Loading information from Portfolio tab...\n')
        print(asset),print('\n'),print(style),print('\n'),print(sectors)
        print('\n'),print(sustain),print('\n'),print(holdings),print('\n')

        print('Number of crawled ETFs : ', codes.index(code)+1-len(noResult), '\n')
        print('\n\n')

    except Exception:
        print('No result found in Morningstar.com for : ' + code +'\n\n')
        noResult.append(code)
        pass

print(noResult)
