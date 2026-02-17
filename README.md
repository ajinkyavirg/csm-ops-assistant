# CSM Ops Knowledge Assistant 🛠️

<div align="center">

![Status](https://img.shields.io/badge/status-active-success.svg)
![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**AI-powered knowledge assistant for CSM (CloudOps) Operations Center**

*Inspired by [NanoBot's](https://github.com/HKUDS/nanobot) markdown-based approach, adapted for enterprise cloud operations*

[Features](#features) • [Installation](#installation) • [Architecture](#architecture) • [Demo](#demo) • [Roadmap](#roadmap)

</div>

---

## 📢 Project Overview

Built as a learning initiative to explore AI agents and automation concepts from [NanoBot](https://github.com/HKUDS/nanobot) and [Cloudflare's Moltworker](https://blog.cloudflare.com/moltworker-self-hosted-ai-agent/), this project delivers a practical, production-ready knowledge assistant tailored for CSM (Cloud Ops) Operations workflows.

**What makes this different:** While NanoBot focuses on academic research automation, this assistant addresses real-world cloud infrastructure operations with actual alert scenarios, troubleshooting runbooks, and SLA-driven incident response.

---

## ✨ Features

### 🎯 Core Capabilities

| Feature | Description |
|---------|-------------|
| **📚 Markdown Knowledge Base** | 6 comprehensive documentation files covering S/4HANA, IBP, CloudERP, and Server Management |
| **🤖 AI-Powered Q&A** | Natural language queries answered using Llama 3.2 via Hugging Face |
| **🌐 Web Search Integration** | Falls back to web search when knowledge base doesn't have the answer |
| **📄 PDF Export** | Generate downloadable troubleshooting guides from AI responses |
| **💬 Multi-Channel Access** | Web interface + Telegram bot for 24/7 accessibility |
| **🔒 Access Control** | Security-first design with user authentication |
| **💾 Conversation Memory** | Maintains context within sessions for follow-up questions |
| **📱 Mobile Responsive** | Beautiful UI that works on desktop, tablet, and mobile |

---

## 🗺️ Project Journey - Milestone Breakdown

### Phase 1: Foundation & Planning
**Goal:** Understand AI agent concepts and define scope

- ✅ Researched NanoBot's markdown-based agent architecture
- ✅ Analyzed Cloudflare Moltworker's approach to self-hosted AI
- ✅ Identified CSM Ops use cases (incident response, alert handling, troubleshooting)
- ✅ Set up development environment (Python, VS Code, Git)
- ✅ Obtained free Hugging Face API access

**Key Decision:** Build simplified agent focused on CSM Operations domain rather than general-purpose automation

---

### Phase 2: Knowledge Base Creation
**Goal:** Document real operational scenarios

Created 6 comprehensive markdown files based on actual CSM Ops workflows:

#### 1. **Incident Response SOP** (`incident_response.md`)
- P1-P4 severity definitions and SLAs
- Escalation matrix (L1 → L2 → L3 → Management)
- Communication templates for critical incidents

#### 2. **CloudERP Troubleshooting** (`clouderp_troubleshooting.md`)
- Login failures and authentication issues
- Report generation problems
- Performance degradation scenarios

#### 3. **Monitoring Runbook** (`monitoring_runbook.md`)
- Daily health check procedures
- Alert response playbooks
- Digital Command Center metrics
- AppOps case management lifecycle

#### 4. **IBP Operations** (`ibp_troubleshooting.md`)
Real production alerts and resolutions:
- `SID system not accessible` - System unavailability troubleshooting
- `URL availability check failed` - Web dispatcher and backend connectivity
- `HDB_HOST_STATUS_ALERT_INST` - HANA database health issues

#### 5. **S/4HANA Operations** (`s4hana_troubleshooting.md`)
Actual infrastructure alerts:
- `CPU Utilization above 90%` - Performance bottleneck resolution
- `Swap space usage above 85%` - Memory pressure handling
- `ABAP daemon framework - 405` - Background processing failures
- `Filesystem usage above 90%` - Disk space management for /hana/data, /hana/log, /hana/backup
- `Metric provider errors - 104` - Monitoring agent troubleshooting

#### 6. **Server Management** (`server_management.md`)
Infrastructure operations:
- Filesystem full alerts with cleanup procedures
- Load balancer degradation responses
- Host unreachable scenarios
- Unexpected server reboots
- Hosts stuck in maintenance mode

**Outcome:** 6 knowledge base files covering 30+ operational scenarios with SLAs, root causes, and step-by-step resolutions

---

### Phase 3: Core AI Assistant Development
**Goal:** Build functional Q&A system

**Tech Stack Selected:**
- **Backend:** Python + Flask (lightweight, easy deployment)
- **AI Model:** Meta Llama 3.2 3B (via Hugging Face Inference API)
- **Frontend:** HTML/CSS/JavaScript (no framework complexity)

**Implementation:**
- ✅ Flask web server with RESTful API
- ✅ Knowledge base loader (parses all markdown files)
- ✅ System prompt engineering (CSM Ops expert persona)
- ✅ Context window management (loads full KB into AI context)
- ✅ Conversation state management (maintains history per session)
- ✅ Error handling and graceful degradation

**Key Achievement:** Successfully created AI assistant that answers CSM Ops questions with citations to source documents

---

### Phase 4: Enhanced Capabilities
**Goal:** Add production-ready features

#### Web Search Integration
- **Challenge:** Knowledge base can't cover everything (new patches, vendor updates, emerging issues)
- **Solution:** Integrated DuckDuckGo search API
- **Behavior:** Auto-triggers on keywords ("latest", "current", "recent") or when KB has no answer
- **Workflow:** KB first → If insufficient → Web search → Combined response

#### PDF Export Functionality
- **Use Case:** Share troubleshooting guides with team, documentation for post-mortems
- **Implementation:** ReportLab for PDF generation
- **Features:** Formatted guides with timestamps, proper styling
- **Benefit:** Converts chat responses into shareable documents

#### Document Viewer
- **Feature:** Click any KB file in sidebar to view full content
- **Implementation:** Markdown to HTML conversion with modal display
- **Benefit:** Quick reference without leaving the interface

**Outcome:** Assistant can now handle both known (KB) and unknown (web) queries, with exportable results

---

### Phase 5: Multi-Channel Access
**Goal:** Make assistant accessible beyond web browser

#### Telegram Bot Development
- **Motivation:** 24/7 access from mobile devices
- **Setup:** BotFather integration, webhook-free polling architecture
- **Security:** User ID-based access control (only authorized personnel)
- **Features:**
  - `/start` - Welcome and capabilities overview
  - `/help` - Example questions and usage guide
  - `/clear` - Reset conversation history
  - Real-time typing indicators
  - Message chunking for long responses

**Implementation Details:**
- Async/await architecture for responsive performance
- Shared knowledge base and AI client with web interface
- Per-user conversation state management
- Error handling with user-friendly messages

**Outcome:** Same AI knowledge accessible via Telegram for on-call engineers, mobile users

---

### Phase 6: Professional UI/UX
**Goal:** Create production-grade interface

#### Design Principles Applied:
- **Visual Hierarchy:** Clear distinction between user/bot messages
- **Responsive Design:** Works on desktop (1920px) to mobile (375px)
- **Performance:** Smooth animations without lag
- **Accessibility:** High contrast, readable fonts, clear CTAs

#### UI Enhancements:
- Animated gradient background (subtle, professional)
- Message animations (slide-in with scale)
- Hover effects on interactive elements
- Status indicators (online badge, typing animation)
- Custom scrollbars
- Modal overlays for document viewing
- Icon-based navigation

**Color Palette:**
- Primary: SAP Blue (#1e3c72, #2a5298)
- Success: Green (#28a745)
- Background: Deep gradient (#0f2027 → #2c5364)
- Text: High contrast for readability

**Outcome:** Enterprise-grade interface that looks professional in executive demos

---

## 🏗️ Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                     User Interfaces                          │
│  ┌──────────────┐            ┌─────────────────┐            │
│  │ Web Browser  │            │ Telegram App    │            │
│  │ (Desktop/    │            │ (Mobile/        │            │
│  │  Mobile)     │            │  Desktop)       │            │
│  └──────┬───────┘            └────────┬────────┘            │
│         │                              │                     │
└─────────┼──────────────────────────────┼─────────────────────┘
          │                              │
          ▼                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Application Layer                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Flask Web Server                         │   │
│  │  ┌────────────┐  ┌──────────────┐  ┌─────────────┐  │   │
│  │  │ Web Routes │  │ Telegram Bot │  │ API Handlers│  │   │
│  │  └────────────┘  └──────────────┘  └─────────────┘  │   │
│  └──────────────────────────────────────────────────────┘   │
│                          │                                   │
│                          ▼                                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │          Core AI Processing Engine                    │   │
│  │                                                        │   │
│  │  1. Load Knowledge Base (6 markdown files)           │   │
│  │  2. Build System Prompt (CSM Ops expert context)     │   │
│  │  3. Manage Conversation State                        │   │
│  │  4. Query AI Model                                   │   │
│  │  5. Fallback to Web Search (if needed)               │   │
│  │  6. Format Response                                  │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
          │                              │
          ▼                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   External Services                          │
│  ┌──────────────────┐         ┌──────────────────┐          │
│  │ Hugging Face API │         │ DuckDuckGo       │          │
│  │ (Llama 3.2)      │         │ Web Search       │          │
│  └──────────────────┘         └──────────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow Example:

**User Query:** "What should I do if CPU is above 90% on S/4HANA?"

1. **Input** → Web UI or Telegram
2. **Routing** → Flask handles request
3. **Context Building** → Loads S/4HANA troubleshooting KB
4. **AI Query** → Sends to Llama 3.2 with full context
5. **Response Generation** → AI returns step-by-step resolution
6. **Output** → Formatted response to user
7. **Optional** → User exports as PDF for documentation

---

## 📦 Installation

### Prerequisites
- Python 3.7+
- Hugging Face account (free)
- Telegram account (optional, for bot feature)

### Quick Start

**1. Clone repository**
```bash
git clone https://github.com/ajinkyavirg/csm-ops-assistant.git
cd csm-ops-assistant
```

**2. Install dependencies**
```bash
pip install flask huggingface_hub python-dotenv markdown reportlab requests beautifulsoup4 python-telegram-bot
```

**3. Get Hugging Face API token**
- Sign up at https://huggingface.co/join
- Go to https://huggingface.co/settings/tokens
- Create token with "Write" permissions
- Copy the token

**4. Create `.env` file**
```bash
HUGGINGFACE_TOKEN=your-token-here
TELEGRAM_BOT_TOKEN=your-bot-token-here  # Optional
TELEGRAM_USER_ID=your-user-id-here      # Optional
```

**5. Run web interface**
```bash
python ops_assistant.py
```

Open browser: `http://127.0.0.1:5000`

**6. Run Telegram bot** (Optional)
```bash
python telegram_bot.py
```

---

## 🚀 Usage

### Web Interface

**Ask questions:**
- "What is the SLA for P1 incidents?"
- "How to troubleshoot HDB_HOST_STATUS_ALERT_INST?"
- "CPU above 90% on S/4HANA - what to do?"

**Browse knowledge base:**
- Click documents in left sidebar
- View full content in modal

**Export troubleshooting guides:**
- Ask a question
- Click "Export PDF" button
- Download formatted guide

### Telegram Bot

**Setup:**
1. Search for your bot on Telegram
2. Send `/start`
3. Ask questions naturally
4. Use `/help` for examples
5. Use `/clear` to reset conversation

---

## 💡 Knowledge Base Coverage

### Systems Supported
- **S/4HANA** - SAP ERP operations
- **IBP** - Integrated Business Planning
- **CloudERP** - Cloud-based ERP services
- **HANA Database** - In-memory database platform
- **Server Infrastructure** - Linux servers, load balancers

### Alert Types Covered
- Performance (CPU, memory, swap)
- Availability (system down, URL checks)
- Capacity (disk space, connections)
- Monitoring (metric collection, agent issues)
- Maintenance (scheduled, unplanned)

### Operational Workflows
- Incident classification (P1-P4)
- Escalation procedures
- Communication templates
- Post-mortem documentation
- Preventive maintenance

---

## 🎯 Comparison: NanoBot vs CSM Ops Assistant

| Aspect | NanoBot | CSM Ops Assistant |
|--------|---------|-------------------|
| **Purpose** | Academic research automation | Cloud operations support |
| **Domain** | Literature review, paper writing | Infrastructure troubleshooting |
| **Knowledge Format** | Markdown files | Markdown files ✓ |
| **AI Integration** | OpenRouter, multiple models | Hugging Face (Llama 3.2) |
| **Complexity** | ~4,000 lines (lightweight) | ~500 lines (ultra-lightweight) |
| **Channels** | CLI, Telegram, WhatsApp | Web UI, Telegram |
| **Target Users** | Researchers, academics | CSM Ops engineers, SREs |
| **Deployment** | Self-hosted, cloud | Local, easily cloud-deployable |
| **Cost** | Requires API credits | 100% free (Hugging Face free tier) |
| **Learning Curve** | Medium (requires setup) | Low (5-minute setup) |

**Key Insight:** NanoBot demonstrated the power of markdown-based AI agents. This project proves the concept works brilliantly for enterprise operations when properly scoped.

---

## 🎬 Demo

### Screenshots

**Web Interface:**
![Web Interface](docs/screenshots/web-interface.png)
*Professional gradient UI with sidebar navigation and chat interface*

**Telegram Bot:**
![Telegram Bot](docs/screenshots/telegram-bot.png)
*Mobile-first access for on-call engineers*

**PDF Export:**
![PDF Export](docs/screenshots/pdf-export.png)
*Downloadable troubleshooting guides for documentation*

### Video Demo
[Watch 5-minute demo video](docs/demo-video.mp4) *(Coming soon)*

---

## 🔮 Future Enhancements

### Planned Features (Post-Demo)

**High Priority:**
- [ ] **Voice Interface** - Speech-to-text for hands-free queries
- [ ] **Real-time Monitoring Integration** - Pull live metrics from cloud systems
- [ ] **Ticket System Integration** - Auto-create ServiceNow/Jira tickets
- [ ] **Multi-language Support** - Support for regional operations teams
- [ ] **Advanced Search** - Brave Search API for better web results
- [ ] **Audit Logging** - Track all queries for compliance

**Medium Priority:**
- [ ] **Role-Based Access** - Different permissions for L1/L2/L3 engineers
- [ ] **Custom Knowledge Base** - Allow teams to add their own documentation
- [ ] **Slack Integration** - Additional channel for team collaboration
- [ ] **Email Notifications** - Alert summaries and digest emails
- [ ] **Dashboard Analytics** - Most common queries, resolution times

**Long-term Vision:**
- [ ] **Proactive Alerts** - AI suggests checks based on patterns
- [ ] **Incident Prediction** - Machine learning on historical data
- [ ] **Auto-remediation** - Execute safe commands automatically
- [ ] **Multi-tenant** - Support multiple CSM Ops teams
- [ ] **Knowledge Graph** - Visualize relationships between issues

---

## 🛠️ Technical Details

### Tech Stack

**Backend:**
- Python 3.12
- Flask 3.0+ (web framework)
- python-telegram-bot 20.8 (bot integration)
- python-dotenv (environment management)

**AI & ML:**
- Hugging Face Inference API
- Meta Llama 3.2 3B Instruct (language model)
- Custom prompt engineering for CSM Ops domain

**Frontend:**
- HTML5
- CSS3 (Flexbox, Grid, animations)
- Vanilla JavaScript (no frameworks)
- Responsive design (mobile-first)

**Data & Storage:**
- Markdown files (knowledge base)
- In-memory conversation state
- ReportLab (PDF generation)

**Search & Integration:**
- BeautifulSoup4 (web scraping)
- DuckDuckGo HTML API (web search)
- Requests (HTTP client)

### Project Structure
```
csm-ops-assistant/
├── knowledge_base/              # Documentation files
│   ├── incident_response.md
│   ├── clouderp_troubleshooting.md
│   ├── monitoring_runbook.md
│   ├── ibp_troubleshooting.md
│   ├── s4hana_troubleshooting.md
│   └── server_management.md
├── templates/                   # Web UI
│   └── ops_assistant.html
├── ops_assistant.py            # Main web application
├── telegram_bot.py             # Telegram bot
├── .env                        # Configuration (not in Git)
├── .gitignore                  # Git exclusions
└── README.md                   # This file
```

---

## 🤝 Contributing

This is a personal learning project, but suggestions and improvements are welcome!

**To contribute:**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

MIT License - feel free to use this project for your own learning or adapt for your operations team.

---

## 🙏 Acknowledgments

**Inspired by:**
- [NanoBot](https://github.com/HKUDS/nanobot) - Ultra-lightweight AI agent architecture
- [Cloudflare Moltworker](https://blog.cloudflare.com/moltworker-self-hosted-ai-agent/) - Self-hosted AI agent concepts

**Built with:**
- Meta's Llama 3.2 language model
- Hugging Face's incredible free tier
- Python's amazing ecosystem

**Special thanks to:**
- The open-source AI community
- Everyone building the future of AI agents

---

## 📧 Contact

**Created by:** Ajinkya Virgaonkar   
**Project Type:** Learning initiative, proof of concept  
**Status:** Active development

---

<div align="center">

**⭐ If this project helped you understand AI agents, please star it! ⭐**

Built with ❤️ for CSM Operations teams everywhere

</div>