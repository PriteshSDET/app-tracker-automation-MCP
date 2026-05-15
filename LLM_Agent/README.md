# LLM Agent Folder Overview

This folder contains the intelligent agent scaffolding for:
- storing context and chat history
- reviewing artifacts against folder 1 rules
- preparing prompts for MCP workflows
- supporting audit and review automation

## Agents

- **LLMAgent**: Base agent class for context management and prompt creation
- **QAAuditorAgent**: Specialized agent for auditing test artifacts against QA rules from the Rules folder

Use this folder as the foundation for integrating LLM-based test generation and validation.
