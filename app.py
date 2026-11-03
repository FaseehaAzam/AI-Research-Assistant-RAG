
import re
import os
import gradio as gr
import pymupdf
import numpy as np
import faiss
import torch

from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load AI models
print("Loading AI models...")

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

device = "cuda" if torch.cuda.is_available() else "cpu"
model_name = "google/flan-t5-large"

tokenizer = AutoTokenizer.from_pretrained(model_name)
llm = AutoModelForSeq2SeqLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16 if device == "cuda" else torch.float32
).to(device)
llm.eval()

print("Models loaded successfully!")

def create_smart_chunks(pages, max_chars=700):
    chunks = []

    for page in pages:
        text = re.sub(r"\s+", " ", page["text"]).strip()
        sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", text)

        current = ""

        for sentence in sentences:
            if len(current) + len(sentence) + 1 <= max_chars:
                current += " " + sentence
            else:
                if current.strip():
                    chunks.append({
                        "page": page["page"],
                        "text": current.strip()
                    })
                current = sentence

        if current.strip():
            chunks.append({
                "page": page["page"],
                "text": current.strip()
            })

    return chunks


def process_pdf(file_path):
    if file_path is None:
        return None, "Please upload a PDF first."

    try:
        pages = []

        with pymupdf.open(file_path) as pdf:
            for number, page in enumerate(pdf, start=1):
                text = page.get_text("text", sort=True)
                if text.strip():
                    pages.append({"page": number, "text": text})

        if not pages:
            return None, "No readable text found in the PDF."

        chunks = create_smart_chunks(pages)
        texts = [chunk["text"] for chunk in chunks]

        embeddings = embedding_model.encode(
            texts, convert_to_numpy=True
        ).astype("float32")

        faiss.normalize_L2(embeddings)

        index = faiss.IndexFlatIP(embeddings.shape[1])
        index.add(embeddings)

        state = {
            "chunks": chunks,
            "index": faiss.serialize_index(index).tobytes()
        }

        return state, (
            f"PDF processed successfully!\n"
            f"Pages with readable text: {len(pages)}\n"
            f"Chunks created: {len(chunks)}"
        )

    except Exception as error:
        return None, f"Error processing PDF: {error}"


def answer_question(question, state):
    if not question.strip():
        return "Please enter a question."

    if state is None:
        return "Please upload and process a PDF first."

    index = faiss.deserialize_index(
        np.frombuffer(state["index"], dtype=np.uint8).copy()
    )

    question_embedding = embedding_model.encode(
        [question], convert_to_numpy=True
    ).astype("float32")

    faiss.normalize_L2(question_embedding)

    scores, indices = index.search(
        question_embedding, min(3, index.ntotal)
    )

    if scores[0][0] < 0.30:
        return "Not found in the PDF."

    results = [state["chunks"][int(i)] for i in indices[0]]

    context = "\n\n".join(result["text"] for result in results)

    prompt = f"""Answer the question using only the context.
Give a clear and concise answer.
If the answer is missing, say "Not found in the PDF."

Context:
{context}

Question: {question}

Answer:"""

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        max_length=512,
        truncation=True
    ).to(device)

    with torch.no_grad():
        outputs = llm.generate(
            **inputs,
            max_new_tokens=120,
            do_sample=False
        )

    answer = tokenizer.decode(
        outputs[0], skip_special_tokens=True
    )

    if answer.strip().lower().startswith("not found in the pdf"):
        return "Not found in the PDF."

    pages = sorted(set(result["page"] for result in results))

    return (
        f"{answer}\n\n"
        f"Retrieved PDF pages: {', '.join(map(str, pages))}"
    )


with gr.Blocks(title="AI Research Assistant") as demo:
    gr.Markdown("# 📚 AI Research Assistant")
    gr.Markdown(
        "Upload a text-based PDF and ask questions using RAG technology."
    )

    pdf_state = gr.State(None)

    pdf_input = gr.File(
        label="Upload Your PDF",
        file_types=[".pdf"],
        type="filepath"
    )

    process_button = gr.Button("Process PDF", variant="primary")
    status = gr.Textbox(label="Processing Status")

    question = gr.Textbox(
        label="Ask a Question",
        placeholder="What is the main objective of this document?"
    )

    ask_button = gr.Button("Ask AI")
    answer = gr.Textbox(label="AI Answer", lines=6)

    process_button.click(
        fn=process_pdf,
        inputs=pdf_input,
        outputs=[pdf_state, status]
    )

    ask_button.click(
        fn=answer_question,
        inputs=[question, pdf_state],
        outputs=answer
    )

if __name__ == "__main__":
    demo.launch()
