from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import CSVLoader
from langchain_community.document_loaders import UnstructuredExcelLoader
from langchain_community.document_loaders import WebBaseLoader


def load_documents(file_type, file_path_or_url):
    if file_type.upper() == "PDF":
        loader = PyPDFLoader(file_path_or_url)
    elif file_type.upper() == "CSV":
        loader = CSVLoader(file_path=file_path_or_url)
    elif file_type.upper() == "EXCEL":
        loader = UnstructuredExcelLoader(file_path_or_url)
    elif file_type.upper() == "TEXT":
        loader = TextLoader(file_path_or_url)
    elif file_type.upper() == "LINK":
        loader = WebBaseLoader(file_path_or_url)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")
    
    return loader.load()
