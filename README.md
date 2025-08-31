# 🚀 Overview

SARIF Reviewer is a Python tool designed to help developers and security teams quickly review, analyze, and understand SARIF (Static Analysis Results Interchange Format) files. It provides context, filtering, and actionable insights to streamline your code review and vulnerability triage process.

## ✨ Features

* **Easy SARIF File Analysis**: Parse and review SARIF results with simple commands.
* **Contextual Insights**: Get code context and explanations for findings.
* **Configurable**: Customize analysis with your own config.
* **Clear Logging**: Track actions and errors for transparency.
* **Extensible**: Modular design for easy feature additions.

## 📦 Installation

    ```bash
    # Clone the repository
    git clone https://github.com/dmdhrumilmistry/sarif-reviewer.git
    cd sarif-reviewer

    # (Optional) Create a virtual environment
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

    pip install .
    ```

## 🛠️ Usage

* Set env variables

    ```bash
    export OPENAI_API_KEY="secret-api-key"
    ```

* See command-line options with:

    ```bash
    python -m sarif_reviewer --help
    ```

* Run Tool on Sarif File using locally hosted ollama

    ```bash
    python -m sarif_reviewer -f result.sarif -lang python -b "/path/to/source/files" -m "gpt-oss:20b" -u "http://localhost:11434/v1"
    ```
