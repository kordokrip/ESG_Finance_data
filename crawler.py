import sys
import requests
import time
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QProgressBar, QFileDialog, QMessageBox, QComboBox
from PyQt5.QtCore import Qt

class YahooFinanceApp(QWidget):
    def __init__(self):
        super().__init__()
        self.api_key = " API key"  # API key
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Ticker input fields
        self.ticker_inputs = []
        for i in range(10):
            ticker_input = QLineEdit(self)
            ticker_input.setPlaceholderText(f'Ticker {i+1}')
            layout.addWidget(ticker_input)
            self.ticker_inputs.append(ticker_input)

        # ComboBoxes for selecting year range
        self.start_year_combo = QComboBox(self)
        self.start_year_combo.addItems(['2020', '2021', '2022', '2023'])
        layout.addWidget(QLabel("Start Year"))
        layout.addWidget(self.start_year_combo)

        self.end_year_combo = QComboBox(self)
        self.end_year_combo.addItems(['2020', '2021', '2022', '2023'])
        layout.addWidget(QLabel("End Year"))
        layout.addWidget(self.end_year_combo)

        # Progress Bar for status
        self.progress_bar = QProgressBar(self)
        layout.addWidget(self.progress_bar)

        # Fetch data button
        self.fetch_button = QPushButton('Fetch Data & Save as Excel', self)
        self.fetch_button.clicked.connect(self.fetch_data)
        layout.addWidget(self.fetch_button)

        # Save path selection button
        self.save_path_button = QPushButton('Select Save Path', self)
        self.save_path_button.clicked.connect(self.choose_save_directory)
        layout.addWidget(self.save_path_button)

        self.save_path_label = QLabel('Save path not selected', self)
        layout.addWidget(self.save_path_label)

        self.setLayout(layout)

    def choose_save_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Choose Save Directory")
        if directory:
            self.save_path_label.setText(f'Save Path: {directory}')
            self.save_directory = directory

    def fetch_data(self):
        tickers = [ticker.text().upper() for ticker in self.ticker_inputs if ticker.text().strip()]
        if not tickers:
            QMessageBox.warning(self, "Error", "Please enter at least one ticker.")
            return

        start_year = int(self.start_year_combo.currentText())
        end_year = int(self.end_year_combo.currentText())

        start_timestamp = int(time.mktime(time.strptime(f"{start_year}-01-01", "%Y-%m-%d")))
        end_timestamp = int(time.mktime(time.strptime(f"{end_year}-12-31", "%Y-%m-%d")))

        self.progress_bar.setValue(0)
        total_tickers = len(tickers)

        results = []
        for i, ticker in enumerate(tickers):
            try:
                # Fetching stock price history
                price_history_url = f"https://yahoo-finance-api-data.p.rapidapi.com/symbol/price-history"
                querystring = {
                    "symbol": ticker,
                    "from": start_timestamp,
                    "to": end_timestamp,
                    "type": "price_history",
                    "frequency": "1d",
                    "limit": "10"
                }
                headers = {
                    "X-RapidAPI-Key": self.api_key,
                    "X-RapidAPI-Host": "yahoo-finance-api-data.p.rapidapi.com"
                }
                response = requests.get(price_history_url, headers=headers, params=querystring)

                if response.status_code == 200:
                    data = response.json()
                    result = self.process_data(ticker, data)
                    results.append(result)
                else:
                    QMessageBox.warning(self, "Error", f"Failed to retrieve data for {ticker}. Status code: {response.status_code}")
                time.sleep(1)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Data fetch error: {str(e)}")

            progress = int(((i + 1) / total_tickers) * 100)
            self.progress_bar.setValue(progress)

        if results and hasattr(self, 'save_directory'):
            self.save_to_excel(results)

    def process_data(self, ticker, data):
        try:
            # Stock price data
            price_data = data.get('data', [])
            close_prices = {}

            if price_data:
                for price in price_data:
                    timestamp = pd.to_datetime(price.get('timestamp'), unit='s')
                    if timestamp.month == 12 and timestamp.day == 31:  # Year-end data
                        close_prices[timestamp.year] = price.get('close', 'N/A')

            # Fetch additional data like shares issued, market cap, financials from other endpoints
            shares_issued = self.fetch_shares_issued(ticker)
            financial_data = self.fetch_financial_data(ticker)

            # Combine results
            result = {
                'Ticker': ticker,
                '2020 Closing Price': close_prices.get(2020, 'N/A'),
                '2021 Closing Price': close_prices.get(2021, 'N/A'),
                '2022 Closing Price': close_prices.get(2022, 'N/A'),
                '2023 Closing Price': close_prices.get(2023, 'N/A'),
                'Shares Issued': shares_issued,
                'Market Cap': financial_data.get('market_cap', 'N/A'),
                'EBITDA': financial_data.get('ebitda', 'N/A'),
                'Revenue': financial_data.get('revenue', 'N/A'),
                'Net Debt': financial_data.get('net_debt', 'N/A'),
                'Total Debt': financial_data.get('total_debt', 'N/A'),
                'EPS': financial_data.get('eps', 'N/A'),
                'Industry': financial_data.get('industry', 'N/A'),
                'Employee Count': financial_data.get('employees', 'N/A'),
                'ESG Score': financial_data.get('esg_score', 'N/A')
            }

            return result

        except Exception as e:
            return {'Ticker': ticker, 'Error': f"Data parsing error: {str(e)}"}

    def fetch_shares_issued(self, ticker):
        # Additional endpoint for shares issued
        try:
            shares_url = f"https://yahoo-finance-api-data.p.rapidapi.com/symbol/shares-outstanding"
            querystring = {"symbol": ticker}
            headers = {
                "X-RapidAPI-Key": self.api_key,
                "X-RapidAPI-Host": "yahoo-finance-api-data.p.rapidapi.com"
            }
            response = requests.get(shares_url, headers=headers, params=querystring)
            if response.status_code == 200:
                shares_data = response.json()
                return shares_data.get('sharesOutstanding', 'N/A')
            else:
                return 'N/A'
        except:
            return 'N/A'

    def fetch_financial_data(self, ticker):
        # Additional endpoint for financials (market cap, EBITDA, etc.)
        try:
            financial_url = f"https://yahoo-finance-api-data.p.rapidapi.com/symbol/financials"
            querystring = {"symbol": ticker}
            headers = {
                "X-RapidAPI-Key": self.api_key,
                "X-RapidAPI-Host": "yahoo-finance-api-data.p.rapidapi.com"
            }
            response = requests.get(financial_url, headers=headers, params=querystring)
            if response.status_code == 200:
                financial_data = response.json()
                return {
                    'market_cap': financial_data.get('marketCap', 'N/A'),
                    'ebitda': financial_data.get('ebitda', 'N/A'),
                    'revenue': financial_data.get('totalRevenue', 'N/A'),
                    'net_debt': financial_data.get('netDebt', 'N/A'),
                    'total_debt': financial_data.get('totalDebt', 'N/A'),
                    'eps': financial_data.get('eps', 'N/A'),
                    'industry': financial_data.get('industry', 'N/A'),
                    'employees': financial_data.get('fullTimeEmployees', 'N/A'),
                    'esg_score': financial_data.get('esgScore', 'N/A')
                }
            else:
                return {}
        except:
            return {}

    def save_to_excel(self, results):
        df = pd.DataFrame(results)
        save_path = f"{self.save_directory}/Financial_Data.xlsx"
        df.to_excel(save_path, index=False)
        QMessageBox.information(self, "Complete", f"Data saved to {save_path}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = YahooFinanceApp()
    ex.show()
    sys.exit(app.exec_())
