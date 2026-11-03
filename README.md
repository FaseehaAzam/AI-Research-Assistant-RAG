# 📚 AI Research Assistant — RAG-Based PDF Question Answering

An AI-powered research assistant that allows users to upload text-based PDF documents and ask questions about their contents using **Retrieval-Augmented Generation (RAG)**.

The application combines semantic search, vector embeddings, and a language model to generate answers based on information retrieved from uploaded documents.

## 🚀 Features

- Upload and process text-based PDF documents
- Extract PDF text using PyMuPDF
- Split documents into sentence-aware chunks
- Generate semantic embeddings
- Retrieve relevant passages using FAISS
- Generate answers using FLAN-T5 Large
- Display retrieved PDF page numbers
- Return "Not found in the PDF" for questions with insufficiently relevant retrieved content
- Interactive web interface built with Gradio
- Session-based document handling

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development |
| PyMuPDF | PDF text extraction |
| Sentence Transformers | Semantic embeddings |
| all-MiniLM-L6-v2 | Embedding model |
| FAISS | Vector similarity search |
| FLAN-T5 Large | Answer generation |
| Hugging Face Transformers | Language model integration |
| PyTorch | Deep learning framework |
| Gradio | Web interface |

## 🧠 How It Works

1. **PDF Upload:** The user uploads a text-based PDF document.
2. **Text Extraction:** PyMuPDF extracts readable text.
3. **Chunking:** The extracted text is divided into smaller passages.
4. **Embedding Generation:** Sentence Transformers converts passages into numerical vectors.
5. **Vector Storage:** FAISS indexes the document embeddings.
6. **Question Processing:** The user's question is converted into an embedding.
7. **Semantic Retrieval:** FAISS retrieves the most relevant passages.
8. **Answer Generation:** FLAN-T5 Large generates an answer using the retrieved context.
9. **Results:** The application displays the answer and retrieved PDF page numbers.

## 💻 Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/AI-Research-Assistant-RAG.git
cd AI-Research-Assistant-RAG
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

Open the local Gradio URL displayed in your terminal.

**Note:** Replace `YOUR_USERNAME` with your actual GitHub username. FLAN-T5 Large requires substantial memory, and GPU acceleration is recommended.

## 📖 Example Questions

After uploading a relevant research PDF, users can ask:

- What is the main objective of this research?
- Which methodology was used?
- What are the main findings?
- What limitations are discussed?
- What future improvements are suggested?

## ⚠️ Limitations

- Supports text-based PDFs; scanned PDFs require OCR.
- AI answers may be incomplete or inaccurate.
- The similarity threshold of 0.30 is experimental and may reject valid questions.
- Retrieved page numbers are not verified claim-level citations.
- Large PDF documents may require additional optimization.
- Model loading may require significant RAM or GPU memory.

## 🔮 Future Improvements

- Support scanned PDFs using OCR
- Improve document chunking and retrieval
- Add verified source citations
- Support multiple PDFs in one session
- Improve answer completeness and accuracy
- Add chat history and follow-up questions
- Deploy the application online

## 📌 Project Status

**Working prototype — tested with research PDFs using Google Colab and Gradio.**

This project demonstrates practical applications of Natural Language Processing, semantic search, and Retrieval-Augmented Generation in document-based question answering.
