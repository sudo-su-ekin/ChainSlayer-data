import APIWrapper as wrapper
import pandas as pd
import datetime

class candleDataframeFetcher:
    
    '''Fethes a dict of dataframes consisting of candle data. '''

    def getExchangesWithPair(self):
        exchanges = []
        for exchange in wrapper.getExchanges():
            if wrapper.marketInExchange(self.PAIR, exchange):
                exchanges.append(exchange)
        return exchanges

    def getDataFrame(self, exchange):
        df = pd.DataFrame(columns = ['timestamp', 
                                     exchange+'-appTimestamp', 
                                     exchange+'-id', 
                                     exchange+'-uid', 
                                     exchange+'-assetPair', 
                                     exchange+'-instrumentClass', 
                                     exchange+'-exchangeId', 
                                     exchange+'-interval', 
                                     exchange+'-type', 
                                     exchange+'-filled', 
                                     exchange+'-high', 
                                     exchange+'-low', 
                                     exchange+'-open', 
                                     exchange+'-close', 
                                     exchange+'-average', 
                                     exchange+'-middle', 
                                     exchange+'-volume', 
                                     exchange+'-tradeCount', 
                                     exchange+'-eventType'])
                   
        timestampInRange                    = True
        isFirstRun                          = True
        

        
        def processResponse(response):
            
            def checkTimestampInRange(timestamp):
                if hasattr(self, 'UNTIL'):
                    return timestamp < wrapper.convertDateToTimestamp(self.UNTIL)
                return True
            
            nonlocal timestampInRange
            for item in response['items']:
                if checkTimestampInRange(item['timestamp']):
                    values                  = list(item.values())
                    values[0]               = datetime.datetime.utcfromtimestamp(values[0]/1000)
                    values[1]               = datetime.datetime.utcfromtimestamp(values[1]/1000)
                    values[10]              = float(values[10])
                    values[11]              = float(values[11])
                    values[12]              = float(values[12])
                    values[13]              = float(values[13])
                    values[14]              = float(values[14])
                    values[15]              = float(values[15])
                    values[16]              = float(values[16])
                    values[17]              = int(values[17])
                    df.loc[len(df)]         = values
                else:
                    timestampInRange        = False
                    break
        
        while timestampInRange:
            if isFirstRun                   == True:
                response                    = wrapper.getCandle(self.PAIR, exchange, self.INTERVAL, timestampFrom=self.FROM, timestampTo=self.UNTIL, limit=self.LIMIT, direction=self.DIRECTION)
                processResponse(response)
                if timestampInRange         == False:
                    return df
                isFirstRun                  = False
                paging                      = response['lastEvaluatedKey']
                
            else:
                response                    = wrapper.getCandle(self.PAIR, exchange, self.INTERVAL, timestampFrom=self.FROM, timestampTo=self.UNTIL, limit=self.LIMIT, direction=self.DIRECTION, exclStartKey=paging)
                if 'lastEvaluatedKey' in response.keys():
                    processResponse(response)
                    if timestampInRange     == False:
                        return df
                    paging                  = response['lastEvaluatedKey']
                
                else:
                    processResponse(response)
                    if timestampInRange     == False:
                        return df
                    return df
                
            
            

    ## Constants
    # PAIR                  e.g. 'BTC-USD'
    # FROM                  'dd/mm/yyyy' (mandatory)
    # UNTIL                 'dd/mm/yyyy' (optional) (not supported yet) 
    # INTERVAL              '1m', '5m', '15m', '1h', '6h', '1d', '1wk'
    # LIMIT                 10 to 100
    # DIRECTION             'ascending' or 'descending'
    def __init__(self, pair, dateFrom, interval, limit, direction, dateUntil=None):
        self.PAIR                           = pair
        self.FROM                           = dateFrom
        if dateUntil != None:
            self.UNTIL                      = dateUntil
        self.INTERVAL                       = interval
        self.LIMIT                          = limit
        self.DIRECTION                      = direction
        self.DATAFRAMES        = {}
    
        exchangesWithPair                   = self.getExchangesWithPair()
        
        for item in exchangesWithPair:
            self.DATAFRAMES[str(item+self.PAIR)] = self.getDataFrame(item)

    
#new = candleDataframeFetcher(pair='BTC-USD', dateFrom='01/08/2020', interval='1h', limit=100, direction='ascending', dateUntil='16/08/2020')
#dataframes = new.DATAFRAMES
#print('done')