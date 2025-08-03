# 📚 HealthAI - Technical Documentation

## Table of Contents
- [Architecture Overview](#architecture-overview)
- [System Requirements](#system-requirements)
- [Installation Guide](#installation-guide)
- [API Integration](#api-integration)
- [Core Components](#core-components)
- [Data Flow](#data-flow)
- [Security Implementation](#security-implementation)
- [Troubleshooting](#troubleshooting)
- [Development Guide](#development-guide)
- [Deployment](#deployment)

## Architecture Overview

HealthAI is built using a modular architecture that separates concerns and ensures scalability:

```
+-----------------+    +------------------+    +-----------------+
| Streamlit UI    |--->| Core Logic       |--->| IBM Watson API  |
| (Frontend)      |    | (Backend)        |    | (AI Service)    |
+-----------------+    +------------------+    +-----------------+
         |                       |                       |
         v                       v                       v
+---------+           +-------------+         +-------------+
| Patient |           | Health Data |         | AI Models    |
| Profile |           | Processing  |         | (Granite)    |
+---------+           +-------------+         +-------------+
```

### Key Components
- **Frontend**: Streamlit-based web interface
- **Backend**: Python application logic
- **AI Service**: IBM Watson Machine Learning
- **Data Layer**: Local file processing and session management

## System Requirements

### Minimum Requirements
- **OS**: Windows 10, macOS 10.14, or Linux (Ubuntu 18.04+)
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 1GB free space
- **Internet**: Stable connection for API calls

### Recommended Requirements
- **Python**: 3.9+
- **RAM**: 16GB for optimal performance
- **CPU**: Multi-core processor
- **Storage**: SSD for faster file processing

## Installation Guide

### Step 1: Environment Setup

```bash
# Create virtual environment
python -m venv healthai_env

# Activate virtual environment
# On Windows:
healthai_env\Scripts\activate
# On macOS/Linux:
source healthai_env/bin/activate
```

### Step 2: Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt

# Verify installation
python -c "import streamlit; print('Streamlit version:', streamlit.__version__)"
```

### Step 3: Environment Configuration

Create `.env` file with the following structure:

```env
# IBM Watson Credentials
WATSONX_API_KEY=your_api_key_here
WATSONX_PROJECT_ID=your_project_id_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com

# Optional: Application Settings
DEBUG_MODE=False
LOG_LEVEL=INFO
```

### Step 4: Verify Installation

```bash
# Test the application
streamlit run app.py

# Check for any import errors
python -c "from app import HealthAIAssistant; print('Installation successful!')"
```

## API Integration

### IBM Watson Machine Learning Integration

#### Authentication Flow
1. **API Key Validation**: Verify credentials on startup
2. **Token Generation**: Request OAuth token from IBM Cloud
3
