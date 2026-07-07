# The Agentic Builder Vault 🛠️🤖

Welcome to **The Agentic Builder Vault**! This repository is a curated collection of templates, prompt packs, custom agent skills, and automation workflows designed for developers, creators, and "vibe coders" who build with AI.

Whether you are writing code with Claude Code, orchestrating agents, building complex workflows in n8n, or configuring Voice AI, this repository provides copy-paste resources to supercharge your productivity.

---

## 📁 Repository Structure

Here is how the vault is organized:

```text
/ (Root)
│
├── claude-code/                           # All Claude Code resources
│   ├── prompt-guides/                     # Curated PDF Prompt packs and guides
│   │   ├── Fable-5-Prompt-Guide.pdf       # Prompt guide for Fable 5 models
│   │   ├── Fable5-Higgsfield-Website...  # Prompt pack for website creation
│   │   ├── JARVIS-Prompt-Pack.pdf         # AI assistant prompt pack
│   │   ├── Social-Autopilot-Prompt-Pack   # Social media automation prompts
│   │   └── claude-sonnet5-vs-opus48...    # LLM comparison prompts
│   │
│   ├── templates/                         # Configuration and prompt templates
│   │   └── brand-voice/
│   │       ├── brand-voice-template.md    # Custom brand voice setup file (Markdown)
│   │       └── Brand-Voice-Template.pdf   # Reference guide
│   │
│   └── custom-skills/                     # Custom Claude Code Skills / Agent packs
│       ├── zips/                          # Zip files for quick installation
│       │   ├── ads-skills.zip             # Marketing & ads execution skills
│       │   ├── crypto-skills.zip          # Web3 & blockchain utilities
│       │   ├── finance-skills.zip         # Financial analysis and reporting
│       │   ├── realestate-skills.zip      # Real estate data & copy skills
│       │   ├── recruiter-skills.zip       # Recruitment & candidate sourcing
│       │   ├── scroll-cinematic.zip       # Cinematic storytelling/writing rules
│       │   └── trading-skills.zip         # Algorithmic trading and analysis
│       │
│       └── extracted/                     # Extracted folders for direct browsing
│           ├── ads/
│           ├── crypto/
│           ├── finance/
│           ├── realestate/
│           ├── recruiter/
│           ├── scroll-cinematic/
│           └── trading/
│
├── n8n/                                   # 100+ Production-ready n8n workflow templates
│   ├── workflows/                         # JSON workflow files for direct copy-paste
│   └── zips/                              # Zip file containing all workflows
│
├── voice-ai/                              # Conversational Voice AI agent templates
│   ├── agents/                            # Voice AI node and hook configurations (JSON)
│   └── zips/                              # Zip file containing all voice templates
│
└── vibe-coding/                           # Vibe coding workflows and app templates
    ├── workflows/                         # Vibe coding app configurations (JSON)
    ├── guides/                            # Video generation prompting PDF guides
    └── zips/                              # Zip file containing all vibe coding templates
```

---

## 🤖 Claude Code Custom Skills & Agents

Claude Code allows you to define custom **Skills** and **Agents** to automate complex tasks, perform specialized research, and enforce behavioral rules.

### Quick Installation

1. Navigate to the `claude-code/custom-skills/zips` folder.
2. Download the `.zip` file for the skill package you want (e.g., `ads-skills.zip`).
3. Extract the contents directly into your Claude Code customizations directory:
   * **Global Customizations:** `~/.gemini/config/` (macOS/Linux) or `C:\Users\<YourUsername>\.gemini\config\` (Windows)
   * **Workspace-Specific Customizations:** `.agents/` in the root of your project directory.
4. Restart your Claude Code session, and the new skills and subagents will be automatically discovered and loaded!

### Browse the Code
If you want to view the source code, prompts, or scripts of these skills before downloading, browse the `claude-code/custom-skills/extracted/` folder. For example:
* [Ads Skills Directory](claude-code/custom-skills/extracted/ads/) — Contains audience research, budget planning, landing page evaluation, and ad copy skills.
* [Trading Skills Directory](claude-code/custom-skills/extracted/trading/) — Contains market analysis, strategy evaluation, backtesting, and execution skills.

---

## 📝 Brand Voice Template

Teach Claude how to write exactly like you do! 

1. Copy the contents of the [brand-voice-template.md](claude-code/templates/brand-voice/brand-voice-template.md) template.
2. Place it in your Claude Code workspace.
3. Run the prompt: `"Interview me to fill in my brand voice template."`
4. Claude will ask you a series of targeted questions, fill in the file, and adapt its style to sound like you on X/Twitter, LinkedIn, YouTube, and more.

---

## 🔄 n8n Automation Workflows

We have added a catalog of **100+ production-ready n8n workflows** for automating common tasks.

* **Email & Inbox Routers:** Gmail and Outlook auto-labeling, review summaries, and auto-drafting.
* **Chatbots & Voice AI:** Twilio/Telegram/WhatsApp chatbots with contextual memory.
* **Content Autopilot:** WordPress automated publishers powered by DeepSeek R1 and Claude.
* **Developer Utilities:** GitLab automatic code review, autonomous web crawler, and API schema extraction.

To browse these workflows and learn how to import them directly to your canvas, go to the [n8n Directory](n8n/README.md).

---

## 🎙️ Voice AI Prompts & Configurations

We have added conversational Voice AI integration templates for popular APIs and telephony systems.

* **API Integrations:** Out-of-the-box configurations for Telnyx and ElevenLabs conversational agents.
* **Agent Blueprints:** Pre-designed system prompts and flows for health check-in bots and real estate lead qualification assistants.

To browse these templates and learn how to use them on your canvas, visit the [Voice AI Directory](voice-ai/README.md).

---

## 🚀 Vibe Coding Workflows & Resources

We have added structured Vibe Coding application resources and templates.

* **Ad Generators:** UGC image and video prompt workflows designed to drive generative video engines (like Veo3).
* **Conversational AI:** Modular templates to prototype speech-to-speech lead qualifiers.
* **Prompting Guides:** The Ultimate Prompting Guide for Video Generation Models PDF.

To browse these workflows and explore our vibe coding blueprints, visit the [Vibe Coding Directory](vibe-coding/README.md).

---

## 🔄 Upcoming Integrations

As the AI ecosystem expands, this repository will serve as a living library. Planned additions include:

* **Agentic IDE Configs:** Custom `.cursorrules` and prompt scripts to optimize agentic coding assistants.

---

## 🤝 Contributing & Support

If you have a prompt pack, a custom Claude Code skill, or an n8n workflow you would like to share:
1. Fork this repository.
2. Create a new branch.
3. Submit a pull request.

🌟 **If you find this repository useful, give it a star!** 

Connect with me on [LinkedIn](https://www.linkedin.com/in/YOUR-LINKEDIN-USERNAME) to stay updated on new additions, tutorials, and AI building tips.
