import pandas as pd
import statistics


class Trader:
    MA20 = []
    MA5 = []
    MA3 = []
    Boolean = []
    stock_info = []
    price = 0
    total = 0
    stock = 0

    def train(self, data: pd.core.frame.DataFrame):
        # TODO: 看要用高低收來算還是收盤
        self.MA5 = data["Close"].rolling(5).mean()
        self.MA20 = data["Close"].rolling(20).mean()
        self.stock_info = data

    def re_training(self, data: pd.core.series.Series):
        self.stock_info.loc[len(self.stock_info) + 1] = data
        self.MA5.loc[len(self.MA5) + 1] = self.stock_info.tail(5)['Close'].mean()
        self.MA20.loc[len(self.MA20) + 1] = self.stock_info.tail(20)['Close'].mean()

    def predict_action(self, data: pd.core.series.Series):
        action = 0
        print(f"Close price:{data['Close']}")
        self.MA3.append(data['Close'])
       
        if len(self.MA3) < 3:
            action = 0

        else:            
            print(f"MA3 price:{statistics.mean(self.MA3[-3:])}")
            if data['Close'] > statistics.mean(self.MA3[-3:]) and self.stock != 1: #昨日收盤價突破MA3，買進
                action = 1
            elif data['Close'] < statistics.mean(self.MA3[-3:]) and self.stock != -1:#昨日收盤價跌破MA3，賣出
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
    FEATURE_NAMES = ('Open', 'High', 'Low', 'Close')

    train_data = pd.read_csv(args.training, names=FEATURE_NAMES)
    trader = Trader()
    trader.train(train_data)

    testing_data = pd.read_csv(args.testing, names=FEATURE_NAMES)
    testing_data.drop(testing_data.tail(1).index, inplace=True)

    with open(args.output, 'w') as output_file:
        for (_, row) in testing_data.iterrows():
            # We will perform your action as the open price in the next day.
            output_file.writelines(f'{trader.predict_action(row)}\n')
            





