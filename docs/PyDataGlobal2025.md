# Building Production-Ready Research AI Assistants with One-Command Setup

Wednesday, December 10, 4:00 PM, Machine Learning & AI, Machine Learning & AI

## Summary

Academic research is often fragmented across dense PDFs, complex jargon, and scattered media articles, making it hard to access for students, interns, and the broader public. To address this, we introduce Lab Lens: an open-source Research AI Assistant that unifies a lab’s papers and media coverage into a conversational system, where anyone can ask natural language questions and receive structured answers with full source citations.

This talk demonstrates how to build and deploy a production-ready RAG pipeline that uses [Landing.AI](https://landing.ai/) for vision-based PDF parsing, Firecrawl for media extraction, and LangGraph for agentic orchestration. The entire system is containerized with FastAPI and Streamlit, launching with a single command: docker compose up.

Attendees will learn how to turn scattered research artifacts into a transparent, queryable knowledge base, making lab insights accessible, reproducible, and conversational for all.

## Description

In this talk, we introduce Lab Lens: an open-source framework for Research AI Assistant that allows labs to ingest scientific papers and media coverage, build a vector database, and query it via natural language—all in one reproducible command.

This 30-minute talk will explore:

🧠 **Architecture:** How LangGraph, FastAPI, and Streamlit are combined with agentic reasoning for document Q&A.
📄 **Multi-modal Ingestion:** How Lab Lens uses Landing.AI (vision agentic document extraction) and Firecrawl to intelligently extract content from complex PDFs and dynamic media pages.
🤖 **LLM Workflow:** How intents are classified, documents retrieved, and responses synthesized with structured JSON output and source attribution.
🔄 **Reusability and Extensibility:** How any lab or research group can plug in their own documents and deploy in minutes.
⚙️ **One-Line Setup:** How a single YAML config and docker compose up sets up ingestion, vectorization, API, UI, and Slack bot integration.

We'll conclude with a live demo showing how Lab Lens answers real research questions using citation-backed reasoning, emphasizing transparency, reliability, and ease of use.

Lab Lens is designed for reproducibility, minimal setup, and immediate utility. If you're interested in bringing GenAI to your research workflow—or your research to the world—this talk will show you exactly how.

**Target Audience:** Researchers, students, and enthusiasts wanting practical AI tools.

**Prerequisites:**

- Python knowledge
- Familiarity with containerization concepts.

**Resources Provided:** Complete open-source codebase with Docker configuration for immediate deployment.  
Remember that the main goal/advantage here is to make it accessible for the whole lab's documents (papers and media coverage), so anyone can ask about it with a source citation.
