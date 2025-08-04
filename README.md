# LLM Document Processing System

This project is an intelligent system that uses Large Language Models (LLMs) to process natural language queries and retrieve relevant information from large unstructured documents such as policy documents, contracts, and emails.

It takes a simple query, semantically searches a collection of documents for relevant clauses, and uses an LLM to generate a structured JSON response containing a decision and its justification, citing the exact source clauses.

## Features

-   **Natural Language Query Processing**: Understands queries written in plain English.
-   **Semantic Document Search**: Finds relevant information in PDFs and Word documents based on meaning, not just keywords.
-   **AI-Powered Reasoning**: Evaluates retrieved clauses to make logical decisions.
-   **Explainable & Auditable**: Justifies every decision by citing the specific text from the source documents.
-   **Structured JSON Output**: Delivers clean, predictable JSON responses ideal for downstream applications.

## Tech Stack

-   **Backend**: Python
-   **API Framework**: FastAPI
-   **LLM**: Google Gemini API
-   **Embeddings**: Sentence-Transformers
-   **Vector Database**: ChromaDB (local)

***

## ⚙️ Setup and Installation

Follow these steps carefully to set up and run the project on your local machine.

### Prerequisites

-   **Git**: Required for cloning repositories.
-   **Python 3.11**: This project is tested and optimized for Python 3.11. Using newer versions like 3.12+ may lead to installation issues as not all required packages have been updated. You can download Python 3.11 [here](https://www.python.org/downloads/release/python-3119/).

### Step 1: Get the Project Files

Clone the repository or ensure all the project files (`app.py`, `utils.py`, etc.) are in a single folder on your computer.

### Step 2: Place Your Documents

Create a folder named `documents` inside your main project folder. Place all the PDF or `.docx` files you want the system to analyze into this folder.

### Step 3: Set Up Your Google AI API Key

An API key is required to use the Google Gemini model.

1.  **Get a Key**: Go to [Google AI Studio](https://aistudio.google.com/) to create your API key.
2.  **Enable Billing**: The free tier has very strict rate limits. To avoid `429 Quota Exceeded` errors, it's highly recommended to use a standard Google account and [enable a billing account](https://console.cloud.google.com/billing) for your project.
3.  **Create `.env` file**: In the main project folder, create a file named `.env`.
4.  **Add Your Key**: Open the `.env` file and add your API key in the following format:
    ```
    GOOGLE_API_KEY="PASTE_YOUR_API_KEY_HERE"
    ```

### Step 4: Create and Activate a Virtual Environment

This isolates the project's dependencies from your main system. Open your terminal in the project folder and run the appropriate commands for your operating system.

**On Windows:**
```bash
# Create the virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\activate
```

**On macOS / Linux:**
```bash
# Create the virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate
```
You'll know it's active when you see **`(venv)`** at the beginning of your terminal prompt.

### Step 5: Install Dependencies

With your virtual environment active, install all the required packages from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

***

## 🚀 Running the Application

Once the setup is complete, you can start the API server.

1.  Make sure your virtual environment is still active.
2.  Run the following command in your terminal:

    ```bash
    uvicorn app:app --host 0.0.0.0 --port 8000
    ```
3.  The terminal will show logs indicating the server is running, including the document indexing process. Once you see `Application startup complete`, the system is ready.

## 🧪 How to Use the API

The easiest way to test the system is through the interactive API documentation.

1.  Open your web browser and navigate to: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
2.  Click on the green `POST /process_query/` bar to expand it.
3.  Click the **`Try it out`** button.
4.  In the **Request body** text box, enter your query in JSON format.
    ```json
    {
      "query": "Is a 46-year-old male covered for knee surgery if his policy is only 3 months old?"
    }
    ```
5.  Click the blue **`Execute`** button.
6.  Scroll down to see the **Server response** with the decision and justification.

***

## 🤔 Troubleshooting

If you run into issues, check this guide for common solutions.

| Problem                                                                  | Cause                                                                       | Solution                                                                                                                                                                                                       |
| ------------------------------------------------------------------------ | --------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`ModuleNotFoundError`** (e.g., `No module named 'dotenv'`)              | Your virtual environment is not active.                                     | Run `source venv/Scripts/activate` (Windows) or `source venv/bin/activate` (Mac/Linux) in your terminal before running any Python scripts.                                                                     |
| **Editor shows "Import ... could not be resolved"** | Your code editor (VS Code) is not using the correct Python interpreter.     | In VS Code, press `Ctrl+Shift+P`, search for `Python: Select Interpreter`, and choose the one that includes `venv` in its path (e.g., `./venv/Scripts/python.exe`).                                              |
| **`429 Quota Exceeded`** error                                            | You have hit the API's free tier rate limit.                                | The best solution is to [enable billing](https://console.cloud.google.com/billing) on your Google Cloud project. Alternatively, wait a few minutes and test less frequently.                                        |
| **`404 Model Not Found`** error                                           | The model name in `utils.py` is outdated.                                   | Run the `find_models.py` script (`python find_models.py`) to get a list of currently available models. Copy a suitable name (e.g., `models/gemini-1.5-flash-latest`) and update the `llm` variable in `utils.py`. |
| **Installation fails or gets stuck in a loop** | You are using an incompatible version of Python.                            | Uninstall your current Python version and install **Python 3.11**. This project is tested and stable on this version.                                                                                           |

