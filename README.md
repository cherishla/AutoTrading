## xGBoost 分類(含三日線)
> python trader.py --training training_data.csv --testing testing_data.csv  --output output.csv

* 預測隔天收盤落在哪個group，來決定是否要買進或賣出
* 利用漲幅來計算，台股漲幅落在正負10%
* 觀察0050的漲幅大概落在-4%~4%中，可參照[ratio_data.csv](ratio_data.csv)
* 類別從-3 開始計算，調教參數時，在range = 2時，雖然測試分數沒有很高，但計算出來的損益數值比較好  
* 搭配三日線來做決策


## 3日線
> python trader2.py --training training_data.csv --testing testing_data.csv  --output output.csv

* 沒有利用ML直接坐回測
* 因為資料量過少，嘗試1~5日線中，只有3日線損益比較好

## xGBoost  (不含三日線)
> python trader3.py --training training_data.csv --testing testing_data.csv  --output output.csv








