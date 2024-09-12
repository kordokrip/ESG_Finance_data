
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

## **License**
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

By following this README, contributors and users can understand the purpose and functionality of the project, how to set it up, and how to use it effectively. The architecture diagram, installation guide, and detailed usage instructions help ensure a smooth onboarding process for new users.
