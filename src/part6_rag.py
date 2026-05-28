"""
PART 6: Retrieval-Augmented Generation (RAG)
=============================================

WHAT YOU'LL LEARN:
- What RAG is and why it matters
- How to split documents into chunks
- How embeddings and vector stores work
- How to retrieve relevant context and feed it to the model

RUN: python src/part6_rag.py

WHAT IS RAG?
LLMs only know what they were trained on. If you want them to answer
questions about YOUR data (docs, code, notes), you need to:
  1. Store your data in a searchable format (vector store)
  2. When a question comes in, find the relevant chunks
  3. Feed those chunks to the model as context

That's RAG: Retrieve relevant context, then Generate an answer.

Without RAG: "What's our refund policy?" → model guesses or says "I don't know"
With RAG:    "What's our refund policy?" → finds the policy doc → answers accurately
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

load_dotenv()


# ============================================================
# STEP 1: Our "Knowledge Base"
# ============================================================
# In a real app, this would be loaded from files, a database,
# or an API. Here we define it inline so you can see exactly
# what the model has access to.

DOCUMENTS = [
    """Company: TechStart Inc.
Founded: 2023
Product: An AI-powered project management tool called "FlowBoard"
Pricing: Free tier (up to 3 projects), Pro ($12/month), Enterprise (custom)
Refund Policy: Full refund within 14 days of purchase. No refunds after 14 days.
Pro features include: unlimited projects, AI task prioritization, team analytics.""",

    """FlowBoard Technical Architecture:
- Frontend: React with TypeScript
- Backend: Python FastAPI
- Database: PostgreSQL with pgvector for AI features
- AI: Uses GPT-4o-mini for task suggestions and prioritization
- Hosting: AWS (ECS for backend, CloudFront for frontend)
- The AI prioritization model runs every 15 minutes per workspace.""",

    """FlowBoard Roadmap Q3 2026:
- Launch mobile app (iOS first, Android Q4)
- Add Slack integration for task creation via messages
- Implement "Focus Mode" that hides low-priority tasks
- Beta test voice commands for task creation
- Expand AI to suggest task dependencies automatically
Priority: Mobile app is the #1 priority per customer feedback.""",

    """FlowBoard Customer Support FAQ:
Q: How do I reset my password?
A: Click "Forgot Password" on the login page. Check your email for a reset link.

Q: Can I export my data?
A: Yes. Go to Settings > Export > Choose CSV or JSON format.

Q: What happens when I downgrade from Pro to Free?
A: Your projects remain but you can only access the 3 most recent ones.
   Others are archived (not deleted) and restored if you upgrade again.

Q: Is there an API?
A: Yes, REST API available on Pro and Enterprise plans. Docs at api.flowboard.io.""",

    """FlowBoard Team:
CEO: Sarah Chen (ex-Google PM)
CTO: Marcus Johnson (ex-Stripe engineer)
Head of AI: Dr. Priya Patel (PhD ML from Stanford)
Team size: 23 people (12 engineering, 4 product, 3 design, 4 ops)
Office: San Francisco, with remote engineers in 5 countries.
Hiring: Currently looking for senior backend engineers and a mobile lead.""",
]


# ============================================================
# STEP 2: Split Documents into Chunks
# ============================================================
# Why split? Because:
#   - LLMs have limited context windows
#   - Smaller chunks = more precise retrieval
#   - You only send the RELEVANT parts, not everything
#
# RecursiveCharacterTextSplitter tries to split on natural
# boundaries (paragraphs, sentences) before falling back to
# character count.

print("=" * 60)
print("PART 6: Retrieval-Augmented Generation (RAG)")
print("=" * 60)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,       # Max characters per chunk
    chunk_overlap=50,     # Overlap between chunks (preserves context at boundaries)
    separators=["\n\n", "\n", ". ", " "],  # Try these split points in order
)

# Convert our strings into Document objects and split them
docs = [Document(page_content=text) for text in DOCUMENTS]
chunks = text_splitter.split_documents(docs)

print(f"\nOriginal documents: {len(DOCUMENTS)}")
print(f"After splitting:    {len(chunks)} chunks")
print(f"\nExample chunk (first one):")
print(f"  '{chunks[0].page_content[:100]}...'")
print()


