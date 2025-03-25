from pathlib import Path
from langchain import hub
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_core.prompts import PromptTemplate
import re

# Function to load all text files in a folder
def load_text_files(folder_path):
    folder = Path(folder_path)
    data = []
    for file_path in folder.glob('*.txt'):
        loader = TextLoader(file_path)
        data.extend(loader.load())
    return data

# Load all text files in the folder
data = load_text_files("/Users/muneer78/Downloads/docs")

# Load titles from a file
with open(r"/Users/muneer78/Downloads/docs/file.txt", 'r', encoding='utf-8') as file:
    content = file.read()
lines = content.split('\n')
titles = []
for line in lines:
    match = re.search(r'"([^"]+)"', line)
    if match:
        titles.append(match.group(1))

model_name = "BAAI/bge-small-en"
model_kwargs = {"device": "cpu"}
encode_kwargs = {"normalize_embeddings": True}
hf = HuggingFaceBgeEmbeddings(model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs)

# Split
text_splitter = RecursiveCharacterTextSplitter(
    separators=[
        "\n\n",
        "\n",
        "\uff0e",  # Fullwidth full stop
        "\u3002",  # Ideographic full stop
    ],
    chunk_size=300, chunk_overlap=50, length_function=len, add_start_index=True)
all_splits = text_splitter.split_documents(data)

# Store splits
vectorstore = FAISS.from_documents(documents=all_splits, embedding=hf)

# RAG prompt
template = """Use the following context to search for answers to your questions.
    If you don't know the answer, just say you don't know, don't try to make up an answer.
    Don't add anything else.{context}
    Question: {question}
    Helpful Answer:"""
QA_CHAIN_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template=template,
)

# LLM
llm = Ollama(model="llama3.1")

# RetrievalQA
qa_chain = RetrievalQA.from_chain_type(
    llm,
    retriever=vectorstore.as_retriever(),
    chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
)

for title in titles:
    specific_question = f"Definition of {title}"
    result = qa_chain({"query": specific_question})
    print(f"Definition of {title}: {result['result']}")