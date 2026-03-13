# OpenRouter Small Application

A simple Python application that demonstrates how to use the OpenRouter API.

## Setup Instructions

### Prerequisites

- Python 3.11 (tested)
- pip (Python package installer)

### Setting Up the Environment

1. **Create a virtual environment**

   ```bash
   # Windows
   python -m venv .venv
   .\.venv\Scripts\activate

   # macOS/Linux
   python -m venv .venv
   source .venv/bin/activate
   ```

2. **Install required packages**

   ```bash
   pip install openrouter requests python-dotenv
   ```

3. **Create a .env file**

   Create a `.env` file in the root directory with your OpenRouter API key:

   ```
   OPENROUTER_API_KEY=your_api_key_here
   ```

   You can get an API key by signing up at [OpenRouter](https://openrouter.ai/).

## Running the Application

Activate your virtual environment and run the demo application with:

```bash
python demo-app.py
```

## Additional Resources

- [OpenRouter Documentation](https://openrouter.ai/docs)