# ============================================================
# STEP 3: Create Embeddings and Vector Store
# ============================================================
# Embeddings convert text into numbers (vectors) that capture meaning.
# Similar texts have similar vectors. This lets us SEARCH by meaning,
# not just keywords.
#
# "What's the price?" and "How much does it cost?" have different words
# but similar embeddings — so both would find the pricing chunk.
#
# We use a local model (runs on your machine, no API needed for embeddings).
# FAISS is a fast, local vector store. No external database needed.

print("-" * 60)
print("Creating embeddings and vector store...")
print("(First run downloads a small model ~90MB — subsequent runs are instant)")
print("-" * 60)

from langchain_community.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2",  # Small, fast, runs locally
)

# This embeds all chunks and stores them in a searchable index
vector_store = FAISS.from_documents(chunks, embeddings)

print(f"Vector store created with {len(chunks)} vectors.")
print()


# ============================================================
# STEP 4: Retrieval — Find Relevant Chunks
# ============================================================
# Given a question, find the chunks most similar to it.
# This is the "R" in RAG.

print("-" * 60)
print("RETRIEVAL: Finding relevant chunks for a question")
print("-" * 60)

question = "What's the refund policy?"

# Search for the 2 most relevant chunks
retrieved_docs = vector_store.similarity_search(question, k=2)

print(f"\nQuestion: '{question}'")
print(f"Retrieved {len(retrieved_docs)} relevant chunks:\n")
for i, doc in enumerate(retrieved_docs):
    print(f"  Chunk {i+1}: '{doc.page_content[:120]}...'\n")


# ============================================================
# STEP 5: Generation — Answer Using Retrieved Context
# ============================================================
# Now we feed the retrieved chunks to the model as context.
# The model answers based on THIS context, not its training data.
# This is the "G" in RAG.

print("-" * 60)
print("GENERATION: Answering with retrieved context")
print("-" * 60)

model = ChatOpenAI(
    model=os.getenv("LLM_MODEL", "deepseek-chat"),
    temperature=0.3,  # Low temp for factual answers
    base_url=os.getenv("OPENAI_BASE_URL"),
)


def ask_with_rag(question: str, k: int = 3) -> str:
    """
    The full RAG pipeline:
      1. Retrieve relevant chunks
      2. Build a prompt with the context
      3. Ask the model to answer based on that context
    """
    # Retrieve
    docs = vector_store.similarity_search(question, k=k)
    context = "\n\n".join([doc.page_content for doc in docs])
    
    # Generate
    messages = [
        SystemMessage(content=f"""Answer the question based ONLY on the following context.
If the answer isn't in the context, say "I don't have that information."
Be concise and specific.

Context:
{context}"""),
        HumanMessage(content=question),
    ]
    
    response = model.invoke(messages)
    return response.content


# Test with several questions
questions = [
    "What's the refund policy?",
    "What tech stack does FlowBoard use?",
    "Who is the CTO?",
    "What's the #1 priority on the roadmap?",
    "What happens if I downgrade to the free plan?",
    "What's the meaning of life?",  # Not in our docs!
]

print()
for q in questions:
    answer = ask_with_rag(q)
    print(f"Q: {q}")
    print(f"A: {answer}\n")


# ============================================================
# STEP 6: Compare — With RAG vs Without RAG
# ============================================================
# Let's show the difference: same question, with and without context.

print("=" * 60)
print("COMPARISON: With RAG vs Without RAG")
print("=" * 60)

comparison_q = "What's FlowBoard's pricing?"

# Without RAG — model has no context about FlowBoard
no_rag_messages = [
    SystemMessage(content="Answer concisely. If you don't know, say so."),
    HumanMessage(content=comparison_q),
]
no_rag_answer = model.invoke(no_rag_messages).content

# With RAG — model gets relevant context
rag_answer = ask_with_rag(comparison_q)

print(f"\nQuestion: {comparison_q}\n")
print(f"WITHOUT RAG: {no_rag_answer}")
print(f"\nWITH RAG:    {rag_answer}")

print()
print("-" * 60)
print("KEY INSIGHTS:")
print("  1. RAG = Retrieve relevant context + Generate answer from it")
print("  2. Documents are split into chunks for precise retrieval")
print("  3. Embeddings convert text to vectors for semantic search")
print("  4. The model answers from YOUR data, not its training data")
print("  5. Without RAG, the model guesses. With RAG, it's grounded in facts.")
print("  6. The system prompt tells the model to ONLY use the provided context")
