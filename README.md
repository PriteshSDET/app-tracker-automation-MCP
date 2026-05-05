# App Tracker Automation (TypeScript/Playwright)

## Overview
This repository contains a modular, component-driven automation framework for the ABSLI App Tracker project. The framework has been successfully migrated from Python/Pytest to a modern TypeScript/Playwright architecture.

## Directory Structure
- **`/ts-framework/`**: The core TypeScript framework.
  - **`tests/`**: Playwright test scripts.
  - **`pages/`**: Page Object Models.
  - **`components/`**: Modular UI components.
  - **`locators/`**: Resilient selector definitions.
  - **`data/`**: Configuration (`.env`) and test data.
  - **`docs/`**: Documentation, rules, and user stories.
  - **`mcp/`**: Model Context Protocol (MCP) server implementation.
  - **`reports/`**: Consolidated execution reports and artifacts.

## Quick Start
To get started with the TypeScript framework:

```bash
cd ts-framework
npm install
npx playwright install
npx playwright test --headed
```

## Documentation
For detailed execution instructions and framework rules, please refer to:
- [Execution Guide](ts-framework/docs/guides/EXECUTION_GUIDE.md)
- [Autonomous Agent Rules](ts-framework/docs/rules/autonomous_agent_rules.md)

---
*Maintained by the AI Automation Team*
