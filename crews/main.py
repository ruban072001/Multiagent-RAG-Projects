import streamlit as st
import os
import time
from dotenv import load_dotenv
from custom_tool import documentsearchtool
from crew import AgenticCrew

# Load environment variables
load_dotenv()

# Streamlit UI
st.title("Multi-Agent RAG System")

# Get Current Directory
CURRENT_DIRECTORY = os.path.dirname(__file__)

def is_greeting(message):
    greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening", "greetings"]
    return any(message.lower() in greet for greet in greetings)

# Define File Paths
ALL_FILE_PATH = os.path.join(CURRENT_DIRECTORY, 'Files')
DB_DIRECTORY = os.path.join(CURRENT_DIRECTORY, "DATABASES")

# Ensure directories exist
os.makedirs(ALL_FILE_PATH, exist_ok=True)

FILE_TYPES = {
    "pdf": "PDF",
    "csv": "CSV",
    "txt": "TXT",
    "docx": "DOC",
    "pptx":"PPT"
}

# Create file-specific directories
FILE_PATHS = {ext: os.path.join(ALL_FILE_PATH, folder) for ext, folder in FILE_TYPES.items()}
for path in FILE_PATHS.values():
    os.makedirs(path, exist_ok=True)

# Count existing files
FILE_COUNTS = {ext: len(os.listdir(path)) for ext, path in FILE_PATHS.items()}

# Session State Initialization
if "crew" not in st.session_state:
    st.session_state.crew = None

if "document_tool" not in st.session_state:
    st.session_state.document_tool = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar Inputs
with st.sidebar:
    Search_type = st.selectbox("Select Search Type", ["Document Search", "Google Search"])
    DB_NAME = st.text_input("Enter DB name")
    COLLECTION_NAME = st.text_input("Enter collection name")
    METHOD = st.selectbox("Select an Option", ["store", "retrieve"])

    DB_PATH = os.path.join(DB_DIRECTORY, DB_NAME, COLLECTION_NAME)

    files = st.file_uploader(
        "Select your file(s)", accept_multiple_files=True, type=list(FILE_TYPES.keys())
    )

    if st.button("Process Files") and files:
        
        for idx, file in enumerate(files):
            with st.spinner(f"Processing files...{idx + 1}/{len(files)}"):
                file_ext = file.name.split(".")[-1].lower()
                
                if file_ext in FILE_TYPES:
                    file_count = FILE_COUNTS[file_ext] + 1
                    new_filename = f"{file_ext}_{file_count}.{file_ext}"
                    file_path = os.path.join(FILE_PATHS[file_ext], new_filename)

                    with open(file_path, 'wb') as f:
                        f.write(file.getvalue())

                    FILE_COUNTS[file_ext] += 1  # Update count

                    # Process File with documentsearchtool
                    st.session_state.document_tool = documentsearchtool(
                        extension=file_ext, file_path=file_path, db_path=DB_PATH, method=METHOD
                    )
                else:
                    st.warning(f"Invalid file type: {file.name}. Supported types: {', '.join(FILE_TYPES.keys())}")

        st.success("All files processed successfully!")

# Retrieval Mode
if METHOD == "retrieve" and Search_type == "Document Search":
    if os.path.exists(DB_PATH):
        try:
            st.session_state.document_tool = documentsearchtool(
                extension=None, file_path=None, db_path=DB_PATH, method=METHOD
            )
            st.sidebar.success(f"Connected to Database: {DB_NAME}/{COLLECTION_NAME}")
        except Exception as e:
            st.sidebar.error(f"Error loading document tool: {str(e)}")
    else:
        st.sidebar.warning(f"Database path not found: {DB_PATH}. Please store files first.")

# Display Chat History
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

# User Input for Chat
prompt = st.chat_input("Ask your question...")
if prompt:
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Check for greeting
    if is_greeting(prompt):
        result = "Hi there! How can I assist you today?"
        with st.chat_message("assistant"):
            st.markdown(result)
        st.session_state.chat_history.append({"role": "assistant", "content": result})

    else:
        # Initialize crew if not done
        if st.session_state.crew:
            print("crew already there")
            if Search_type == "Document Search":
                print("using document")
                st.session_state.crew = AgenticCrew(st.session_state.document_tool, True)
            else:
                print("using google")
                st.session_state.crew = AgenticCrew(None, False)

        else:
            print("crew is not there")
            if Search_type == "Document Search":
                print("document tool")
                st.session_state.crew = AgenticCrew(st.session_state.document_tool, True)
            else:
                print("google")
                st.session_state.crew = AgenticCrew(None, False)
                
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            with st.spinner("Thinking..."):
                inputs = {"questions": prompt}
                result = st.session_state.crew.crew().kickoff(inputs=inputs)
                if not result or not result.raw:
                        st.error("❗️ Empty response received. Please try again or check your inputs.")
                        st.session_state.chat_history.append({"role": "assistant", "content": "Sorry, I couldn't find an answer. Please rephrase your question."})
                else:
                    # Streaming Effect
                    full_response = ""
                    for i, line in enumerate(result.raw.split("\n")):
                        full_response += line + ("\n" if i < len(result.raw.split("\n")) - 1 else "")
                        message_placeholder.markdown(full_response + "▌")
                        time.sleep(0.25)

                    message_placeholder.markdown(full_response)
                    st.session_state.chat_history.append({"role": "assistant", "content": result.raw})