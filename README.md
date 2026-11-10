# 🔎 ResearchMind — AI-Powered Multi-Agent Research Assistant

ResearchMind is an AI-powered research assistant that automates the research process using multiple specialized AI agents. It searches the web, extracts relevant information, generates structured research reports, and evaluates the quality of those reports.

Built with **Python, LangChain, Groq, Tavily, and Streamlit**, ResearchMind demonstrates how multiple AI agents can collaborate to complete a complex research workflow.

## ✨ Features

- **🔎 Search Agent:** Finds relevant, recent, and reliable information from the web.
- **📖 Reader Agent:** Selects relevant URLs and extracts detailed webpage content.
- **✍️ Writer Agent:** Generates structured research reports using the gathered information.
- **🧐 Critic Agent:** Reviews generated reports, evaluates their quality, and provides constructive feedback.
- **📊 Interactive Dashboard:** A clean Streamlit interface to run research and explore results.
- **📄 Report Export:** Download generated research reports in Markdown format.
- **⚡ Automated Workflow:** Executes the four stages sequentially through a single research request.

## 🏗️ Architecture

ResearchMind follows a sequential multi-agent architecture:

```text
             USER INPUT
                  |
                  v
          +---------------+
          |  SEARCH AGENT |
          +---------------+
                  |
                  v
          +---------------+
          |  READER AGENT |
          +---------------+
                  |
                  v
          +---------------+
          |  WRITER AGENT |
          +---------------+
                  |
                  v
          +---------------+
          |  CRITIC AGENT |
          +---------------+
                  |
                  v
           RESEARCH REPORT
             + REVIEW
```

### Agent Responsibilities

| Agent | Responsibility |
|---|---|
| Search Agent | Discovers relevant web sources |
| Reader Agent | Extracts information from selected webpages |
| Writer Agent | Creates a structured research report |
| Critic Agent | Evaluates the report and suggests improvements |

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| LangChain | Agent creation and LLM orchestration |
| Groq | LLM inference |
| Tavily | Web search |
| BeautifulSoup | HTML parsing |
| Trafilatura | Webpage content extraction |
| Streamlit | Interactive frontend |
| Pydantic | Structured output validation |
| python-dotenv | Environment variable management |

## 📁 Project Structure

```text
ResearchMind/
│
├── .streamlit/
│   └── config.toml
│
├── agents.py
├── app.py
├── tools.py
├── pipeline.py
│
├── outputs/
│
├── .env
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ResearchMind.git

cd ResearchMind
```

### 2. Install dependencies

This project uses `uv` for Python package management.

Install uv if you don't already have it:

```bash
pip install uv
```

Install project dependencies:

```bash
uv sync
```

### 3. Configure environment variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Get your API keys:

- Groq: https://console.groq.com/
- Tavily: https://tavily.com/

**Important:** Never commit your `.env` file or expose your API keys publicly.

### 4. Run the application

```bash
uv run streamlit run app.py
```

The application will open in your browser, usually at:

```text
http://localhost:8501
```

## 🚀 How to Use

1. Open the ResearchMind application.
2. Enter a topic you want to research.
3. Click **Generate Research Report**.
4. Let the Search Agent find relevant information.
5. The Reader Agent extracts detailed content from selected sources.
6. The Writer Agent generates a structured report.
7. The Critic Agent evaluates the generated report.
8. Explore the results in the dashboard.
9. Download your research report in Markdown format.

## 📄 Report Structure

The Writer Agent is instructed to organize research reports into:

- Introduction
- Key Findings
- Conclusion
- Sources

The Critic Agent evaluates the report and provides:

- Overall score
- Strengths
- Areas to improve
- Final verdict

## 🔮 Future Improvements

- [ ] Implement a feedback loop between the Critic and Writer agents.
- [ ] Add iterative report refinement based on critic feedback.
- [ ] Implement source credibility and relevance scoring.
- [ ] Support multiple source extraction.
- [ ] Add PDF report generation.
- [ ] Introduce LangGraph for advanced agent orchestration.
- [ ] Add report history and persistent storage.
- [ ] Improve error handling and API rate-limit management.

## 🎯 Project Objective

The goal of ResearchMind is to explore multi-agent AI systems and understand how specialized agents can collaborate to automate complex tasks.

It demonstrates practical applications of LLMs, tool calling, web search, information extraction, structured outputs, and agent orchestration.

## 👨‍💻 Author

**Anirudha Pratap Singh**

- GitHub: https://github.com/Anirudh0024
