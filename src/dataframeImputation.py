import pandas as pd


class imputateCandleDataframe:
    
    # Filled by interpolating the column.
    def fillMissingValues(self, column):
        c = column.interpolate()
        return c.values.tolist()
        
    #Simple linear intepolation is used here. Adjust accordingly
    def imputateDataframe(self, candleDataframe):
        df = candleDataframe
        for column in list(df.columns):
            for item in self.COLUMNSTOIMPUTATE:
                if item in column:
                    df[column].interpolate(inplace=True)
        return df      
    
    def __init__(self):
        self.COLUMNSTOIMPUTATE = ['high', 'low', 'open', 'close', 'average', 'middle', 'volume', 'tradecount']
        
        
        
    
        
