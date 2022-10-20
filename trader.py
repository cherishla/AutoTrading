import pandas as pd
import statistics
import pandas.core.frame
from xgboost import XGBClassifier

FEATURE_NAMES = ('open', 'high', 'low', 'close')


class Trader:
    NEXT_DAY = 1
    xgb = XGBClassifier()
    stock_info = pd.DataFrame(columns=FEATURE_NAMES)
    stock = 0
    MA3=[]

    def get_class(self, row: pd.core.series.Series):
        bound = 4
        rank = 0
        range_size = 2

        while bound > -3:
            if row['Ratio'] > bound:
                break
            rank += 1
            bound -= range_size
        return rank

    def train(self, data: pandas.core.frame.DataFrame):
        df = pd.DataFrame(data)
        df['Prediction'] = df['close'].shift(-self.NEXT_DAY)
        df['Ratio'] = (df['Prediction'] / df["close"] - 1) * 100
        df['Class'] = df.apply(self.get_class, axis=1)
        df_group_by_class = df.groupby('Class')
        map_class_to_count = dict()
        for name, group in df_group_by_class:
            map_class_to_count[name] = len(group)

        names = list(map_class_to_count.keys())
        values = list(map_class_to_count.values())
        print(names)
        print(values)
        print('---')
        from sklearn.model_selection import train_test_split
        train = df.iloc[:, 0:4]
        # y_train = df[['Class']]
        x_train, x_test, y_train, y_test = train_test_split(train, df['Class'], test_size=0.2)
        self.xgb.fit(x_train, y_train)
        print(x_test)
        print('訓練集: ', self.xgb.score(x_train, y_train))
        print('測試集: ', self.xgb.score(x_test, y_test))
        pass

    def re_train(self):
        pass

    def predict_action(self, data: pd.core.series.Series):
        self.stock_info.loc[len(self.stock_info) + 1] = data
        self.MA3.append(data['close'])
        df = pd.DataFrame(self.stock_info)
        predict = self.xgb.predict(df)
        action = 0

        if predict[-1] > 2 and self.stock != -1:
            action = -1
        elif predict[-1] < 3 and self.stock != 1:
            action = 1
        elif len(self.MA3) > 3:
            if data['close'] > statistics.mean(self.MA3[-3:]) and predict[-1] <= 2 and self.stock != 1: #昨日收盤價突破MA3，買進
                action = 1
            elif data['close'] < statistics.mean(self.MA3[-3:]) and predict[-1] <= 1 and self.stock != -1:#昨日收盤價跌破MA3，賣出
                action = -1

        self.stock += action
        return action


# You can write code above the if-main block.
if __name__ == "__main__":
    # You should not modify this part.
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--training", default="training_data.csv", help="input training data file name")
    parser.add_argument("--testing", default="testing_data.csv", help="input testing data file name")
    parser.add_argument("--output", default="output.csv", help="output file name")
    args = parser.parse_args()

    training_data = pd.read_csv(args.training, names=FEATURE_NAMES)

    trader = Trader()
    trader.train(training_data)

    testing_data = pd.read_csv(args.testing, names=FEATURE_NAMES)
    testing_data.drop(testing_data.tail(1).index, inplace=True)
    with open(args.output, 'w') as output_file:
        for (_, row) in testing_data.iterrows():
            # We will perform your action as the open price in the next day.
            output_file.writelines(f'{trader.predict_action(row)}\n')
            # this is your option, you can leave it empty.
            #trader.re_training(i)
