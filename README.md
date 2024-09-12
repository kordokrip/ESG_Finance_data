
---

# ESG Data Crawler and Analysis System

![ESG Banner](https://www.complilaw.com/wp-content/uploads/2023/09/AdobeStock_570800308-1.jpeg) 

## **Table of Contents**
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Data Sources](#data-sources)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [System Architecture](#system-architecture)
- [Contributing](#contributing)
- [License](#license)

## **Overview**
This project is designed to **crawl ESG (Environmental, Social, and Governance) data** from multiple financial and ESG-specific sources, including **Yahoo Finance**, **Google Finance**, and **MarketWatch**, and analyze it for various companies. The system can retrieve data related to **carbon emissions**, **workforce diversity**, **fair compensation**, and more. It can also handle API-based data access via **ESG Enterprise API**, **Refinitiv**, or other ESG data providers for more reliable and rich data.

The system allows users to:
- Retrieve ESG data for a list of companies (identified by their stock tickers).
- Analyze and visualize the data.
- Export the data and visualizations to Excel for further analysis.

## **Features**
- **Multi-source ESG data scraping**: Scrapes data from Yahoo Finance, Google Finance, and MarketWatch.
- **API Integration**: Supports **ESG Enterprise API**, **Refinitiv API**, and **Sustainalytics API** for accurate ESG data.
- **Data Analysis**: Analyzes ESG metrics such as **carbon emissions**, **workforce diversity**, **board composition**, and more.
- **Excel Export**: Export ESG data and visualizations (bar charts) to Excel for easy sharing and further analysis.
- **PyQt5 GUI**: User-friendly graphical interface to input stock tickers, choose output folder, and initiate data collection.

## **Project Structure**
```
ESG_Data_Crawler/
│
├── data/                     # Example data and excel files
├── src/                      # Source code for scraping, analysis, and GUI
│   ├── crawler.py            # Main logic for data crawling
│   ├── api_integration.py    # Handles API requests for ESG data
│   ├── analysis.py           # Functions for data analysis and visualization
│   └── gui.py                # PyQt5-based graphical interface
├── tests/                    # Unit tests for the system
├── README.md                 # This README file
└── requirements.txt          # Required dependencies
```

## **Data Sources**
The system supports multiple sources for ESG data collection:

### 1. **Yahoo Finance**
   - Provides basic ESG data such as **carbon emissions** and **workforce diversity**.
   - Data is scraped from the `https://finance.yahoo.com` domain.
   - Example of scraped data: `https://finance.yahoo.com/quote/AAPL/sustainability`

### 2. **Google Finance**
   - Secondary source for ESG data.
   - Scrapes financial data and sustainability-related metrics from `https://google.com/finance`.

### 3. **MarketWatch**
   - Provides company profiles and limited ESG data.
   - URL: `https://www.marketwatch.com/investing/stock/{ticker}/company-profile`

### 4. **API-Based Data Access**
   - **ESG Enterprise API**: Provides comprehensive ESG data on multiple companies with access to **carbon emissions**, **board composition**, **data privacy** concerns, etc.
   - **Refinitiv API**: Paid service for premium ESG data.

## **Technology Stack**
- **Programming Language**: Python
- **Libraries**:
  - `requests`: For making HTTP requests to websites and APIs.
  - `BeautifulSoup`: For parsing and extracting data from HTML pages.
  - `pandas`: For data manipulation and analysis.
  - `matplotlib`: For visualizing ESG data as charts.
  - `openpyxl`: For exporting data and charts to Excel.
  - `PyQt5`: For building a user-friendly graphical interface.
- **API Integrations**:
  - **ESG Enterprise API**: For accessing ESG-specific data.
  - **Refinitiv API**: For advanced ESG metrics.

## **Installation**

### **Pre-requisites**
Make sure you have Python 3.7 or higher installed.

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/ESG_Data_Crawler.git
   cd ESG_Data_Crawler
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up the API keys:
   - Obtain API keys from **ESG Enterprise API** and other services.
   - Save the keys in an environment variable or a separate file such as `api_keys.json`.

### Example `api_keys.json`:
```json
{
  "esg_enterprise_key": "your-esg-enterprise-key",
  "refinitiv_key": "your-refinitiv-key"
}
```

## **Usage**

1. **Running the GUI:**
   Run the PyQt5-based GUI for interacting with the system:
   ```bash
   python src/gui.py
   ```

2. **Select the stock tickers:**
   In the GUI, input up to 5 stock tickers (e.g., AAPL, TSLA) and choose a folder where the data will be saved.

3. **Start the data collection:**
   Click the "Crawl Data" button to start collecting ESG data from the available sources.

4. **Analyze and export data:**
   The system will generate Excel files for each ticker, including raw ESG data and visualizations (bar charts) of key ESG metrics such as **carbon emissions**, **material usage**, **board composition**, etc.

## **System Architecture**

### **Design Overview**

The system consists of the following key components:

- **GUI Module (PyQt5)**: This module provides a user-friendly interface where users can input stock tickers, select output folders, and trigger data collection.
- **Data Crawling Module**:
   - **Web Scraping**: Scrapes ESG data from multiple financial sources (Yahoo Finance, Google Finance, MarketWatch).
   - **API Integration**: If web scraping fails, the system switches to API-based data access (e.g., **ESG Enterprise API**, **Refinitiv**).
- **Data Analysis & Visualization Module**:
   - Analyzes the collected ESG data and generates visualizations (using Matplotlib).
   - Exports the raw data and charts to Excel files.

### **System Flow Diagram**

```plaintext
┌────────────┐     ┌────────────────┐     ┌─────────────┐
│   GUI      │ ──► │ Data Crawling  │ ──► │ Data Export │
└────────────┘     └────────────────┘     └─────────────┘
     ▲                    │                      │
     │                    ▼                      ▼
     │              API Integration         Visualization
     │              (ESG Enterprise)         (Matplotlib)
     ▼                    
User Input            Web Scraping                
```

## **Contributing**
We welcome contributions! Please follow the steps below:

1. Fork the repository.
2. Create a new branch for your feature or bug fix: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m 'Add new feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Create a pull request and describe your changes.

┌───────────────────────────┐
│   Start Application       │
└───────────────┬───────────┘
                │
                ▼
┌────────────────────────────────┐
│  User Inputs Ticker Symbols     │
│  (Max 5 Symbols)                │
└───────────────┬────────────────┘
                │
                ▼
┌────────────────────────────────┐
│  Choose Folder to Save Data     │
└───────────────┬────────────────┘
                │
                ▼
┌────────────────────────────────────────┐
│  Attempt to Fetch ESG Data from Yahoo  │
│  Finance using Web Scraping            │
└───────────────┬────────────────────────┘
                │
                │ Success:               │
                ▼                        ▼
┌────────────────────────┐   ┌─────────────────────────┐
│  Success: Yahoo Data   │   │  Failure: Try ChatGPT    │
│  Process and Store Data│   │  API for Data Retrieval  │
└───────────────┬────────┘   └─────────────────────────┘
                │                        │
                ▼                        ▼
┌───────────────────────────────────────────────┐
│  Store Data in Excel and Create Visualization │
│  (Including Graphs with Matplotlib)           │
└───────────────┬───────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────┐
│  Success/Failure Notification to User (Error Alerts) │
│  Display Message: Data Stored or Error Occurred      │
└─────────────────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────┐
│  End Program                │
└─────────────────────────────┘

## **License**
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

By following this README, contributors and users can understand the purpose and functionality of the project, how to set it up, and how to use it effectively. The architecture diagram, installation guide, and detailed usage instructions help ensure a smooth onboarding process for new users.



----------------------------------------------------------------------------------


# ESG 데이터 크롤러 및 분석 시스템


## **목차**
- [개요](#개요)
- [기능](#기능)
- [프로젝트 구조](#프로젝트-구조)
- [데이터 소스](#데이터-소스)
- [기술 스택](#기술-스택)
- [설치](#설치)
- [사용 방법](#사용-방법)
- [시스템 아키텍처](#시스템-아키텍처)
- [기여](#기여)
- [라이선스](#라이선스)

## **개요**
이 프로젝트는 **ESG(환경, 사회, 지배구조)** 데이터를 여러 금융 및 ESG 전문 소스에서 크롤링하고 분석하는 시스템입니다. 여기에는 **Yahoo Finance**, **Google Finance**, **MarketWatch** 등의 데이터 소스가 포함되며, 다양한 기업의 **탄소 배출**, **직원 복지**, **이사회 구성** 등과 같은 ESG 데이터를 수집하고 분석합니다.

또한, **ESG Enterprise API**, **Refinitiv API** 등의 API를 통해 더욱 신뢰할 수 있는 데이터를 API 방식으로 가져올 수 있습니다.

### 이 시스템은 다음을 수행합니다:
- 기업의 **티커(symbol)**를 통해 ESG 데이터를 수집합니다.
- 수집한 데이터를 분석하고 시각화합니다.
- 데이터를 **엑셀 파일**로 내보내고, 분석 결과를 **그래프**로 시각화하여 추가 분석에 활용할 수 있습니다.

## **기능**
- **다중 소스 ESG 데이터 크롤링**: Yahoo Finance, Google Finance, MarketWatch 등 다양한 소스에서 데이터를 크롤링합니다.
- **API 통합**: **ESG Enterprise API**, **Refinitiv API**, **Sustainalytics API**를 통한 신뢰성 높은 ESG 데이터를 수집할 수 있습니다.
- **데이터 분석**: **탄소 배출**, **직원 복지**, **이사회 구성** 등 ESG 지표를 분석합니다.
- **엑셀 내보내기**: 수집된 데이터를 **엑셀 파일**로 내보내고, **Matplotlib**를 사용하여 그래프로 시각화할 수 있습니다.
- **PyQt5 GUI**: 직관적인 GUI를 제공하여 사용자가 티커(symbol)를 입력하고 데이터를 수집하고 저장할 수 있습니다.

## **프로젝트 구조**
```
ESG_Data_Crawler/
│
├── data/                     # 예시 데이터 및 엑셀 파일
├── src/                      # 데이터 크롤링, 분석, GUI 코드
│   ├── crawler.py            # 데이터 크롤링 주요 로직
│   ├── api_integration.py    # ESG 데이터 API 통합 처리
│   ├── analysis.py           # 데이터 분석 및 시각화 함수
│   └── gui.py                # PyQt5 기반의 GUI 코드
├── tests/                    # 시스템 테스트
├── README.md                 # 이 README 파일
└── requirements.txt          # 의존성 목록
```

## **데이터 소스**
이 시스템은 여러 소스에서 ESG 데이터를 수집합니다:

### 1. **Yahoo Finance**
   - **탄소 배출**, **직원 복지** 등의 ESG 데이터를 제공합니다.
   - 웹 스크래핑을 통해 데이터를 수집합니다.
   - 예시 URL: `https://finance.yahoo.com/quote/AAPL/sustainability`

### 2. **Google Finance**
   - 추가 ESG 데이터 소스로서 **구글 파이낸스**에서 데이터를 수집합니다.
   - URL: `https://google.com/finance`

### 3. **MarketWatch**
   - **기업 프로필** 및 일부 ESG 데이터를 제공합니다.
   - URL: `https://www.marketwatch.com/investing/stock/{ticker}/company-profile`

### 4. **API 기반 데이터 접근**
   - **ESG Enterprise API**: 여러 회사의 **탄소 배출**, **이사회 구성**, **데이터 보안** 등을 포함한 심층 ESG 데이터를 제공합니다.
   - **Refinitiv API**: 유료 API로, 프리미엄 ESG 데이터를 제공합니다.

## **기술 스택**
- **프로그래밍 언어**: Python
- **사용 라이브러리**:
  - `requests`: 웹사이트와 API 요청을 처리합니다.
  - `BeautifulSoup`: HTML 파싱 및 데이터 추출에 사용됩니다.
  - `pandas`: 데이터 분석 및 처리.
  - `matplotlib`: ESG 데이터를 시각화합니다.
  - `openpyxl`: 엑셀 파일로 데이터와 시각화 결과를 저장합니다.
  - `PyQt5`: 사용하기 쉬운 GUI를 제공합니다.
- **API 통합**:
  - **ESG Enterprise API**: 종합적인 ESG 데이터 제공 API.
  - **Refinitiv API**: 심층 ESG 데이터를 제공하는 유료 API.

## **설치**

### **사전 요구 사항**
- Python 3.7 이상 설치가 필요합니다.

1. 이 저장소를 클론합니다:

   ```bash
   git clone https://github.com/yourusername/ESG_Data_Crawler.git
   cd ESG_Data_Crawler
   ```

2. 필요한 의존성을 설치합니다:

   ```bash
   pip install -r requirements.txt
   ```

3. API 키 설정:
   - **ESG Enterprise API** 또는 다른 API 키를 발급받아 설정합니다.
   - 환경 변수에 저장하거나 `api_keys.json` 파일로 설정할 수 있습니다.

### **예시 `api_keys.json`**:
```json
{
  "esg_enterprise_key": "your-esg-enterprise-key",
  "refinitiv_key": "your-refinitiv-key"
}
```

## **사용 방법**

1. **GUI 실행**:
   PyQt5 GUI를 실행하여 사용자가 상호작용할 수 있도록 합니다:
   ```bash
   python src/gui.py
   ```

2. **티커 입력**:
   GUI에서 최대 5개의 티커(symbol)를 입력하고 데이터를 저장할 폴더를 선택하세요.

3. **데이터 수집 시작**:
   "데이터 크롤링" 버튼을 클릭하여 데이터를 수집하고, 지정된 폴더에 데이터를 저장합니다.

4. **데이터 분석 및 내보내기**:
   수집된 ESG 데이터는 **엑셀 파일**로 내보내지며, 주요 지표에 대한 **그래프**도 포함됩니다. 각 티커에 대해 데이터를 분석하고 결과를 시각화할 수 있습니다.

## **시스템 아키텍처**

### **설계 개요**

이 시스템은 다음과 같은 주요 구성 요소로 나뉩니다:

- **GUI 모듈 (PyQt5)**: 사용자 인터페이스에서 티커를 입력받고, 데이터를 수집하고 내보내는 과정을 제어합니다.
- **데이터 크롤링 모듈**:
   - **웹 스크래핑**: Yahoo Finance, Google Finance, MarketWatch 등의 웹사이트에서 ESG 데이터를 스크래핑합니다.
   - **API 통합**: 스크래핑 실패 시 **ESG Enterprise API**, **Refinitiv API** 등으로부터 데이터를 수집합니다.
- **데이터 분석 및 시각화 모듈**:
   - 수집된 데이터를 분석하고 **Matplotlib**을 사용하여 그래프를 생성합니다.
   - 데이터를 엑셀 파일로 내보내고, 그래프 이미지를 함께 저장합니다.

### **시스템 흐름도**

```plaintext
┌────────────┐     ┌────────────────┐     ┌─────────────┐
│   GUI      │ ──► │ Data Crawling  │ ──► │ Data Export │
└────────────┘     └────────────────┘     └─────────────┘
     ▲                    │                      │
     │                    ▼                      ▼
     │              API Integration         Visualization
     │              (ESG Enterprise)         (Matplotlib)
     ▼                    
User Input            Web Scraping                
```

## **기여**
기여를 환영합니다! 아래 단계에 따라 기여할 수 있습니다:

1. 이 저장소를 포크하세요.
2. 새로운 브랜치를 생성하세요: `git checkout -b feature-name`.
3. 변경 사항을 커밋하세요: `git commit -m 'Add new feature'`.
4. 브랜치에 푸시하세요: `git push origin feature-name`.
5. 풀 리퀘스트를 생성하고 변경 사항을 설명하세요.

## **라이선스**
이 프로젝트는 MIT 라이선스에 따라 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

---

이 README는 **ESG 데이터를 크롤링하고 분석하는 시스템**의 전반적인 구조와 사용 방법을 설명합니다. 사용자는 이 문서를 참조하여 시스템을 설치하고 실행할 수 있으며, 프로젝트에 기여할 수 있는 방법에 대해서도 안내받을 수 있습니다.
