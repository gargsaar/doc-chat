from app.chat.create_embeddings import get_vectorstore_for_pdf
import logging

logger = logging.getLogger(__name__)

def build_retriever(chat_args):
    user_id = chat_args.metadata.user_id
    pdf_id = chat_args.pdf_id
    
    print(f"🔍 Building retriever for PDF: {pdf_id}, User: {user_id}")
    
    # Get your existing ChromaDB vectorstore
    vectorstore = get_vectorstore_for_pdf(pdf_id, user_id)
    
    # Get retrieval configuration
    retrieval_config = chat_args.get_retrieval_config()
    print(f"⚙️ Using retrieval config: k={retrieval_config.k}, search_type={retrieval_config.search_type}")
    
    # Check collection size and adjust k if needed
    try:
        collection_count = vectorstore._collection.count()
        print(f"📊 Collection has {collection_count} documents")
        
        # Adjust k if collection is smaller than requested
        effective_k = retrieval_config.k
        if collection_count < retrieval_config.k:
            effective_k = max(1, collection_count - 1)
            print(f"⚙️ Adjusted k from {retrieval_config.k} to {effective_k} based on collection size")
        
        # Sample documents for debugging
        sample_docs = vectorstore.similarity_search("", k=min(5, collection_count))
        print(f"📋 Sample documents available")
        for i, doc in enumerate(sample_docs[:3]):
            print(f"  Sample {i+1}: {doc.page_content[:100]}...")
            
    except Exception as e:
        print(f"⚠️ Could not get collection info: {e}")
        effective_k = retrieval_config.k
    
    # Build search kwargs with the configured parameters
    search_kwargs = {"k": effective_k}
    
    # Return retriever with configured parameters
    return vectorstore.as_retriever(
        search_type=retrieval_config.search_type,
        search_kwargs=search_kwargs
    )
