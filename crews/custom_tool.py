from crewai.tools import BaseTool
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field, ConfigDict
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from langchain_community.document_loaders import (TextLoader, PDFPlumberLoader, UnstructuredCSVLoader,
                                                  Docx2txtLoader, UnstructuredPowerPointLoader)
from langchain_text_splitters import RecursiveCharacterTextSplitter
load_dotenv()

hug_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key="AIzaSyDJTeB65kMPULSarqFIkiFzNRSBjiyYjL8")

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
        self.extension = extension
        if method == "store":
            self.process_document()
        
    def process_document(self):
        """Loads, splits, and stores document content in FAISS."""
        loaders = {
            "pdf": PDFPlumberLoader,
            "txt": TextLoader,
            "csv": UnstructuredCSVLoader,
            "docx": Docx2txtLoader,
            "pptx":UnstructuredPowerPointLoader,
        }

        if self.extension not in loaders:
            raise ValueError(f"Unsupported file type: {self.extension}")

        loader = loaders[self.extension](self.file_path)
        load = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        documents = splitter.split_documents(load)
        print(documents)
        self.save_to_db(documents)
        
    def save_to_db(self, documents):
        """Saves or updates FAISS DB."""
        new_vec_store = FAISS.from_documents(documents, embedding=hug_model)

        if os.path.exists(self.db_path):
            existing_db = FAISS.load_local(self.db_path, hug_model, allow_dangerous_deserialization=True)
            existing_db.merge_from(new_vec_store)
            existing_db.save_local(self.db_path)
            print("Merged new documents into the existing FAISS DB!")
        else:
            new_vec_store.save_local(self.db_path)
            print("Created a new FAISS DB!")
        
    def _run(self, questions: str):
        """Retrieves relevant content from FAISS DB."""
        if not os.path.exists(self.db_path):
            return "Database not found! Please store documents first."

        print("Retrieving from database...")
        existing_db = FAISS.load_local(self.db_path, hug_model, allow_dangerous_deserialization=True)
        retriever = existing_db.as_retriever(search_type="mmr", search_kwargs={'k': 20, 'lambda_mult': 1.0})
        return retriever.invoke(questions)
    
    
if __name__ == "__main__":
    tool = documentsearchtool(
        extension='pptx',
        file_path=r"C:\Users\Ruban\Documents\Resolute-AI\User Guide Manual v1.pptx",
        db_path=os.path.join(current, "VECTOR DB", 'ruban', 'mission-1'),
        method = "store"
    )
    question = "two roads diverged in wood"
    result = tool._run(question=question)
    print(result)
