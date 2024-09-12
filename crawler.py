import openai
import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit, QLabel, QFileDialog, QMessageBox, QHBoxLayout
from openpyxl import load_workbook
from openpyxl.drawing.image import Image
import os
import time

# ChatGPT API Key 설정
openai.api_key = ""

# ChatGPT API를 통해 문제 해결
def ask_chatgpt(prompt):
    response = openai.Completion.create(
      engine="gpt-4",
      prompt=prompt,
      max_tokens=150,
      n=1,
      stop=None,
      temperature=0.7,
    )
    return response.choices[0].text.strip()

# Yahoo Finance에서 ESG 데이터를 웹 스크래핑하는 함수
def scrape_yahoo_finance_esg(ticker):
    url = f"https://finance.yahoo.com/quote/{ticker}/sustainability"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        def safe_find(key):
            element = soup.find(text=key)
            return element.find_next().text if element else "N/A"

        data = {
            'waterUsage': safe_find("Water Usage"),
            'materialUsage': safe_find("Material Usage"),
            'wasteManagement': safe_find("Waste Management"),
            'energyUsage': safe_find("Energy Usage"),
            'pollutionIncidents': safe_find("Pollution Incidents"),
            'workforceDiversity': safe_find("Workforce Diversity"),
            'fairCompensation': safe_find("Fair Compensation"),
            'employeeWelfare': safe_find("Employee Welfare"),
            'boardComposition': safe_find("Board Composition"),
            'executiveCompensation': safe_find("Executive Compensation"),
            'dataPrivacy': safe_find("Data Privacy"),
            'ethicalDecisionMaking': safe_find("Ethical Decision Making")
        }

        if all(value == "N/A" for value in data.values()):
            print(f"{ticker}에 대한 ESG 데이터를 찾을 수 없습니다.")
            return None

        return data
    elif response.status_code == 404:
        print(f"Error: Unable to fetch data for {ticker}. Status Code: 404")
        return None
    else:
        print(f"Error: Unable to fetch data for {ticker}. Status Code: {response.status_code}")
        return None

# Google Finance에서 데이터를 스크래핑하는 함수 추가
def scrape_google_finance_esg(ticker):
    # Google Finance에서 특정 티커의 데이터를 스크래핑하는 로직
    url = f"https://www.google.com/finance/quote/{ticker}:NASDAQ"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        def safe_find_google(key):
            element = soup.find(text=key)
            return element.find_next().text if element else "N/A"

        data = {
            'waterUsage': safe_find_google("Water Usage"),
            'materialUsage': safe_find_google("Material Usage"),
            'wasteManagement': safe_find_google("Waste Management"),
            'energyUsage': safe_find_google("Energy Usage"),
            'pollutionIncidents': safe_find_google("Pollution Incidents"),
            'workforceDiversity': safe_find_google("Workforce Diversity"),
            'fairCompensation': safe_find_google("Fair Compensation"),
            'employeeWelfare': safe_find_google("Employee Welfare"),
            'boardComposition': safe_find_google("Board Composition"),
            'executiveCompensation': safe_find_google("Executive Compensation"),
            'dataPrivacy': safe_find_google("Data Privacy"),
            'ethicalDecisionMaking': safe_find_google("Ethical Decision Making")
        }

        if all(value == "N/A" for value in data.values()):
            print(f"Google Finance에서 {ticker}에 대한 데이터를 찾을 수 없습니다.")
            return None

        return data
    else:
        print(f"Error: Unable to fetch data for {ticker} from Google Finance. Status Code: {response.status_code}")
        return None

# 다른 소스에서 데이터를 가져오는 함수 (MarketWatch 추가 예시)
def scrape_marketwatch_esg(ticker):
    url = f"https://www.marketwatch.com/investing/stock/{ticker}/company-profile"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        def safe_find_marketwatch(key):
            element = soup.find(text=key)
            return element.find_next().text if element else "N/A"

        data = {
            'waterUsage': safe_find_marketwatch("Water Usage"),
            'materialUsage': safe_find_marketwatch("Material Usage"),
            'wasteManagement': safe_find_marketwatch("Waste Management"),
            'energyUsage': safe_find_marketwatch("Energy Usage"),
            'pollutionIncidents': safe_find_marketwatch("Pollution Incidents"),
            'workforceDiversity': safe_find_marketwatch("Workforce Diversity"),
            'fairCompensation': safe_find_marketwatch("Fair Compensation"),
            'employeeWelfare': safe_find_marketwatch("Employee Welfare"),
            'boardComposition': safe_find_marketwatch("Board Composition"),
            'executiveCompensation': safe_find_marketwatch("Executive Compensation"),
            'dataPrivacy': safe_find_marketwatch("Data Privacy"),
            'ethicalDecisionMaking': safe_find_marketwatch("Ethical Decision Making")
        }

        if all(value == "N/A" for value in data.values()):
            print(f"MarketWatch에서 {ticker}에 대한 데이터를 찾을 수 없습니다.")
            return None

        return data
    else:
        print(f"Error: Unable to fetch data for {ticker} from MarketWatch. Status Code: {response.status_code}")
        return None

