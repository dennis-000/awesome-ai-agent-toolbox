# Voice AI Prompts & Configurations 🎙️🤖

This directory contains production-ready configuration templates, API hooks, and prompts for setting up conversational Voice AI agents (e.g., Telnyx, ElevenLabs, Vapi, Retell).

You can download the full bundle directly as a zip file from [voice-ai-agents-bundle.zip](zips/voice-ai-agents-bundle.zip).

---

## 📂 Featured Voice AI Templates

Here is the index of available templates in this directory:

* [Telnyx Voice Agent Hook](agents/telynx-voice-agent.json) — Hook configurations and API templates for triggering and controlling conversational voice assistants via Telnyx TeXML.
* [ElevenLabs Agent Integration](agents/eleven-labs-agent.json) — Configuration template for setting up conversational voice pipelines using ElevenLabs text-to-speech, transcription, and LLM backends.
* [Health Checkin Voice Agent](agents/health-checkin-voice-ai-agent.json) — System prompt and tool config for patient check-ins, automated follow-ups, and logging answers.
* [Real Estate Lead Qualification Agent](agents/lead-qualification---real-estate.json) — Conversational flow designed to qualify property buyers, budget ranges, and interest areas.
* [Generic Voice Agent Workflows](agents/my-workflow-3.json) and [workflow-46](agents/my-workflow-46.json) — Pipeline templates for handling voice events, transcribing audio files, and storing transcripts.

---

## 🚀 How to Import into your Automation Canvas

These configurations are exported as n8n-compatible JSON node structures for orchestrating Voice AI events:

1. Browse to any agent `.json` file in the [agents/](agents/) directory.
2. Open the file and copy its entire raw JSON content.
3. Open your automation canvas.
4. Press `Ctrl + V` (Windows) or `Cmd + V` (macOS) to paste the nodes directly onto the canvas!
5. Replace placeholders (like `YOUR_TELNYX_API_KEY`) with your own API credentials in the HTTP Request nodes.
