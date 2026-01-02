# Agentic AI Content Generation System

## Overview
This project implements an **Agentic AI-based pipeline** that transforms raw skincare product data into structured data models, highly relevant FAQs, and comparative analysis tables.

Unlike simple template engines, this system uses **LangGraph** to orchestrate intelligent agents powered by **Google Gemini**.

## Key Features
- **Agentic Architecture**: Built on LangGraph, creating a directed acyclic graph (DAG) of autonomous agents.
- **LLM-Powered Generation**: Uses `gemini-flash-latest` for intelligent reasoning, not just text replacement.
- **Structured Output**: Enforces strict JSON schemas using Pydantic models.
- **Comparison Engine**: An autonomous agent analyzes two products to create an objective comparison verdict.

## Project Structure

```text
Multi_Agent_Content_Generation_System/
├─ README.md
├─ requirements.txt
├─ src/
│  ├─ agents/
│  │  ├─ parser_agent.py          # Extracts structured data
│  │  ├─ question_generator.py    # Generates relevant FAQs
│  │  ├─ comparison_agent.py      # Performs competitive analysis
│  │  └─ page_assembler_agent.py  # Saves final artifacts
│  ├─ core/
│  │  └─ graph.py                 # LangGraph Graph Definition
│  ├─ domain/
│  │  └─ models.py                # Pydantic Data Models
│  └─ main.py                     # Entry point
├─ product_page.json              # Generated Output
├─ faq.json                       # Generated Output
└─ comparison_page.json           # Generated Output
 ```

## Setup & Running

1. **Install Dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

2. **Set API Key**
   Get a free key from [Google AI Studio](https://aistudio.google.com/).
   ```powershell
   $env:GOOGLE_API_KEY="your-key-here"
   ```

3. **Run the Pipeline**
   ```powershell
   python src/main.py
   ```

## Architecture
The system follows a sequential agent workflow:
1. **Parser Node**: Intelligent extraction of data from input.
2. **Parallel Processing**:
   - **FAQ Node**: Generates user-centric questions.
   - **Comparison Node**: Analyzes competitor data.
3. **Assembly Node**: Aggregates state and writes final JSON files.
