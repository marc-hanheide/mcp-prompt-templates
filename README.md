# MCP Analysis Templates

An MCP server for managing and serving analysis templates and prompt chains.

## Overview

This repository contains a Model Context Protocol (MCP) server implementation that provides standardized templates for various types of content analysis:

- Meeting Analysis (detailed meeting minutes and action items)
- Meeting Summary (executive-style brief summary)
- Webinar to Blog Post conversion

## Structure

```
mcp-analysis-templates/
├── README.md
├── requirements.txt
├── server.py
├── config.yaml
├── templates/
│   ├── meeting_analysis/
│   │   ├── template.md
│   │   └── config.yaml
│   ├── meeting_summary/
│   │   ├── template.md
│   │   └── config.yaml
│   └── webinar_blog/
       ├── template.md
       └── config.yaml
└── docs/
    ├── setup.md
    └── usage.md
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python server.py
```

## Usage

The server provides templates through the MCP protocol. Connect to it using any MCP client to access the templates.

See the docs directory for detailed setup and usage instructions.