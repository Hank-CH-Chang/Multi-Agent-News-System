[English](#multi-agent-news-system-english) | [中文](#multi-agent-news-system-中文)

---

# Multi-Agent News System (English)

This is a system where multiple AI agents collaborate to automatically search, analyze, and organize news on a specific topic. You just need to provide a topic, and the system will activate a series of AI agents to produce structured news information for you.

## ✨ Features

- **Multi-Agent Collaboration**: The system consists of specialized AI agents such as a Commander, Crawler, Classifier, and Ranker, simulating a team workflow.
- **Automated News Gathering**: Integrates with the Google News RSS feed to automatically fetch the latest news related to a given topic.
- **Intelligent Content Processing**: Leverages the power of Large Language Models (LLMs) to summarize, classify, and rank the fetched news articles.
- **Stable Link Handling**: Automatically resolves Google News redirect links to provide clean, direct, and valid final URLs.
- **Asynchronous Architecture**: Built on FastAPI, providing high-performance asynchronous processing capabilities.

## 🚀 Architecture

The system uses a Multi-Agent design pattern. Each agent has a clear responsibility and communicates and transfers data via an Agent-to-Agent Bus.

1.  **Commander Agent**: Receives the user-input topic, initiates the entire news processing pipeline, and sends a notification upon completion.
2.  **Crawler Agent**: Receives the topic, uses an LLM with the `google_web_search` tool to find relevant articles from Google News, and extracts basic information like title, link, and summary.
3.  **Classifier Agent**: (Conceptual) Classifies the fetched news into categories (e.g., Technology, Politics, Sports).
4.  **Ranker Agent**: (Conceptual) Ranks articles based on importance, relevance, or popularity.
5.  **Storage Agent**: (Conceptual) Saves the final processed news data to a database or a JSON file.

## 🛠️ Setup and Installation

Follow these steps to set up and run the project.

**1. Clone the Project**
```bash
git clone <your-repository-url>
cd multi_agent_news_system
```

**2. Create and Activate a Virtual Environment**
```bash
# Create a virtual environment
python3 -m venv myenv

# Activate the virtual environment (macOS/Linux)
source myenv/bin/activate
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

**4. Set Up Environment Variables**

This project requires a Google Gemini API key. Create a file named `.env` in the project's root directory.

```bash
touch .env
```

Then, add the following content to the `.env` file, replacing `YOUR_GEMINI_API_KEY` with your own key:

```
GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
```

## ▶️ How to Run

Once everything is set up, run the following command to start the application:

```bash
python3 main.py
```

You will see output similar to the following in your terminal, indicating the server has started successfully:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```
You can then interact with the system, for example, by sending a topic task via another terminal or an API testing tool.

## 📁 Project Structure

```
/
├── agents/             # Contains the code for all agents
│   ├── commander_agent.py
│   └── crawler_agent.py
├── core/               # Core modules, like the LLM client and tools
│   ├── llm_client.py
│   └── tools.py
├── database/           # Database-related files
├── data/               # Stores output data, such as JSON files
├── main.py             # Main project entry point (FastAPI)
├── requirements.txt    # List of Python dependencies
└── README.md           # This README file
```

---

# Multi-Agent News System (中文)

這是一個由多個 AI 代理（Agent）協作，自動化搜尋、分析並整理特定主題新聞的系統。你只需要給定一個主題，系統便會啟動一系列的 AI 代理，為你產出結構化的新聞資訊。

## ✨ 功能特性

- **多代理協作**：系統由指揮官、爬蟲、分類器、排序器等多個專職 AI 代理組成，模擬團隊工作流程。
- **自動化新聞搜集**：整合 Google News RSS feed，自動抓取與指定主題相關的最新新聞。
- **智慧內容處理**：利用大型語言模型（LLM）的能力，對抓取到的新聞進行摘要、分類與排序。
- **穩定的連結處理**：自動解析 Google News 的重新導向連結，提供乾淨、直接、有效的最終新聞網址。
- **非同步架構**：基於 FastAPI 構建，具備高效能的非同步處理能力。

## 🚀 運作架構

本系統採用了多代理（Multi-Agent）的設計模式，每個代理都有明確的職責，並透過訊息總線（Agent-to-Agent Bus）進行通訊與數據傳遞。

1.  **Commander Agent (指揮官)**：接收使用者輸入的主題，啟動整個新聞處理流程，並在流程結束時發出通知。
2.  **Crawler Agent (爬蟲)**：接收主題後，利用 LLM 和 `google_web_search` 工具從 Google News 搜尋相關文章，並抓取標題、連結、摘要等基本資訊。
3.  **Classifier Agent (分類器)**：(概念) 對抓取到的新聞進行分類（例如：科技、政治、體育）。
4.  **Ranker Agent (排序器)**：(概念) 根據新聞的重要性、相關性或熱度進行排序。
5.  **Storage Agent (儲存)**：(概念) 將最終處理好的新聞資料儲存到資料庫或 JSON 檔案中。

## 🛠️ 安裝與設定

請依照以下步驟來設定與執行本專案。

**1. 複製專案**
```bash
git clone <your-repository-url>
cd multi_agent_news_system
```

**2. 建立並啟用虛擬環境**
```bash
# 建立虛擬環境
python3 -m venv myenv

# 啟用虛擬環境 (macOS/Linux)
source myenv/bin/activate
```

**3. 安裝依賴套件**
```bash
pip install -r requirements.txt
```

**4. 設定環境變數**

本專案需要使用 Google Gemini 的 API 金鑰。請在專案的根目錄下建立一個名為 `.env` 的檔案。

```bash
touch .env
```

然後在 `.env` 檔案中加入以下內容，並將 `YOUR_GEMINI_API_KEY` 替換成你自己的金鑰：

```
GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
```

## ▶️ 如何執行

一切設定就緒後，執行以下指令來啟動應用程式：

```bash
python3 main.py
```

你會在終端機看到類似以下的輸出，表示伺服器已成功啟動：
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```
接著，你可以透過另一個終端機或 API 測試工具來與系統互動，例如發送一個主題任務。

## 📁 專案結構

```
/
├── agents/             # 包含所有代理的程式碼
│   ├── commander_agent.py
│   └── crawler_agent.py
├── core/               # 核心模組，如 LLM 客戶端、工具等
│   ├── llm_client.py
│   └── tools.py
├── database/           # 資料庫相關檔案
├── data/               # 儲存輸出的資料，如 JSON 檔案
├── main.py             # 專案主程式入口 (FastAPI)
├── requirements.txt    # Python 依賴套件列表
└── README.md           # 本說明檔案
```
