# Project Documentation

## Problem Statement

Users often struggle to understand skincare products due to fragmented information spread across ingredient lists, usage instructions, FAQs, and comparison pages. Manually collecting, organizing, and presenting this information is time-consuming and error-prone.

There is a need for an automated system that can process raw product data and transform it into structured, reusable, and comparison-ready outputs in a consistent manner.


## Solution Overview

This project implements an agentic AI-based pipeline that converts raw product information into structured data models and generates multiple outputs such as product pages, FAQs, and comparison pages.

The system is built using specialized agents, each responsible for a single task, ensuring modularity, scalability, and clarity. Shared data models enable seamless communication between agents and maintain consistency across all outputs.


## Scopes & Assumptions

### Scope
- The system processes skincare product information provided as structured or semi-structured input.
- It generates product details, FAQs, and comparison outputs in JSON format.
- The pipeline supports multiple agents executing sequentially.
- The system is designed for informational purposes.

### Assumptions
- Input product data is relevant and reasonably clean.
- Currency is assumed to be INR unless specified otherwise.
- The system does not provide medical or dermatological advice.
- Products being compared belong to the same category.


## System Design

### Architecture Overview

The system follows an agent-based pipeline architecture. Each agent performs a well-defined responsibility and passes structured data to subsequent agents through a shared context.

This design ensures separation of concerns, ease of extension, and predictable data flow.


### Components

#### 1. ParserAgent
- Accepts raw product input data.
- Extracts relevant fields such as name, ingredients, benefits, usage instructions, and pricing.
- Creates and stores a structured `ProductModel` object in the shared context.

#### 2. QuestionGeneratorAgent
- Reads the structured `ProductModel`.
- Generates frequently asked questions and answers based on product attributes.
- Produces a list of `FAQItem` objects.

#### 3. PageAssembler Agents
- Consume structured data from the context.
- Assemble:
  - Product detail pages
  - FAQ pages
  - Product comparison pages
- Output data in JSON format for downstream consumption.


### Data Models

#### ProductModel
- Represents a standardized product structure.
- Stores attributes such as product name, concentration, skin type, ingredients, benefits, usage instructions, side effects, price, and currency.

#### FAQItem
- Represents a single frequently asked question.
- Contains question text, answer text, and category information.

#### ComparisonModel
- Holds two `ProductModel` objects.
- Enables structured side-by-side comparison between products.


### Data Flow

1. Raw product data is provided as input to the system.
2. ParserAgent processes the input and creates a `ProductModel`.
3. QuestionGeneratorAgent generates FAQs using the structured product data.
4. PageAssembler agents consume all structured data and generate final output JSON files.
5. Generated outputs are stored for further use or presentation.


### Design Principles

- **Modularity**: Each agent handles a single responsibility.
- **Reusability**: Shared data models enable reuse across agents.
- **Scalability**: New agents or output formats can be added without impacting existing components.
- **Maintainability**: Clear separation of logic and data structures improves readability and debugging.
![alt text](<ai_agents.png>)