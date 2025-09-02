import os
import json
import time
from typing import Optional
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import logging

# Load environment variables
load_dotenv()

# Set up logging
logger = logging.getLogger(__name__)


def _get_pdf_mappings_file(chroma_db_path: str) -> str:
    """Get the path to the PDF mappings file for a user's ChromaDB directory"""
    return os.path.join(chroma_db_path, "pdf_mappings.json")


def _load_pdf_mappings(chroma_db_path: str) -> dict:
    """Load PDF ID to collection UUID mappings from file"""
    mappings_file = _get_pdf_mappings_file(chroma_db_path)
    if os.path.exists(mappings_file):
        try:
            with open(mappings_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Could not load PDF mappings file: {e}")
    return {}


def _save_pdf_mappings(chroma_db_path: str, mappings: dict):
    """Save PDF ID to collection UUID mappings to file"""
    mappings_file = _get_pdf_mappings_file(chroma_db_path)
    try:
        with open(mappings_file, 'w') as f:
            json.dump(mappings, f, indent=2)
        logger.info(f"Saved PDF mappings to {mappings_file}")
    except IOError as e:
        logger.error(f"Could not save PDF mappings file: {e}")


def _add_pdf_mapping(chroma_db_path: str, pdf_id: str, collection_uuid):
    """Add a PDF ID to collection UUID mapping"""
    mappings = _load_pdf_mappings(chroma_db_path)
    mappings[pdf_id] = {
        "collection_uuid": str(collection_uuid),  # Convert UUID to string
        "collection_name": f"pdf_{pdf_id.replace('-', '_')}",
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    _save_pdf_mappings(chroma_db_path, mappings)


def _remove_pdf_mapping(chroma_db_path: str, pdf_id: str):
    """Remove a PDF ID to collection UUID mapping"""
    mappings = _load_pdf_mappings(chroma_db_path)
    if pdf_id in mappings:
        del mappings[pdf_id]
        _save_pdf_mappings(chroma_db_path, mappings)
        logger.info(f"Removed PDF mapping for {pdf_id}")
    else:
        logger.warning(f"No mapping found for PDF {pdf_id}")


def create_embeddings_for_pdf(pdf_id: str, pdf_path: str, user_id: Optional[str] = None):
    """
    Generate and store embeddings for the given pdf

    1. Extract text from the specified PDF.
    2. Divide the extracted text into manageable chunks.
    3. Generate an embedding for each chunk.
    4. Persist the generated embeddings.

    :param pdf_id: The unique identifier for the PDF.
    :param pdf_path: The file path to the PDF.
    :param user_id: The unique identifier for the user (for isolation).

    Example Usage:

    create_embeddings_for_pdf('123456', '/path/to/pdf', 'user_789')
    """
    
    print(f"=== STARTING EMBEDDING CREATION FOR PDF {pdf_id} ===")
    
    try:
        # Validate file exists and is readable
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found at path: {pdf_path}")
        
        if not os.path.isfile(pdf_path):
            raise ValueError(f"Path is not a file: {pdf_path}")
        
        file_size = os.path.getsize(pdf_path)
        if file_size == 0:
            raise ValueError(f"PDF file is empty: {pdf_path}")
        
        print(f"File validation passed. Size: {file_size} bytes")
        logger.info(f"Processing PDF {pdf_id} at path {pdf_path} (size: {file_size} bytes)")
        
        # 1. Extract text from PDF using PyPDFLoader
        try:
            loader = PyPDFLoader(pdf_path)
            documents = loader.load()
            
            if not documents:
                raise ValueError(f"No content could be extracted from PDF {pdf_id}")
            
            print(f"Successfully loaded {len(documents)} pages from PDF")
            logger.info(f"Successfully loaded {len(documents)} pages from PDF {pdf_id}")
            
        except Exception as e:
            print(f"Failed to load PDF: {str(e)}")
            logger.error(f"Failed to load PDF {pdf_id}: {str(e)}")
            raise ValueError(f"Could not process PDF file {pdf_id}. The file may be corrupted, password-protected, or in an unsupported format.") from e
        
        # 2. Divide the text into manageable chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        # Split the documents into chunks
        chunks = text_splitter.split_documents(documents)
        
        if not chunks:
            raise ValueError(f"No text chunks could be created from PDF {pdf_id}")
        
        # Add comprehensive metadata to each chunk
        print(f"Adding metadata to chunks...")
        for i, chunk in enumerate(chunks):
            # Add PDF ID
            chunk.metadata['pdf_id'] = str(pdf_id)
            
            # Add page number from original document metadata
            if 'page' in chunk.metadata:
                chunk.metadata['page'] = chunk.metadata['page']
            else:
                # If page metadata is not available, try to get it from source
                chunk.metadata['page'] = chunk.metadata.get('source', 'unknown')
            
            # Add text content for reference
            chunk.metadata['content'] = chunk.page_content
            
            # Add chunk index for ordering
            chunk.metadata['chunk_index'] = i
            
            # Add total chunks for context
            chunk.metadata['total_chunks'] = len(chunks)
        
        # 3. Generate embeddings using OpenAI
        print(f"Initializing OpenAI embeddings...")
        embeddings = OpenAIEmbeddings()
        
        # 4. Store embeddings in ChromaDB
        print(f"Setting up ChromaDB vector store...")
        
        # Get project root directory (langchain-pdf folder)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        chroma_db_relative_path = os.environ.get("CHROMA_DB_PATH", "chroma_db")
        
        # Implement database-level isolation: each user gets their own database directory
        if user_id:
            chroma_db_path = os.path.join(project_root, chroma_db_relative_path, f"user_{user_id}")
        else:
            # Fallback for backward compatibility - use default directory
            chroma_db_path = os.path.join(project_root, chroma_db_relative_path, "default")
        
        # Create ChromaDB directory if it doesn't exist
        os.makedirs(chroma_db_path, exist_ok=True)
        print(f"ChromaDB path: {chroma_db_path}")
        
        # Simple collection name based on PDF ID (no user prefix needed with database isolation)
        # ChromaDB doesn't allow hyphens, so replace them with underscores
        collection_name = f"pdf_{pdf_id.replace('-', '_')}"
        
        # Check if collection already exists
        try:
            # Try to load existing collection
            existing_vectorstore = Chroma(
                persist_directory=chroma_db_path,
                embedding_function=embeddings,
                collection_name=collection_name
            )
            
            # Check if the collection has any documents
            existing_docs = existing_vectorstore._collection.count()
            
            if existing_docs > 0:
                print(f"Collection '{collection_name}' already exists with {existing_docs} documents. Skipping embedding creation.")
                logger.info(f"PDF {pdf_id} already has embeddings stored. Skipping processing.")
                
                # Still save the mapping for existing collections if not already saved
                collection_uuid = existing_vectorstore._collection.id
                mappings = _load_pdf_mappings(chroma_db_path)
                if pdf_id not in mappings:
                    _add_pdf_mapping(chroma_db_path, pdf_id, collection_uuid)
                    print(f"📄 Collection UUID: {collection_uuid}")
                    print(f"📁 Mapping saved to: {_get_pdf_mappings_file(chroma_db_path)}")
                
                return
            else:
                print(f"Collection '{collection_name}' exists but is empty. Adding embeddings.")
                vectorstore = existing_vectorstore
                
        except Exception as e:
            # Collection doesn't exist, create a new one
            print(f"Creating new ChromaDB collection: {collection_name}")
            vectorstore = None
        
        # Create or add to ChromaDB vector store
        if vectorstore is None:
            # Create new collection
            vectorstore = Chroma.from_documents(
                documents=chunks,
                embedding=embeddings,
                persist_directory=chroma_db_path,
                collection_name=collection_name
            )
        else:
            # Add to existing collection
            vectorstore.add_documents(chunks)
        
        # Get the collection UUID and save mapping
        collection_uuid = vectorstore._collection.id
        _add_pdf_mapping(chroma_db_path, pdf_id, collection_uuid)
        
        logger.info(f"Successfully created chunks for PDF {pdf_id} with {len(chunks)} chunks")
        
    except Exception as e:
        logger.error(f"Error processing PDF {pdf_id}: {str(e)}")
        print(f"=== ERROR processing PDF {pdf_id}: {str(e)} ===")
        raise


def get_vectorstore_for_pdf(pdf_id: str, user_id: Optional[str] = None):
    """
    Get the ChromaDB vectorstore for a specific PDF
    
    :param pdf_id: The unique identifier for the PDF
    :param user_id: The unique identifier for the user (for isolation)
    :return: ChromaDB vectorstore instance
    """
    try:
        # Initialize embeddings
        embeddings = OpenAIEmbeddings()
        
        # Get project root directory (langchain-pdf folder)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        chroma_db_relative_path = os.environ.get("CHROMA_DB_PATH", "chroma_db")
        
        # Implement database-level isolation: each user gets their own database directory
        if user_id:
            chroma_db_path = os.path.join(project_root, chroma_db_relative_path, f"user_{user_id}")
        else:
            # Fallback for backward compatibility - use default directory
            chroma_db_path = os.path.join(project_root, chroma_db_relative_path, "default")
        
        # Simple collection name based on PDF ID (no user prefix needed with database isolation)
        collection_name = f"pdf_{pdf_id.replace('-', '_')}"
        
        # Load existing ChromaDB vector store
        vectorstore = Chroma(
            persist_directory=chroma_db_path,
            embedding_function=embeddings,
            collection_name=collection_name
        )
        
        return vectorstore
        
    except Exception as e:
        logger.error(f"Error loading vectorstore for PDF {pdf_id}: {str(e)}")
        raise


def check_embeddings_exist(pdf_id: str, user_id: Optional[str] = None) -> bool:
    """
    Check if embeddings already exist for a specific PDF
    
    :param pdf_id: The unique identifier for the PDF
    :param user_id: The unique identifier for the user (for isolation)
    :return: True if embeddings exist, False otherwise
    """
    try:
        # Get project root directory (langchain-pdf folder)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        chroma_db_relative_path = os.environ.get("CHROMA_DB_PATH", "chroma_db")
        
        # Implement database-level isolation: each user gets their own database directory
        if user_id:
            chroma_db_path = os.path.join(project_root, chroma_db_relative_path, f"user_{user_id}")
        else:
            # Fallback for backward compatibility - use default directory
            chroma_db_path = os.path.join(project_root, chroma_db_relative_path, "default")
        
        # Check if ChromaDB directory exists
        if not os.path.exists(chroma_db_path):
            return False
        
        # Simple collection name based on PDF ID (no user prefix needed with database isolation)
        collection_name = f"pdf_{pdf_id.replace('-', '_')}"
        
        try:
            # Initialize embeddings (needed for Chroma)
            embeddings = OpenAIEmbeddings()
            
            # Try to load existing collection
            vectorstore = Chroma(
                persist_directory=chroma_db_path,
                embedding_function=embeddings,
                collection_name=collection_name
            )
            
            # Check if the collection has any documents
            doc_count = vectorstore._collection.count()
            return doc_count > 0
            
        except Exception as e:
            # Collection doesn't exist or can't be loaded
            return False
        
    except Exception as e:
        logger.error(f"Error checking embeddings for PDF {pdf_id}: {str(e)}")
        return False


def get_pdf_mappings(user_id: Optional[str] = None) -> dict:
    """
    Get PDF ID to collection UUID mappings for a user
    
    :param user_id: The unique identifier for the user
    :return: Dictionary of PDF mappings
    """
    try:
        # Get project root directory (langchain-pdf folder)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        chroma_db_relative_path = os.environ.get("CHROMA_DB_PATH", "chroma_db")
        
        # Implement database-level isolation: each user gets their own database directory
        if user_id:
            chroma_db_path = os.path.join(project_root, chroma_db_relative_path, f"user_{user_id}")
        else:
            # Fallback for backward compatibility - use default directory
            chroma_db_path = os.path.join(project_root, chroma_db_relative_path, "default")
        
        return _load_pdf_mappings(chroma_db_path)
        
    except Exception as e:
        logger.error(f"Error loading PDF mappings for user {user_id}: {str(e)}")
        return {}


def list_user_pdfs(user_id: str) -> None:
    """
    List all PDFs and their collection information for a user
    
    :param user_id: The unique identifier for the user
    """
    mappings = get_pdf_mappings(user_id)
    
    if not mappings:
        print(f"No PDF mappings found for user {user_id}")
        return


def delete_embeddings_for_pdf(pdf_id: str, user_id: Optional[str] = None):
    """
    Delete all embeddings and collection for a specific PDF
    
    :param pdf_id: The unique identifier for the PDF
    :param user_id: The unique identifier for the user (for isolation)
    """
    try:
        print(f"=== STARTING EMBEDDING DELETION FOR PDF {pdf_id} ===")
        
        # Get project root directory (langchain-pdf folder)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        chroma_db_relative_path = os.environ.get("CHROMA_DB_PATH", "chroma_db")
        
        # Implement database-level isolation: each user gets their own database directory
        if user_id:
            chroma_db_path = os.path.join(project_root, chroma_db_relative_path, f"user_{user_id}")
        else:
            # Fallback for backward compatibility - use default directory
            chroma_db_path = os.path.join(project_root, chroma_db_relative_path, "default")
        
        # Check if ChromaDB directory exists
        if not os.path.exists(chroma_db_path):
            print(f"ChromaDB directory does not exist: {chroma_db_path}")
            return
        
        # Simple collection name based on PDF ID (no user prefix needed with database isolation)
        collection_name = f"pdf_{pdf_id.replace('-', '_')}"
        
        try:
            # Initialize embeddings (needed for Chroma)
            embeddings = OpenAIEmbeddings()
            
            # Try to load existing collection
            vectorstore = Chroma(
                persist_directory=chroma_db_path,
                embedding_function=embeddings,
                collection_name=collection_name
            )
            
            # Check if the collection has any documents
            doc_count = vectorstore._collection.count()
            
            if doc_count > 0:
                print(f"Found collection '{collection_name}' with {doc_count} documents")
                
                # Delete the collection
                vectorstore.delete_collection()
                print(f"Successfully deleted collection '{collection_name}'")
                logger.info(f"Deleted ChromaDB collection for PDF {pdf_id}")
            else:
                print(f"Collection '{collection_name}' exists but is empty")
                # Still delete the empty collection
                vectorstore.delete_collection()
                print(f"Deleted empty collection '{collection_name}'")
                
        except Exception as e:
            # Collection doesn't exist or can't be loaded
            print(f"Collection '{collection_name}' does not exist or could not be loaded: {str(e)}")
            logger.warning(f"ChromaDB collection for PDF {pdf_id} not found: {str(e)}")
        
        # Remove PDF mapping
        _remove_pdf_mapping(chroma_db_path, pdf_id)
        
        print(f"=== SUCCESS: Embeddings deleted for PDF {pdf_id} ===")
        
    except Exception as e:
        logger.error(f"Error deleting embeddings for PDF {pdf_id}: {str(e)}")
        print(f"=== ERROR deleting embeddings for PDF {pdf_id}: {str(e)} ===")
        raise