# ESG 데이터를 엑셀로 저장하고 시각화하는 함수
def save_esg_data_to_excel_and_plot(tickers, folder_path):
    for ticker in tickers:
        if not ticker:
            continue

        # Yahoo Finance에서 ESG 데이터 가져오기
        data = scrape_yahoo_finance_esg(ticker)

        # Yahoo Finance에서 실패하면 Google Finance 시도
        if data is None:
            print(f"Yahoo Finance에서 {ticker}에 대한 데이터를 찾지 못했습니다. Google Finance를 시도합니다.")
            data = scrape_google_finance_esg(ticker)

        # Google Finance에서 실패하면 MarketWatch 시도
        if data is None:
            print(f"Google Finance에서 {ticker}에 대한 데이터를 찾지 못했습니다. MarketWatch를 시도합니다.")
            data = scrape_marketwatch_esg(ticker)

        if data is not None:
            # 데이터프레임으로 변환
            df = pd.DataFrame([data])

            # 엑셀 파일 저장 경로 설정
            file_path = os.path.join(folder_path, f"{ticker}_esg_data.xlsx")
            df.to_excel(file_path, index=False)
            print(f"{ticker}의 ESG 데이터가 {file_path}에 저장되었습니다.")

            # 시각화 (예: 물 사용과 에너지 사용)
            plt.figure(figsize=(10, 6))
            plt.bar(df.columns, df.iloc[0], color='blue')
            plt.title(f'{ticker}의 ESG 데이터')
            plt.xlabel('ESG 항목')
            plt.ylabel('수치')
            plt.xticks(rotation=45)
            plt.tight_layout()

            # 그래프를 이미지로 저장
            plot_image_path = os.path.join(folder_path, f"{ticker}_esg_plot.png")
            plt.savefig(plot_image_path)
            plt.close()

            # 저장된 엑셀 파일에 그래프 이미지 포함
            wb = load_workbook(file_path)
            ws = wb.active
            img = Image(plot_image_path)
            ws.add_image(img, 'H1')  # 엑셀 시트에서 H1 위치에 이미지 삽입
            wb.save(file_path)
            print(f"{ticker}의 ESG 데이터와 그래프가 {file_path}에 저장되었습니다.")
        else:
                        print(f"{ticker}에 대한 ESG 데이터를 여러 소스에서 가져오지 못했습니다.")

# PyQt5 GUI 개선
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ESG Data Crawler")
        self.setGeometry(100, 100, 500, 300)

        # 폴더 저장 경로
        self.folder_path = ""

        # 메인 레이아웃
        main_layout = QVBoxLayout()

        # 상단 입력 필드 설명 레이블
        instruction_label = QLabel("기업의 티커를 입력하고 데이터를 가져오세요:")
        main_layout.addWidget(instruction_label)

        # 티커 입력 필드 (5개)
        self.ticker_inputs = []
        for i in range(5):
            ticker_input = QLineEdit(self)
            ticker_input.setPlaceholderText(f"티커 {i+1} 입력")
            main_layout.addWidget(ticker_input)
            self.ticker_inputs.append(ticker_input)

        # 버튼 레이아웃
        button_layout = QHBoxLayout()

        # 폴더 선택 버튼
        folder_button = QPushButton("폴더 선택", self)
        folder_button.clicked.connect(self.select_folder)
        button_layout.addWidget(folder_button)

        # 데이터 크롤링 버튼
        crawl_button = QPushButton("데이터 크롤링 및 저장", self)
        crawl_button.clicked.connect(self.crawl_data)
        button_layout.addWidget(crawl_button)

        # 버튼 레이아웃 추가
        main_layout.addLayout(button_layout)

        # 메시지 표시용 레이블
        self.message_label = QLabel("", self)
        main_layout.addWidget(self.message_label)

        # 중앙 위젯 설정
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def crawl_data(self):
        tickers = [ticker_input.text().upper() for ticker_input in self.ticker_inputs if ticker_input.text().strip()]

        if not tickers:
            QMessageBox.warning(self, "입력 오류", "최소 하나의 티커를 입력하세요.")
            return

        if not self.folder_path:
            QMessageBox.warning(self, "폴더 선택 오류", "저장할 폴더를 선택하세요.")
            return

        try:
            save_esg_data_to_excel_and_plot(tickers, self.folder_path)
            self.message_label.setText(f"데이터가 {self.folder_path}에 저장되었습니다.")
        except Exception as e:
            self.message_label.setText(f"크롤링 중 오류가 발생했습니다: {e}")

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "저장할 폴더 선택", "")
        if folder:
            self.folder_path = folder
            self.message_label.setText(f"폴더 선택됨: {self.folder_path}")
        else:
            QMessageBox.warning(self, "폴더 선택 오류", "폴더를 선택하지 않았습니다.")

# PyQt5 애플리케이션 실행
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

