import csv

class ProcessTrades:
    def __init__(self):
        self.input_file = 'sampledata.csv'
        self.output_file = 'output.csv'

    def find_option_trades(self):
        option_trades = []

        with open(self.input_file, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if row[10] == "YOU SOLD OPENING TRANSACTION":
                    symbol = row[2]
                    expanded_symbol = self.expand_symbol(symbol)
                    option_trade_row = expanded_symbol
                    option_trades.append(option_trade_row)

        with open(self.output_file, "w", newline='') as output:
            writer = csv.writer(output)
            header = ["Ticker", "Year", "Month", "Date", "Option Type", "Strike Price"]
            writer.writerow(header)
            writer.writerows(option_trades)

    def expand_symbol(self, symbol):
        first_digit_index = next((i for i, c in enumerate(symbol) if c.isdigit()), None)

        if first_digit_index is not None and first_digit_index > 0:
            ticker = symbol[:first_digit_index]
        else:
            ticker = "DEFAULT"

        year = symbol[first_digit_index: first_digit_index + 2]
        month = symbol[first_digit_index + 2: first_digit_index + 4]
        date = symbol[first_digit_index + 4: first_digit_index + 6]
        option_type = symbol[first_digit_index + 6]
        strike_price = symbol[first_digit_index + 7:]

        return [ticker, year, month, date, option_type, strike_price]


processor = ProcessTrades()
processor.find_option_trades()
