from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from app.chat.models import ChatArgs
from app.chat.vector_stores.chromadb import build_retriever
from app.chat.llms.chatopenai import build_llm
from app.chat.memories.sql_memory import build_memory


def build_chat(chat_args: ChatArgs):
    """
    Build a conversational retrieval chain using LCEL with ChromaDB retriever and SQL memory
    
    :param chat_args: ChatArgs object containing
        conversation_id, pdf_id, metadata, and streaming flag.
    :return: LCEL chain instance
    
    Example Usage:
        chain = build_chat(chat_args)
        response = chain.invoke({"input": "What is this document about?", "chat_history": []})
    """
    
    retriever = build_retriever(chat_args)
    llm = build_llm(chat_args)
    memory = build_memory(chat_args)

    # Create a history-aware retriever that reformulates questions based on chat history
    condense_question_system_template = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history. Do NOT answer the question, "
        "just reformulate it if needed and otherwise return it as is."
    )

    condense_question_prompt = ChatPromptTemplate.from_messages([
        ("system", condense_question_system_template),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
    ])

    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, condense_question_prompt
    )

    # Create the main QA prompt template
    system_prompt = (
        "You are a document analysis assistant that answers questions using ONLY the provided context. "
        "Use the retrieved document content to provide accurate, complete responses without adding external knowledge. "
        "\n\n"
        "Answer Format:\n"
        "- Provide direct answers based strictly on the context\n"
        "- Quote exact text for key claims: 'Document states: [exact quote]'\n"
        "- Reference document sections/pages when available\n"
        "- For lists: provide all items found in context, note if potentially incomplete\n"
        "\n\n"
        "If information is incomplete or missing:\n"
        "- State what information was found in the context\n"
        "- Clearly indicate what specific details are missing\n"
        "- Say 'Information not present in retrieved sections' when applicable\n"
        "\n\n"
        "Never add information from general knowledge. If context is ambiguous, "
        "quote the relevant text and explain the ambiguity rather than interpreting. "
        "\n\n"
        "Context:\n{context}"
    )

    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
    ])

    # Create the document processing chain
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

    # Create the final retrieval chain
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
    
    return rag_chain
