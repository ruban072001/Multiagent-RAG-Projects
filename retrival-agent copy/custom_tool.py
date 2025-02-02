from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field, ConfigDict
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import (TextLoader, PDFPlumberLoader, UnstructuredCSVLoader,
                                                  Docx2txtLoader)
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
load_dotenv()
import os
hug_model = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-mpnet-base-v2")

current = os.path.dirname(__file__)

class documentsearchtoolinput(BaseModel): 
    questions: str = Field(..., description="Mandatory query you want to use to search the PDF's content")

class documentsearchtool(BaseTool):
    name: str = "documentsearchtool"
    description: str = "A tool that can be used to semantic search a query from a PDF's content"
    args_schema: Type[BaseModel] = documentsearchtoolinput
    model_config = ConfigDict(extra="allow")

    def __init__(self, extension, file_path, db_path, method):
        super().__init__()
        self.file_path = file_path
        self.db_path = db_path
        
        if method == "store":
            if extension == "pdf":
                self.pdf_splitter()
            if extension == "txt":
                self.txt_splitter()
            if extension == "csv":
                self.csv_splitter()
            if extension == "docx":
                self.word_splitter()
    
    def word_splitter(self):
        if os.path.exists(self.db_path):
            print("db already exist and adding new values...")
            existing_db = FAISS.load_local(self.db_path, embeddings=hug_model, allow_dangerous_deserialization = True)
            loader = Docx2txtLoader(self.file_path)
            load = loader.load()
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            documents = splitter.split_documents(load)
            existing_db.add_documents(documents, embedding=hug_model)
            existing_db.save_local(self.db_path)
            print("new data added successfully...")
        if not os.path.exists(self.db_path):
            print("creating new db...")
            os.makedirs(self.db_path)
            loader = Docx2txtLoader(self.file_path)
            load = loader.load()
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            documents = splitter.split_documents(load)
            new_db = FAISS.from_documents(documents, embedding=hug_model)
            new_db.save_local(self.db_path)
            print("new db created...")

    def csv_splitter(self):
        if os.path.exists(self.db_path):
            print("db already exist and adding new values...")
            existing_db = FAISS.load_local(self.db_path, embeddings=hug_model, allow_dangerous_deserialization = True)
            loader = UnstructuredCSVLoader(self.file_path)
            load = loader.load()
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            documents = splitter.split_documents(load)
            existing_db.add_documents(documents, embedding=hug_model)
            existing_db.save_local(self.db_path)
            print("new data added successfully...")
        if not os.path.exists(self.db_path):
            print("creating new db...")
            os.makedirs(self.db_path)
            loader = UnstructuredCSVLoader(self.file_path)
            load = loader.load()
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            documents = splitter.split_documents(load)
            new_db = FAISS.from_documents(documents, embedding=hug_model)
            new_db.save_local(self.db_path)
            print("new db created...")         
     
    def txt_splitter(self):
        if os.path.exists(self.db_path):
            print("db already exist and adding new values...")
            existing_db = FAISS.load_local(self.db_path, embeddings=hug_model, allow_dangerous_deserialization = True)
            loader = TextLoader(self.file_path, encoding="utf-8")
            load = loader.load()
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            documents = splitter.split_documents(load)
            existing_db.add_documents(documents, embedding=hug_model)
            existing_db.save_local(self.db_path)
            print("new data added successfully...")
        if not os.path.exists(self.db_path):
            print("creating new db...")
            os.makedirs(self.db_path)
            loader = TextLoader(self.file_path, encoding="utf-8")
            load = loader.load()
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            documents = splitter.split_documents(load)
            new_db = FAISS.from_documents(documents, embedding=hug_model)
            new_db.save_local(self.db_path)
            print("new db created...") 
        
    def pdf_splitter(self):
        if os.path.exists(self.db_path):
            print("db already exist and adding new values...")
            existing_db = FAISS.load_local(self.db_path, embeddings=hug_model, allow_dangerous_deserialization = True)
            loader = PDFPlumberLoader(self.file_path)
            load = loader.load()
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            documents = splitter.split_documents(load)
            existing_db.add_documents(documents, embedding=hug_model)
            existing_db.save_local(self.db_path)
            print("new data added successfully...")
        if not os.path.exists(self.db_path):
            print("creating new db...")
            os.makedirs(self.db_path)
            loader = PDFPlumberLoader(self.file_path)
            load = loader.load()
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            documents = splitter.split_documents(load)
            new_db = FAISS.from_documents(documents, embedding=hug_model)
            new_db.save_local(self.db_path)
            print("new db created...")

    def _run(self, questions: str):
        if os.path.exists(self.db_path):
            print("retriving from database...")
            existing_db = FAISS.load_local(self.db_path, embeddings=hug_model, allow_dangerous_deserialization = True)
            retriever = existing_db.as_retriever(search_type="mmr",
        search_kwargs={'lambda_mult': 1.0})
            return retriever.invoke(questions)
        
    
 
if __name__ == "__main__":
    
    tool = documentsearchtool(
        extension='txt',
        file_path=r"C:\Users\KIRUBA\Desktop\The Free Electron and State Density.txt",
        db_path=os.path.join(current, "VECTOR DB", 'ruban', 'mission-1'),
        method = "store"

    )
    questions = "what is free electron and state density?"
    result = tool._run(questions=questions)
    print(result)