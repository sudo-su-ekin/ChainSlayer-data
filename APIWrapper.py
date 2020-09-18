## Imports
import requests
import time 
import datetime 

# Endpoint constants
URL = 'https://api.mdata.chainslayer.io/'
HEADERS = {'X-API-Key': '3d38650577db4f6e8a7040220c3b25039b2ab137da7c4c30b53d37480ba8ba1b'}


ENDPOINTS = {
    'exchanges':    URL+'info/exchanges/',
    'assetPairs':   URL+'info/assetPairs/',
    'candles':      URL+'data/candles/'
    
}

# Returns list of supported exchanges
def getExchanges():
    try:
        r = requests.get(ENDPOINTS.get('exchanges'), headers=HEADERS).json()
        return r
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

# Return all supported asset pairs
def getAllAssetPairs():
    try:
        r = requests.get(ENDPOINTS.get('assetPairs'), headers=HEADERS).json()
        return r
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

# Get all supported markets for a single exchange
def getExchangeAssetPairs(exchangeId):
    try:
        r = requests.get(ENDPOINTS.get('exchanges')+exchangeId+'/assetPairs', headers=HEADERS).json()
        return r
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

# Check if market is contained in an exchange
def marketInExchange(market, exchange):
    if market in getExchangeAssetPairs(exchange):       return True
    else:                                               return False
    
# Format: dd/mm/yyyy   
def convertDateToTimestamp(date):
    return int(time.mktime(datetime.datetime.strptime(date, "%d/%m/%Y").timetuple())* 1000)

# Candles path parameters   assetPair:      Asset pair in the given market
#                           exchangeId:     Exchange ID
#                           interval:       [1m, 5m, 15m, 1h, 6h, 1d, 1wk]
#
# Candles query parameters  timestampFrom:  date as dd/mm/yyyy 
#                           timestampTo:    date as dd/mm/yyyy 
#                           limit:          Number of items returned [10-100]. Default 10
#                           exclStartKey:   The value of the lastEvaluatedKey property of the previous 'page' of results
#                           direction:      Return order of items ['Ascending' or 'Descending']. Default 'Descending'
def getCandle(assetPair, exchangeId, interval, timestampFrom=None, timestampTo=None, limit=None, direction=None, exclStartKey=None):
    path = ENDPOINTS.get('candles')+'{}/{}/{}'.format(assetPair, exchangeId, interval)
    params = {}
    
    if timestampFrom                    != None:
        _timestampFrom                  = convertDateToTimestamp(timestampFrom)
        params['timestampFrom']         = _timestampFrom
    if timestampTo                     != None:
        _timestampTo                    = convertDateToTimestamp(timestampTo)
        params['timestampTo']           = _timestampTo
    if timestampFrom                    != None:
        _limit                          = limit
        params['limit']                 = _limit
    if exclStartKey                     != 'a':
        _exclStartKey                   = exclStartKey
        params['exclStartKey']          = _exclStartKey
    if direction                        != None:
        _direction                      = direction
        params['direction']             = _direction
    
    try:
        rep = requests.get(path, headers=HEADERS, params=params ).json()
        print(str(rep['items'][0]['exchangeId'])+':'+str(rep['items'][0]['timestamp'])+':'+str(rep['items'][len(rep['items'])-1]['timestamp']))
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    
    # Whenever we have quoteVolumes across entire dataset remove this horrible hack #
    for element in rep['items']:
        if 'quoteVolume' in element:
            del element['quoteVolume']
    # Remove the above #
    
    return rep
    
#print(getExchanges())
#print(getAllAssetPairs())
#print(getExchangeAssetPairs('binance'))
#print(marketInExchange('BTC-EUR', 'binance'))
#print(marketInExchange('BCH-EUR', 'binance'))
#print(convertDateToTimestamp('20/01/2020'))
#print(getCandle('BTC-EUR', 'binance', '6h', timestampFrom=('18/06/2020'), timestampTo=('20/06/2020'), limit=(10), direction=('ascending')))


