# 🤖 AI Document Summarizer

An automated AI workflow that analyzes documents and generates clear, structured summaries using **Make.com** and **Google Gemini**.

## 🔄 How It Works

📄 **Document**
→ ⚙️ **Make.com Automation**
→ 🧠 **Google Gemini**
→ 📝 **Structured AI Summary**
→ 📧 **Gmail**

## ✨ Features

- 📄 Automatically processes document content
- 🧠 Uses Google Gemini to analyze the document
- 📝 Generates a clear and structured summary
- 📧 Automatically sends the summary through Gmail
- ⚡ Fully automated workflow using Make.com
- 🐍 Includes a completely working Python implementation
- 🔐 Uses Google OAuth authentication and Google APIs

## 🛠️ Technologies Used

- ⚙️ Make.com
- 🐍 Python
- 🧠 Google Gemini / Gemini 2.5 Flash
- 📧 Gmail / Gmail API
- 📄 Google Docs / Google Docs API
- 🔐 Google OAuth 2.0
- 📦 Google API Python Client

## 🎯 Purpose

The idea behind this project is to automate document summarization instead of manually copying the content into an AI tool and sending the result yourself.

The project was initially built as an automated Make.com workflow and also includes a completely working Python implementation of the same core idea.

## 📸 Workflow

![Make.com Workflow](Screenshots/AI%20Agent%20WorkFlow.PNG)

## 🚀 Automation Flow

### ⚙️ Make.com Version

1. 📄 A document is detected.
2. ⚙️ Make.com processes the workflow.
3. 🧠 Google Gemini analyzes the document content.
4. 📝 Gemini generates a structured summary.
5. 📧 Gmail automatically sends the final result.

### 🐍 Python Version

1. 🔐 Python authenticates with Google using OAuth 2.0.
2. 📄 The Google Docs API reads the document content.
3. 📝 The Python script extracts the document text.
4. 🧠 Gemini 2.5 Flash generates the summary.
5. 📧 The Gmail API sends the generated summary.

The Python implementation is contained in `ai_agent.py` and has been successfully tested from start to finish.

## 💡 Example

**Input:**  
A long educational or project document.

**Output:**  
A concise, structured AI-generated summary containing the important information from the document.

## 🐍 Python Implementation

The Python version is a fully working implementation of the document summarization workflow.

It combines **Google Docs API**, **Gemini 2.5 Flash**, and **Gmail API** to automate the complete process from reading the document to sending the generated summary.

### Python Project Files

- `ai_agent.py` — Main Python script containing the complete workflow
- `requirements.txt` — Required Python packages
- `.gitignore` — Prevents sensitive files such as API keys and OAuth credentials from being uploaded

## 🔗 Built With

This project is built as a practical experiment with AI automation, Make.com, Python, Google APIs, and Google Gemini.

---

### 🚀 Try Make.com

Want to build your own AI-powered automation?

👉 **[Sign Up Make.com for free](https://www.make.com/en/register?pc=nawaidai)**

*Affiliate link — thanks for supporting the project.*
