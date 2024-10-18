import sys
import requests
import time
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QProgressBar, QFileDialog, QMessageBox, QComboBox
from PyQt5.QtCore import Qt

class YahooFinanceApp(QWidget):
    def __init__(self):
        super().__init__()
        self.api_key = "YOUR_API_KEY"  # API key 입력
        self.initUI()

    def initUI(self):
        # UI 초기화 설정
        # Initializes the User Interface (UI) layout with input fields, buttons, and progress bars.
        layout = QVBoxLayout()

        # 티커 입력 창을 10개까지 제공
        # Provides 10 fields for the user to input stock tickers.
        self.ticker_inputs = []
        for i in range(10):
            ticker_input = QLineEdit(self)
            ticker_input.setPlaceholderText(f'Ticker {i+1}')  # 입력란 설명 표시
            layout.addWidget(ticker_input)
            self.ticker_inputs.append(ticker_input)

        # 연도 선택 콤보박스 추가
        # Adds dropdowns for selecting the start and end year for data retrieval.
        self.start_year_combo = QComboBox(self)
        self.start_year_combo.addItems(['2020', '2021', '2022', '2023'])
        layout.addWidget(QLabel("Start Year 선택"))  # 시작 연도 라벨
        layout.addWidget(self.start_year_combo)

        self.end_year_combo = QComboBox(self)
        self.end_year_combo.addItems(['2020', '2021', '2022', '2023'])
        layout.addWidget(QLabel("End Year 선택"))  # 끝 연도 라벨
        layout.addWidget(self.end_year_combo)

        # 진행 상태 표시를 위한 Progress Bar 추가
        # Adds a progress bar to show data retrieval progress.
        self.progress_bar = QProgressBar(self)
        layout.addWidget(self.progress_bar)

        # 데이터 수집 버튼 추가
        # Adds a button to trigger the data fetch process.
        self.fetch_button = QPushButton('Fetch Data & Save as Excel', self)
        self.fetch_button.clicked.connect(self.fetch_data)
        layout.addWidget(self.fetch_button)

        # 저장 경로 선택 버튼 추가
        # Adds a button to let the user select where to save the Excel file.
        self.save_path_button = QPushButton('Select Save Path', self)
        self.save_path_button.clicked.connect(self.choose_save_directory)
        layout.addWidget(self.save_path_button)

        self.save_path_label = QLabel('Save path not selected', self)
        layout.addWidget(self.save_path_label)

        self.setLayout(layout)

    def choose_save_directory(self):
        # 파일 저장 경로 선택 다이얼로그
        # Opens a dialog for the user to choose where to save the Excel file.
        directory = QFileDialog.getExistingDirectory(self, "Choose Save Directory")
        if directory:
            self.save_path_label.setText(f'Save Path: {directory}')
            self.save_directory = directory

    def fetch_data(self):
        # 티커 입력값을 읽고 연도 선택 및 데이터 수집을 수행
        # Reads the ticker inputs and year selections, then retrieves data from the API.
        tickers = [ticker.text().upper() for ticker in self.ticker_inputs if ticker.text().strip()]
        if not tickers:
            QMessageBox.warning(self, "Error", "Please enter at least one ticker.")
            return

        # 연도별로 데이터 요청 기간 설정
        # Converts the selected years into timestamps for API requests.
        start_year = int(self.start_year_combo.currentText())
        end_year = int(self.end_year_combo.currentText())

        start_timestamp = int(time.mktime(time.strptime(f"{start_year}-01-01", "%Y-%m-%d")))
        end_timestamp = int(time.mktime(time.strptime(f"{end_year}-12-31", "%Y-%m-%d")))

        self.progress_bar.setValue(0)
        total_tickers = len(tickers)

        results = []
        for i, ticker in enumerate(tickers):
            try:
                url = f"https://yahoo-finance-api-data.p.rapidapi.com/symbol/price-history"
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
                response = requests.get(url, headers=headers, params=querystring)

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
        # 데이터를 파싱하여 각 티커에 대한 주가 및 재무 정보를 처리
        # Parses the received data and extracts the required financial information.
        try:
            close_prices = {}
            if 'priceHistory' in data:
                price_history = data.get('priceHistory', {}).get('prices', [])
                for price in price_history:
                    date = pd.to_datetime(price.get('date'), unit='s')
                    if date.month == 12 and date.day == 31:
                        close_prices[date.year] = price.get('close', 'N/A')

            shares_outstanding = data.get('summaryDetail', {}).get('sharesOutstanding', {}).get('raw', 'N/A')
            market_cap = data.get('summaryDetail', {}).get('marketCap', {}).get('raw', 'N/A')
            eps = data.get('defaultKeyStatistics', {}).get('trailingEps', {}).get('raw', 'N/A')
            ebitda = data.get('financialData', {}).get('ebitda', {}).get('raw', 'N/A')
            total_debt = data.get('balanceSheetHistory', {}).get('balanceSheetStatements', [{}])[-1].get('totalDebt', {}).get('raw', 'N/A')
            revenue = data.get('incomeStatementHistory', {}).get('incomeStatementHistory', [{}])[-1].get('totalRevenue', {}).get('raw', 'N/A')

            sector = data.get('summaryProfile', {}).get('sector', 'N/A')
            employees = data.get('summaryProfile', {}).get('fullTimeEmployees', 'N/A')

            esg_score = data.get('sustainability', {}).get('totalEsg', 'N/A')

            result = {
                '티커': ticker,
                '2020년 마지막 마감 주가': close_prices.get(2020, 'N/A'),
                '2021년 마지막 마감 주가': close_prices.get(2021, 'N/A'),
                '2022년 마지막 마감 주가': close_prices.get(2022, 'N/A'),
                '2023년 마지막 마감 주가': close_prices.get(2023, 'N/A'),
                '발행 주식 수': shares_outstanding,
                'Market Cap': market_cap,
                'EBITDA': ebitda,
                '매출액': revenue,
                'EPS': eps,
                '총부채': total_debt,
                '업종': sector,
                '종업원 수': employees,
                'ESG 스코어': esg_score
            }

            return result

        except Exception as e:
            return {'티커': ticker, '오류': f"Data parsing error: {str(e)}"}

    def save_to_excel(self, results):
        # 엑셀 파일로 데이터 저장
        # Saves the fetched data into an Excel file.
        df = pd.DataFrame(results)
        save_path = f"{self.save_directory}/Financial_Data.xlsx"
        df.to_excel(save_path, index=False)
        QMessageBox.information(self, "Complete", f"Data saved to {save_path}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = YahooFinanceApp()
    ex.show()
    sys.exit(app.exec_())
