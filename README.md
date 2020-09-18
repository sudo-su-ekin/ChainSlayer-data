 # ChainSlayer Historical Data
![ChainSlayer]("icon transparent.png") 
Easy programmatic fetching of historical crypto market data from the ChainSlayer API. 

# Features

  - Support for 1m-1d candle data since ~1.6.2020.
  - 8 exchanges, 244 spot pairs.
  - Loads data automatically from the API.
  - Loaded data can be stored as .csv in the datasets folder.
  - Can also return 'pandas.DataFrame' object that can be piped to another script.


# How it works
You need to specify the trading pair you wish to get data from. The script automatically fetches data across 8 exchanges from the same pair and stores in as single .csv file or DataFrame object.

Parameters included to configure calls:

| Parameter | Desctiption |
| ------ | ------ |
| dataType | Currently only support for 'candle' |
| pair | E.g. ("BTC-USD"). You can use APIWrapper.getAllAssetPairs() for comprehensive list of all supported pairs. |
| dateFrom | Starting date - format: dd/mm/yyyy. |
| interval | 1m, 5m, 15m, 1h, 6h, 1d |
| limit | Paging response length, value between 10-100. 100 recommended. |
| direction | "ascending" or "descending". "ascending" currently tested and recommended. |
| dateUntil | End date - format: dd/mm/yyyy. |
| returnObjectType | "csv" or "dataframe". csv is saved in the "datasets" directory. dataframe returns dataframe object that can be piped to processing. |


### Usage

```sh
$ python3 CSData.py dataType, pair, dateFrom, interval, limit, direction, dateUntil, dateUntil, returnObjectType
```

Example call:
```sh
$ python3 CSData.py candle BTC-USD 01/09/2020 1h 100 ascending 15/09/2020 csv
```

# Contact us 
Our community is active in Discord. Please join SlayerChat to find out more.
[![Discord](Discord-Logo+Wordmark-Black)][https://discord.gg/5yBsY5P]
