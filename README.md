# Build Your Own AI Clone

This project is automatically generated.

## Installation

```sh
pip install -r requirements.txt
```
# My AI Clone 🤖

This project is a personalized AI chatbot built using a RAG (Retrieval-Augmented Generation) pipeline. It uses your own documents as a knowledge base to answer questions.

## Tech Stack

- **Framework**: Streamlit
- **LLM**: Llama 3 (via Groq API)
- **Core Libraries**: LangChain
- **Vector Database**: ChromaDB
- **Embeddings**: Hugging Face (all-MiniLM-L6-v2)

##this is for any person who wants to create his/her own AI clone just like this project you can follow the steps
## How to Run               

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/mishraparth/Build-Your-Own-AI-Clone_HiDevs.git

    cd Build-Your-Own-AI-Clone_HiDevs

    ```

2.  **Create a `.env` file** and add your Groq API key:
    ```
    GROQ_API_KEY="your-secret-key-here"
    ```

3.  **Install the required libraries:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Add your knowledge base PDF** to the `data/` folder. Make sure the filename in `app.py` matches the file you uploaded.

5.  **Run the Streamlit app:**
    ```bash
    streamlit run app.py
    ```
