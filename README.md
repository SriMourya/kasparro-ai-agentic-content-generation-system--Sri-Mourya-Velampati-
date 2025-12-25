# Agentic AI Content Generation System

## Overview
This project implements an agentic AI-based pipeline that transforms raw skincare product data into structured data models and automatically generates product pages, FAQs, and comparison-ready outputs.

The system is designed using modular, task-specific agents that operate sequentially on shared data models, with a strong focus on clean system design and maintainability.

## Key Concepts
- Modular agent-based architecture
- Structured data models using Python dataclasses
- Automated FAQ and comparison generation
- Clear separation of parsing, generation, and assembly stages

## Project Structure

```text
Multi_Agent_Content_Generation_System/
├─ README.md
├─ docs/
│  ├─ projectdocumentation.md
│  └─ ai_agents.png
├─ src/
│  ├─ agents/
│  ├─ core/
│  ├─ domain/
│  ├─ templates/
│  └─ main.py
├─ comparison_page.json
├─ faq.json
├─ product_page.json

## Documentation
Detailed system design, architecture, data flow, and design principles are available here:

👉 **docs/projectdocumentation.md**


