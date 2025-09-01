from app.chat.create_embeddings import get_vectorstore_for_pdf
import logging

logger = logging.getLogger(__name__)

def build_retriever(chat_args):
    user_id = chat_args.metadata.user_id
    pdf_id = chat_args.pdf_id
    
    print(f"🔍 Building retriever for PDF: {pdf_id}, User: {user_id}")
    
    # Get your existing ChromaDB vectorstore
    vectorstore = get_vectorstore_for_pdf(pdf_id, user_id)
    
    # Check collection size
    try:
        collection_count = vectorstore._collection.count()
        print(f"📊 Collection has {collection_count} documents")
        
        # Let's also test a sample query to see what's in the collection
        sample_docs = vectorstore.similarity_search("", k=5)  # Empty query to get any docs
        print(f"� Sample documents in collection:")
        for i, doc in enumerate(sample_docs[:3]):  # Show first 3
            print(f"  Sample {i+1}: {doc.page_content[:150]}...")
            
    except Exception as e:
        print(f"⚠️ Could not get collection info: {e}")
    
    # Return standard retriever but we'll add debugging in the chain
    return vectorstore.as_retriever(search_kwargs={"k": 4})
