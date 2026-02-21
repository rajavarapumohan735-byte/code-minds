from groq import Groq
from sentence_transformers import SentenceTransformer
from config import get_settings
import numpy as np

settings = get_settings()
groq_client = Groq(api_key=settings.groq_api_key)

embedding_model = None

def get_embedding_model():
    global embedding_model
    if embedding_model is None:
        embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    return embedding_model

def generate_embedding(text: str) -> list:
    model = get_embedding_model()
    embedding = model.encode(text)
    return embedding.tolist()

def generate_chat_response(messages: list, temperature: float = 0.3, max_tokens: int = 2000) -> str:
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        raise Exception(f"Error generating chat response: {str(e)}")

def build_context_from_papers(papers: list) -> str:
    if not papers:
        return "No papers available in the current workspace."

    context = "Here are the research papers in the current workspace:\n\n"
    for i, paper in enumerate(papers, 1):
        context += f"{i}. Title: {paper['title']}\n"
        context += f"   Authors: {', '.join(paper['authors']) if paper['authors'] else 'Unknown'}\n"
        context += f"   Abstract: {paper['abstract'][:300]}...\n\n"

    return context

def create_research_assistant_prompt(context: str, user_message: str) -> list:
    system_prompt = f"""You are an intelligent research assistant helping users analyze and understand academic papers.
You have access to the following research papers in the user's workspace:

{context}

Your capabilities:
- Summarize research papers clearly and concisely
- Compare and contrast multiple papers
- Answer questions about research findings
- Extract key insights and methodologies
- Help users understand complex concepts

Always base your responses on the provided papers when relevant. If asked about something not in the papers, clearly state that."""

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]
