from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from app.chat.models import ChatArgs
from app.chat.vector_stores.chromadb import build_retriever
from app.chat.llms.chatopenai import build_llm
from app.chat.memories.sql_memory import build_memory


def build_chat(chat_args: ChatArgs):
    """
    Build a ConversationalRetrievalChain with ChromaDB retriever and SQL memory
    
    :param chat_args: ChatArgs object containing
        conversation_id, pdf_id, metadata, and streaming flag.
    :return: ConversationalRetrievalChain instance
    
    Example Usage:
        chain = build_chat(chat_args)
        response = chain({"question": "What is this document about?"})
    """
    
    retriever = build_retriever(chat_args)
    llm = build_llm(chat_args)
    memory = build_memory(chat_args)

    # Custom prompt template to ensure accuracy
    qa_prompt_template = """Use the following pieces of context to answer the question at the end. 
If you don't know the answer from the provided context, just say that you don't know, don't try to make up an answer.
Be very careful about geographical and factual information - only use information that is explicitly stated in the context.

Context:
{context}

Chat History:
{chat_history}

Question: {question}
Helpful Answer:"""

    qa_prompt = PromptTemplate(
        template=qa_prompt_template,
        input_variables=["context", "chat_history", "question"]
    )

    # Create and return the chain with verbose output
    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        memory=memory,
        retriever=retriever,
        combine_docs_chain_kwargs={"prompt": qa_prompt},
        verbose=True,  # This will show us what's happening
        return_source_documents=True  # This will help us see what documents are retrieved
    )
