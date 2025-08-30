from llama_index.core import SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex
from llama_index.llms.ollama import Ollama

loader = SimpleDirectoryReader(
    input_dir="/Users/muneer78/reading",
    recursive=True,
    required_exts=[".epub"],
)

documents = loader.load_data()

embedding_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

index = VectorStoreIndex.from_documents(
    documents,
    embed_model=embedding_model,
)

llama = Ollama(
    model="llama2",
    request_timeout=40.0,
)

query_engine = index.as_query_engine(llm=llama)

print(
    query_engine.query(
        "What are the titles of all the books available? Show me the context used to derive your answer."
    )
)
