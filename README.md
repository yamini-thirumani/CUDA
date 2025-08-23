# 🚀 CUDA - Collaborative Unified Developer Assistant

<div align="center">



[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)](https://streamlit.io/)
[![Transformers](https://img.shields.io/badge/Transformers-4.0+-orange.svg)](https://huggingface.co/transformers/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**An intelligent multi-agent system for code analysis, optimization, and generation**

[Features](#-features) • [Architecture](#-architecture) • [Quick Start](#-quick-start) • [API Reference](#-api-reference) • [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Reference](#-api-reference)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)

## 🎯 Overview

CUDA (Collaborative Unified Developer Assistant) is an advanced AI-powered code analysis and generation system that leverages multiple specialized agents to provide comprehensive code solutions. The system combines the power of Large Language Models with intelligent agent collaboration to deliver high-quality, optimized, and well-structured code.

### Key Capabilities

- **🔧 Code Fixing**: Automatically identifies and fixes bugs and edge cases
- **🔄 Code Refactoring**: Improves code readability and modularity
- **⚡ Code Optimization**: Enhances performance and efficiency
- **🧠 Intelligent Planning**: Generates code from natural language descriptions
- **🏆 Smart Judging**: Evaluates and selects the best solution from multiple agents
- **🌐 Web Interface**: User-friendly Streamlit frontend for easy interaction

## ✨ Features

### 🤖 Multi-Agent Architecture
- **Fix Agent**: Identifies and resolves bugs, handles edge cases
- **Refactor Agent**: Improves code structure and readability
- **Optimizer Agent**: Enhances performance and efficiency
- **Judge Agent**: Evaluates solutions and selects the best one
- **Planner Agent**: Converts natural language to code
- **Code Writer Agent**: Generates code using local LLM models

### 🚀 Advanced Capabilities
- **Parallel Processing**: Multiple agents work simultaneously for faster results
- **Intelligent Scoring**: Sophisticated evaluation system for solution selection
- **Error Handling**: Robust exception handling and validation
- **Real-time Processing**: Fast response times with async operations
- **Offline Support**: Local model inference for privacy and speed

### 🎨 User Interface
- **Streamlit Web App**: Intuitive web interface for easy interaction
- **Dual Input Modes**: Support for both code and natural language input
- **Real-time Feedback**: Live processing status and results display
- **Responsive Design**: Works seamlessly across different devices

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   FastAPI       │    │   Agent System  │
│   (Streamlit)   │◄──►│   Backend       │◄──►│                 │
│                 │    │                 │    │ ┌─────────────┐ │
└─────────────────┘    └─────────────────┘    │ │ Fix Agent   │ │
                                              │ └─────────────┘ │
                                              │ ┌─────────────┐ │
                                              │ │Refactor Agent│ │
                                              │ └─────────────┘ │
                                              │ ┌─────────────┐ │
                                              │ │Optimizer    │ │
                                              │ └─────────────┘ │
                                              │ ┌─────────────┐ │
                                              │ │ Judge Agent │ │
                                              │ └─────────────┘ │
                                              └─────────────────┘
```

### System Components

1. **Frontend Layer**: Streamlit-based web interface
2. **API Layer**: FastAPI REST API for agent communication
3. **Agent Layer**: Specialized AI agents for different tasks
4. **Model Layer**: Local LLM models for code generation and analysis

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- CUDA-compatible GPU (optional, for faster inference)
- 8GB+ RAM recommended

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/cuda-assistant.git
   cd cuda-assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the backend server**
   ```bash
   python main.py
   ```

4. **Launch the frontend**
   ```bash
   cd frontend
   streamlit run app.py
   ```

5. **Access the application**
   - Frontend: http://localhost:8501
   - API Docs: http://localhost:8000/docs

## 💻 Usage

### Web Interface

1. **Open the Streamlit app** in your browser
2. **Choose input type**: Code or Prompt
3. **Enter your code or description**
4. **Click "Send"** to process
5. **View results** with detailed explanations

### API Usage

#### Code Analysis
```python
import requests

# Analyze and improve code
code = """
def divide(a, b):
    return a / b
"""

response = requests.post("http://localhost:8000/run-agents", 
                        json={"code": code})
result = response.json()

print(f"Best Code: {result['final_code']}")
print(f"Winner: {result['winner']}")
print(f"Reason: {result['reason']}")
```

#### Natural Language to Code
```python
# Generate code from description
prompt = "Create a function to calculate fibonacci numbers"

response = requests.post("http://localhost:8000/planner", 
                        json={"text": prompt})
result = response.json()

print(f"Generated Code: {result['output']}")
```

## 📚 API Reference

### Endpoints

#### `POST /run-agents`
Analyzes and improves code using multiple agents.

**Request Body:**
```json
{
  "code": "your_python_code_here"
}
```

**Response:**
```json
{
  "final_code": "improved_code",
  "winner": "agent_name",
  "reason": "explanation"
}
```

#### `POST /planner`
Converts natural language to code.

**Request Body:**
```json
{
  "text": "your_description_here"
}
```

**Response:**
```json
{
  "output": "generated_code"
}
```

#### `GET /`
Health check endpoint.

**Response:**
```json
{
  "message": "Welcome to CUDA Agent Server! Use /docs to explore."
}
```

## 📸 Screenshots

### Main Interface
![Main Interface](https://via.placeholder.com/800x400/4A90E2/FFFFFF?text=Main+Interface)

### Code Analysis Results
![Code Analysis](https://via.placeholder.com/800x400/50C878/FFFFFF?text=Code+Analysis+Results)

### Agent Comparison
![Agent Comparison](https://via.placeholder.com/800x400/FF6B35/FFFFFF?text=Agent+Comparison)

### API Documentation
![API Docs](https://via.placeholder.com/800x400/9B59B6/FFFFFF?text=API+Documentation)

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Add tests** (if applicable)
5. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
6. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request**

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/

# Format code
black .

# Lint code
flake8 .
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [DeepSeek AI](https://github.com/deepseek-ai) for the code generation models
- [Hugging Face](https://huggingface.co/) for the transformers library
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- [Streamlit](https://streamlit.io/) for the frontend framework

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/cuda-assistant/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/cuda-assistant/discussions)
- **Email**: your.email@example.com

---

<div align="center">

**Made with ❤️ by Yamini Thirumani**

[![GitHub stars](https://img.shields.io/github/stars/yaminithirumani/cuda?style=social)](https://github.com/yourusername/cuda-assistant)
[![GitHub forks](https://img.shields.io/github/forks/yaminithirumani/cuda?style=social)](https://github.com/yourusername/cuda-assistant)
[![GitHub issues](https://img.shields.io/github/issues/yaminithirumani/cuda)](https://github.com/yaminithirumani/cuda/issues)

</div>
