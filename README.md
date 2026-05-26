# 🔬 Multi-Agent Research Assistant

> **Give it a topic. Three AI agents collaborate to search, analyze, and write a full research report.**

A production-style multi-agent AI system where specialized agents work in a pipeline: one searches the web, one analyzes the findings, and one writes a polished report — all automatically.

---

## 🎬 Demo

```
Input: "Impact of LLMs on software engineering jobs in 2025"

🔍 Search Agent      → Queries web, collects 12 sources
🧠 Analyst Agent     → Extracts 8 insights, identifies 4 themes  
✍️ Report Writer     → Generates structured 1200-word report

Output: Full markdown report with executive summary, key findings,
        trends, challenges, and recommendations + all sources cited
```

---

## ✨ Features

- 🤖 **3 Specialized Agents** — each with a distinct role, persona, and LLM prompt
- 🔍 **Real-time Web Search** — Tavily API fetches up-to-date sources
- 🧠 **Intelligent Synthesis** — Analyst identifies themes, gaps, and insights
- 📝 **Structured Reports** — Exec summary, findings, analysis, recommendations
- 📥 **Download as Markdown** — Save the report for later use
- ⚡ **Live Agent Status** — Watch each agent work in real time
- 🎚️ **Research Depth Slider** — Quick (3 sources) / Standard (5) / Deep (8)
- 💸 **Nearly free** — Groq free tier + Tavily free tier

---

## 🏗️ Architecture

```
                    User Input: "Research Topic"
                           │
              ┌────────────▼──────────────┐
              │    ResearchOrchestrator    │  ← Manages pipeline & callbacks
              └────────────┬──────────────┘
                           │
           ┌───────────────▼───────────────┐
           │         Agent 1               │
           │      🔍 Search Agent           │
           │  - Generates 3 sub-queries     │
           │  - Calls Tavily Search API     │
           │  - Deduplicates & ranks hits   │
           └───────────────┬───────────────┘
                           │  raw_results, formatted_content
           ┌───────────────▼───────────────┐
           │         Agent 2               │
           │      🧠 Analyst Agent          │
           │  - Extracts 6-10 insights      │
           │  - Identifies 3-5 themes       │
           │  - Spots knowledge gaps        │
           └───────────────┬───────────────┘
                           │  insights, themes, gaps
           ┌───────────────▼───────────────┐
           │         Agent 3               │
           │      ✍️ Report Writer Agent    │
           │  - Writes executive summary    │
           │  - Structures all sections     │
           │  - Formats citations           │
           └───────────────┬───────────────┘
                           │
              ┌────────────▼──────────────┐
              │    Final Research Report   │
              │    (Markdown + Download)   │
              └────────────────────────────┘
```

---

## 🤖 Agent Details

### Agent 1 — Search Agent
| Property | Value |
|---------|-------|
| **Role** | Web Research Specialist |
| **Tool** | Tavily Search API |
| **Input** | Raw topic string |
| **Output** | Ranked search results + formatted content block |
| **Smart Behavior** | Generates 3 focused sub-queries via LLM before searching |

### Agent 2 — Analyst Agent
| Property | Value |
|---------|-------|
| **Role** | Senior Research Analyst |
| **Tool** | Groq LLM (Llama 3) |
| **Input** | Formatted search content |
| **Output** | Numbered insights, key themes, knowledge gaps |
| **Smart Behavior** | Cites source numbers, identifies conflicts, notes missing data |

### Agent 3 — Report Writer Agent
| Property | Value |
|---------|-------|
| **Role** | Technical Report Writer |
| **Tool** | Groq LLM (Llama 3, higher temp for creativity) |
| **Input** | Insights + themes + gaps + raw sources |
| **Output** | Full markdown report with structured sections |
| **Smart Behavior** | Adds exec summary, recommendations, sources section |

---

## 🛠️ Tech Stack

| Component         | Technology              | Why                                |
|------------------|-------------------------|------------------------------------|
| LLM              | Groq API (Llama 3 8B)  | Free, fast, capable                |
| Web Search       | Tavily API              | Best search API for AI agents      |
| Agent Framework  | Custom (LangChain base) | Shows deep understanding           |
| LLM Orchestration| LangChain               | Industry standard                  |
| UI               | Streamlit               | Fast AI app development            |

---

## 📁 Project Structure

```
multi-agent-research-assistant/
├── app.py                          # Main Streamlit application
├── agents/
│   ├── __init__.py
│   ├── base_agent.py               # Abstract base class for all agents
│   ├── search_agent.py             # Agent 1: Web search via Tavily
│   ├── analyst_agent.py            # Agent 2: Insight extraction & synthesis
│   ├── report_writer_agent.py      # Agent 3: Final report compilation
│   └── orchestrator.py             # Pipeline manager + status callbacks
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- Free [Groq API key](https://console.groq.com) (2 minutes to get)
- Free [Tavily API key](https://app.tavily.com) (2 minutes to get)

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/multi-agent-research-assistant.git
cd multi-agent-research-assistant
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
# Edit .env with your actual API keys
```

```env
GROQ_API_KEY=gsk_your_key_here
TAVILY_API_KEY=tvly_your_key_here
```

### 5. Run the application

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## 🧪 Usage

1. Enter both API keys in the sidebar (or set them in `.env`)
2. Choose a **Research Depth** (Quick / Standard / Deep)
3. Type a research topic in the input box
4. Click **🚀 Research**
5. Watch the 3 agents work live (green check = complete)
6. Read the report in the **Full Report** tab
7. Download as Markdown with the ⬇️ button

---

## 🔑 Key Concepts Demonstrated

| Concept                          | Where                               |
|---------------------------------|-------------------------------------|
| Multi-agent pipeline design      | `agents/orchestrator.py`            |
| Agent abstraction / base class   | `agents/base_agent.py`              |
| Tool use (web search)            | `agents/search_agent.py`            |
| LLM prompt engineering           | All agent files                     |
| Inter-agent data passing         | `orchestrator.py` → each agent      |
| Status callbacks / live UI       | `orchestrator.py` + `app.py`        |
| Graceful error handling          | `search_agent.py` (try/except)      |
| Structured output parsing        | `analyst_agent.py`                  |

---

## ⚙️ Configuration

| Parameter          | Default         | Where to change       | Effect                       |
|-------------------|-----------------|-----------------------|------------------------------|
| `max_results`     | 5               | Sidebar slider        | More sources = richer report |
| LLM model         | llama3-8b-8192  | `base_agent.py`       | Swap to llama3-70b for depth |
| Writer temperature| 0.4             | `report_writer_agent` | Higher = more creative prose |
| Analyst max_tokens| 3000            | `analyst_agent.py`    | More = longer analysis       |

---

## 📈 Possible Extensions

- [ ] Add a **Fact-Checker Agent** (Agent 4) to verify claims
- [ ] Add **memory** so agents can reference previous research sessions
- [ ] Integrate **Google Scholar** for academic sources
- [ ] Add **PDF export** of the final report
- [ ] Implement **parallel search** (multiple queries simultaneously)
- [ ] Add **critique-and-revise loop** between Analyst and Writer
- [ ] Deploy to Hugging Face Spaces or Streamlit Cloud

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements

- [LangChain](https://langchain.com) — LLM orchestration
- [Groq](https://groq.com) — Ultra-fast LLM inference
- [Tavily](https://tavily.com) — AI-optimized search API
- [Streamlit](https://streamlit.io) — AI app framework
