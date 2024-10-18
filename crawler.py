import sys
import requests
import time
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QProgressBar, QFileDialog, QMessageBox, QComboBox
from PyQt5.QtCore import Qt

class YahooFinanceApp(QWidget):
    def __init__(self):
        super().__init__()
        self.api_key = "YAHOO FINANCE API KEY"  # API 키 설정
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 티커 입력 창 - 최대 10개의 입력란 제공
        self.ticker_inputs = []
        for i in range(10):
            ticker_input = QLineEdit(self)
            ticker_input.setPlaceholderText(f'티커 {i+1}')
            layout.addWidget(ticker_input)
            self.ticker_inputs.append(ticker_input)

        # 기간 선택을 위한 콤보박스 (1년, 2년, 3년)
        self.year_combo = QComboBox(self)
        self.year_combo.addItems(['2020', '2021', '2022', '2023'])
        layout.addWidget(QLabel("데이터 기간 선택 (연도별 단위)"))
        self.period_combo = QComboBox(self)
        self.period_combo.addItems(['1년', '2년', '3년'])
        layout.addWidget(QLabel("데이터 기간 선택 (단위)"))
        layout.addWidget(self.period_combo)
        layout.addWidget(self.year_combo)

        # 진행 상태 표시
        self.progress_bar = QProgressBar(self)
        layout.addWidget(self.progress_bar)

        # 버튼 및 저장 경로 선택
        self.fetch_button = QPushButton('데이터 수집 및 엑셀 저장', self)
        self.fetch_button.clicked.connect(self.fetch_data)
        layout.addWidget(self.fetch_button)

        # 파일 저장 경로 선택
        self.save_path_button = QPushButton('저장 경로 선택', self)
        self.save_path_button.clicked.connect(self.choose_save_directory)
        layout.addWidget(self.save_path_button)

        self.save_path_label = QLabel('저장 경로: 선택되지 않음', self)
        layout.addWidget(self.save_path_label)

        # GUI 설정 적용
        self.setLayout(layout)

    def choose_save_directory(self):
        # 저장 경로 선택 다이얼로그 열기
        directory = QFileDialog.getExistingDirectory(self, "저장 경로 선택")
        if directory:
            self.save_path_label.setText(f'저장 경로: {directory}')
            self.save_directory = directory

    def fetch_data(self):
        tickers = [ticker.text().upper() for ticker in self.ticker_inputs if ticker.text().strip()]
        if not tickers:
            QMessageBox.warning(self, "오류", "최소한 하나의 티커를 입력해주세요.")
            return

        # 기간 설정 가져오기
        selected_year = self.year_combo.currentText()
        selected_period = self.period_combo.currentText()

        # 진행 상태 초기화
        self.progress_bar.setValue(0)
        total_tickers = len(tickers)

        # 각 티커에 대해 데이터 수집
        results = []
        for i, ticker in enumerate(tickers):
            try:
                url = f"https://yh-finance.p.rapidapi.com/stock/v3/get-historical-data"
                querystring = {"symbol": ticker, "region": "US"}
                headers = {
                    "X-RapidAPI-Key": self.api_key,
                    "X-RapidAPI-Host": "yh-finance.p.rapidapi.com"
                }
                response = requests.get(url, headers=headers, params=querystring)

                if response.status_code == 200:
                    data = response.json()
                    # JSON 파싱 후 필요한 데이터 추출
                    result = self.process_data(ticker, data)
                    results.append(result)
                else:
                    QMessageBox.warning(self, "오류", f"{ticker}에 대한 데이터를 가져오지 못했습니다. 상태 코드: {response.status_code}")
                # 1초 간격으로 API 요청 간 지연 추가
                time.sleep(1)
            except Exception as e:
                QMessageBox.critical(self, "오류", f"데이터 수집 중 오류 발생: {str(e)}")

            # 진행 상황 업데이트
            progress = int(((i + 1) / total_tickers) * 100)
            self.progress_bar.setValue(progress)

        # 엑셀로 데이터 저장
        if results and hasattr(self, 'save_directory'):
            self.save_to_excel(results)

    def process_data(self, ticker, data):
        # Yahoo Finance API 응답에서 필요한 데이터 추출
        try:
            result = {
                '티커': ticker,
                '현재 가격': data['prices'][-1]['close'],  # 최신 마감 주가
                '발행 주식 수': data.get('sharesOutstanding', 'N/A'),  # 발행 주식수량
                'Market Cap': data.get('marketCap', 'N/A'),  # 시가총액
                'EPS': data.get('eps', 'N/A'),  # 주당순이익
                '업종': "N/A",  # 업종 데이터는 별도의 엔드포인트에서 처리 필요
                '종업원 수': "N/A",  # 종업원 수는 별도의 엔드포인트에서 처리 필요
                'ESG 스코어': "N/A"  # ESG 데이터는 별도의 엔드포인트에서 처리 필요
            }
            return result
        except (KeyError, IndexError) as e:
            return {'티커': ticker, '오류': f"데이터 파싱 오류: {str(e)}"}

    def save_to_excel(self, results):
        # 수집된 데이터를 엑셀로 저장하는 함수
        df = pd.DataFrame(results)
        save_path = f"{self.save_directory}/기업_데이터.xlsx"
        df.to_excel(save_path, index=False)
        QMessageBox.information(self, "완료", f"데이터가 {save_path}에 저장되었습니다.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = YahooFinanceApp()
    ex.show()
    sys.exit(app.exec_())
