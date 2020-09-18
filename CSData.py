from candleDataframeFetcher import candleDataframeFetcher
from dataframeImputation import imputateCandleDataframe
import pandas as pd
import argparse


class Candles:

    def combineDatafames(self, candleDataframes):
        mergedDataframes                                = pd.DataFrame(columns=['timestamp'])
        for dataframe in candleDataframes:
            mergedDataframes                            = pd.merge(mergedDataframes, candleDataframes[dataframe], on='timestamp', how='outer')
        return mergedDataframes
            
    
    def getCandles(self):
        candles = candleDataframeFetcher(pair           =self.PAIR, 
                                         dateFrom       =self.DATEFROM, 
                                         interval       =self.INTERVAL, 
                                         limit          =self.LIMIT, 
                                         direction      =self.DIRECTION, 
                                         dateUntil      =self.DATEUNTIL)
        
        mergedDFs                                       = self.combineDatafames(candles.DATAFRAMES)
        mergedDFs                                       = mergedDFs.sort_values('timestamp', ascending=True)
        
        #Fill missing values (currently linear interpolation)
        imp                                             = imputateCandleDataframe()
        filledDFs                                       = imp.imputateDataframe(mergedDFs)
        
        return filledDFs
    
    def __init__(self, pair, dateFrom, interval, limit, direction, dateUntil):
        self.PAIR                                       = pair
        self.DATEFROM                                   = dateFrom
        self.INTERVAL                                   = interval
        self.LIMIT                                      = limit
        self.DIRECTION                                  = direction
        self.DATEUNTIL                                  = dateUntil
            
def main(dataType, pair, dateFrom, interval, limit, direction, dateUntil, returnObjectType):
    if dataType                                         == 'candle':
        candles = Candles(pair, dateFrom, interval, limit, direction, dateUntil)
        if returnObjectType                             == 'dataframe':
            return candles.getCandles()
        else:
            start                                       = dateFrom.replace('/', '')
            end                                         = dateUntil.replace('/', '')
            return candles.getCandles().to_csv('datasets/'+pair+'-'+start+'-'+end+'-'+interval+'.csv')
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch data from the ChainSlayer API. Returned either in csv or dataframe object that can be piped to the next script.')
    
    parser.add_argument('dataType', help='Enter "candle". Support for trades coming shortly.')
    parser.add_argument('pair', help='E.g. ("BTC-USD"). Use APIWrapper.getAllAssetPairs() for comprehensive list.')
    parser.add_argument('dateFrom', help='Starting date - format: dd/mm/yyyy. For convenience we convert the date formats to timestamp automatically. No hours, minutes or seconds supported yet.')
    parser.add_argument('interval', help=('1m, 5m, 15m, 1h, 6h, 1d'))
    parser.add_argument('limit', help='Paging response length, value between 10-100. Use 100 if not sure.')
    parser.add_argument('direction', help='"ascending" or "descending". Use "ascending" for now.')
    parser.add_argument('dateUntil', help='End date - format: dd/mm/yyyy. For convenience we convert the date formats to timestamp automatically. No hours, minutes or seconds supported yet.')
    parser.add_argument('returnObjectType', help='"csv" or "dataframe". csv is saved in the same directory as the script (remember write permissions). dataframe returns dataframe object that can be piped to processing.')
    
    args = parser.parse_args()
    main(args.dataType, args.pair, args.dateFrom, args.interval, args.limit, args.direction, args.dateUntil, args.returnObjectType)
    
    
    