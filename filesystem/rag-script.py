import os
import sys
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import LlamaCpp
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# --- STEP 1: Load and Index ---
target_dir = './scripts'
script_extensions = ["**/*.py", "**/*.pl", "**/*.r"]
documents = []

print(f"--- Indexing scripts in {target_dir} ---")

for ext in script_extensions:
    loader = DirectoryLoader(
        target_dir,
        glob=ext,
        loader_cls=TextLoader,
        recursive=True,
        show_progress=True
    )
    documents.extend(loader.load())

if not documents:
    print("No scripts found. Please check your path.")
    sys.exit()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = text_splitter.split_documents(documents)

# --- STEP 2: Setup Vector DB & LLM ---
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_store = Chroma.from_documents(chunks, embedding_model)

llm = LlamaCpp(
    model_path="./models/llama-2-7b-chat.Q4_K_M.gguf",
    n_ctx=2048,
    temperature=0.1,
    verbose=False
)

# --- STEP 3: Custom Prompt to Force Source Names ---
# This tells the AI exactly how to format the answer
template = """Use the following pieces of context to answer the user's question. 
If you find a relevant script, you MUST mention its filename/path found in the context.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}

Question: {question}

Helpful Answer (Include script names here):"""

QA_CHAIN_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template=template,
)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
    chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
)

# --- STEP 4: Terminal Interaction Loop ---
print("\n--- RAG System Ready (Source Aware) ---")
print("Type 'exit' to stop.\n")

while True:
    user_query = input("Query: ")

    if user_query.lower() in ['exit', 'quit']:
        break

    if not user_query.strip():
        continue

    # We also manually fetch the source documents to verify them if the LLM misses one
    print("\nSearching...")
    response = qa_chain({"query": user_query})

    print("-" * 30)
    print(f"AI Response: {response['result']}")
    print("-" * 30 + "\n")