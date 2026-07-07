# n8n Automation Workflows 🔄

This directory contains **100+ production-ready n8n workflow templates** to automate content generation, email routing, chatbot agents, data extraction, and developer workflows.

You can download the full bundle directly as a zip file from [n8n-workflows-bundle.zip](zips/n8n-workflows-bundle.zip).

---

## 🚀 How to Import Workflows into n8n

1. Browse to any workflow `.json` file in the [workflows/](workflows/) directory.
2. Open the file and copy its entire raw JSON content.
3. Open your n8n editor canvas.
4. Simply press `Ctrl + V` (Windows) or `Cmd + V` (macOS) to paste the workflow directly onto the canvas!
5. Configure your credentials for the nodes, and you're ready to run.

---

## 📂 Featured Workflows by Category

Here is a curated index of the top workflows available in this directory:

### ✉️ Email & Communication AI Agents
* [Auto-Label Gmail Messages with AI](workflows/auto-label-incoming-gmail-messages-with-ai-nodes.json) — Auto-sort and label incoming Gmail messages using LLMs.
* [Gmail Labeling Agent (Alternative Version)](workflows/gmail-labeling-agent.json) — Another implementation for automated inbox management.
* [Compose Reply Draft in Gmail with OpenAI Assistant](workflows/compose-reply-draft-in-gmail-with-openai-assistant.json) — Draft email responses based on incoming threads.
* [Auto Categorise Outlook Emails](workflows/auto-categorise-outlook-emails-with-ai.json) — AI categorization for Microsoft Outlook users.
* [Analyze Suspicious Emails with ChatGPT Vision](workflows/analyze-suspicious-email-contents-with-chatgpt-vision.json) — Screen screenshots of suspicious emails for phishing attempts.

### 🎙️ Chatbots, Messaging & Voice AI
* [Build a Telegram AI Assistant with Voice & Text](workflows/angie,-personal-ai-assistant-with-telegram-voice-and-text.json) — A complete conversational bot using voice notes.
* [AI Slack Bot with Google Gemini](workflows/creating-a-ai-slack-bot-with-google-gemini.json) — Connect Slack directly to Gemini Pro/Flash.
* [WhatsApp AI Chatbot with PostgreSQL Memory](workflows/complete-business-whatsapp-ai-powered-rag-chatbot-using-openai.json) — WhatsApp customer support bot with contextual thread memory.
* [First WhatsApp Chatbot Tutorial Node](workflows/building-your-first-whatsapp-chatbot.json) — Introductory guide for setting up WhatsApp Webhooks.
* [Discord AI Bot](workflows/discord-ai-powered-bot.json) — AI chat integrations for Discord servers.

### 📝 AI Blogging & Content Autopilot
* [WordPress Blog Creator with DeepSeek R1](workflows/automate-content-generator-for-wordpress-with-deepseek-r1.json) — Write and publish content automatically using DeepSeek R1 models.
* [Automate Blog Creation in Brand Voice](workflows/automate-blog-creation-in-brand-voice-with-ai.json) — Connect custom brand voice guidelines to your WordPress publishing.
* [Auto-Tag WordPress Posts with AI](workflows/auto-tag-blog-posts-in-wordpress-with-ai.json) — Dynamic tagging for SEO and indexing.
* [Publish Blog Posts From Google Sheets](workflows/author-and-publish-blog-posts-from-google-sheets.json) — A spreadsheet-to-CMS automation pipe.
* [Pinterest Analyzer & Content Suggester](workflows/automate-pinterest-analysis-&-ai-powered-content-suggestions-with-pinterest-api.json) — Monitor pins and use AI to draft creative content.
* [Create Dynamic Twitter Profile Banner](workflows/create-dynamic-twitter-profile-banner.json) — Refresh your Twitter banner based on stats/time.

### 🧠 Advanced RAG & Document AI Assistants
* [Financial Documents Assistant with Qdrant & Mistral](workflows/build-a-financial-documents-assistant-using-qdrant-and-mistral-ai.json) — Parse and query PDFs/reports.
* [Tax Code Assistant with Qdrant & OpenAI](workflows/build-a-tax-code-assistant-with-qdrant,-mistral-ai-and-openai.json) — Search and answer complex legal/tax compliance questions.
* [BambooHR AI Policy & Benefits Chatbot](workflows/bamboohr-ai-powered-company-policies-and-benefits-chatbot.json) — Internal HR bot answering policy questions for employees.
* [CV Resume PDF Parser with Multimodal Vision](workflows/cv-resume-pdf-parsing-with-multimodal-vision-ai.json) — Extract skills and details from CVs using vision LLMs.
* [CV Screening with OpenAI](workflows/cv-screening-with-openai.json) — Standard text-based recruitment scanner.

### 🛠️ Developer & Productivity Utilities
* [ChatGPT Automatic Code Review in GitLab MR](workflows/chatgpt-automatic-code-review-in-gitlab-mr.json) — Automate pull request reviews and post findings directly as comments.
* [API Schema Extractor](workflows/api-schema-extractor.json) — Automatically query documentation and generate schemas.
* [Autonomous AI Web Crawler](workflows/autonomous-ai-crawler.json) — Intelligent web agent crawling pages to extract specific data.
* [Extract Spending History from Gmail to Google Sheets](workflows/extract-spending-history-from-gmail-to-google-sheet.json) — Automatically track receipts and purchases.
