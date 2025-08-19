import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"
PDF_PATH = r"C:\Users\SABARI\Documents\episode3_langchain_bot\episode3.pdf"
loader = PyPDFLoader(PDF_PATH)
documents = loader.load()
splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
texts = splitter.split_documents(documents)
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(texts, embedding=embedding)
qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(
        model="mistralai/mistral-7b-instruct",  
        temperature=0,
        max_tokens=500
    ),
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)
while True:
    query = input("\nAsk a question about the PDF (or type 'exit' to quit): ")
    if query.lower() == "exit":
        break
    result = qa.run(query)
    print("Answer:", result)
