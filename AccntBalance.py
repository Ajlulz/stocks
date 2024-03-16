import csv
import yfinance as yf

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
                    opening_date = row[1]  # Second column from the CSV file
                    premium = row[6]  # Premium value
                    Quantity = row[3]
                    Price = row[4]
                    Currency = row[5]
                    Comission = row[7]
                    Fees = row[8]
                    ticker = self.get_ticker(symbol)
                    option_outcome = self.get_option_outcome(symbol)
                    expanded_symbol = self.expand_symbol(symbol, opening_date, premium, option_outcome, ticker)
                    expiration_date = expanded_symbol[2]  # Extracting expiration_date from expanded_symbol
                    bought_sold = ""
                    if option_outcome == "Assigned":
                        bought_sold = self.get_bought_sold(expiration_date, ticker)
                    expanded_symbol.append(bought_sold)  # Append bought_sold to expanded_symbol
                    industry = self.get_industry(ticker)  # Get industry using Yahoo Finance
                    expanded_symbol.append(industry)  # Append industry to expanded_symbol
                    option_trades.append(expanded_symbol)

        with open(self.output_file, "w", newline='') as output:
            writer = csv.writer(output)
            header = ["Ticker", "Opening Date", "Expiration Date", "Option Type", "Strike Price", "Premium",
                      "Option Outcome", "Bought/Sold", "Industry"]
            writer.writerow(header)
            writer.writerows(option_trades)

    def expand_symbol(self, symbol, opening_date, premium, option_outcome, ticker):
        first_digit_index = next((i for i, c in enumerate(symbol) if c.isdigit()), None)

        if first_digit_index is not None and first_digit_index > 0:
            ticker = symbol[:first_digit_index]
        else:
            ticker = "DEFAULT"

        year = symbol[first_digit_index: first_digit_index + 2]
        month = symbol[first_digit_index + 2: first_digit_index + 4]
        date = symbol[first_digit_index + 4: first_digit_index + 6]
        expiration_date = "/".join([month, date, year])
        option_type_mapping = {"C": "Call", "P": "Put"}
        option_type = option_type_mapping.get(symbol[first_digit_index + 6], "Unknown")
        strike_price = symbol[first_digit_index + 7:]

        return [ticker, opening_date, expiration_date, option_type, strike_price, premium, option_outcome]

    def get_option_outcome(self, symbol):
        with open(self.input_file, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if row[2] == symbol:
                    first_word = row[10].split()[0]
                    if first_word == "ASSIGNED":
                        return "Assigned"
                    elif first_word == "EXPIRED":
                        return "Expired"
        return "Unknown"

    def get_bought_sold(self, expiration_date, ticker):
        with open(self.input_file, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if row[2] == ticker:
                    expiration_date = expiration_date.replace("/", "-")  # Convert to the format in the CSV file
                    if expiration_date in row[10] or "EX-DIV DATE" in row[10]:  # Check if expiration date is in the 10th column
                        return row[6]  # Return the value from the 6th column
        return "Unknown"

    def get_ticker(self, symbol):
        first_digit_index = next((i for i, c in enumerate(symbol) if c.isdigit()), None)
        if first_digit_index is not None and first_digit_index > 0:
            return symbol[:first_digit_index]
        else:
            return "DEFAULT"

    def get_industry(self, ticker):
        try:
            stock = yf.Ticker(ticker)
            return stock.info['industry']
        except:
            return "Unknown"


processor = ProcessTrades()
processor.find_option_trades()

