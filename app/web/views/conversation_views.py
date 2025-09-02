from flask import Blueprint, g, request, Response, jsonify, stream_with_context
from app.web.hooks import login_required, load_model
from app.web.db.models import Pdf, Conversation
from app.chat.chat import build_chat
from app.chat.models import ChatArgs

bp = Blueprint("conversation", __name__, url_prefix="/api/conversations")


@bp.route("/", methods=["GET"])
@login_required
@load_model(Pdf, lambda r: r.args.get("pdf_id"))
def list_conversations(pdf):
    return [c.as_dict() for c in pdf.conversations]


@bp.route("/", methods=["POST"])
@login_required
@load_model(Pdf, lambda r: r.args.get("pdf_id"))
def create_conversation(pdf):
    conversation = Conversation.create(user_id=g.user.id, pdf_id=pdf.id)

    return conversation.as_dict()


@bp.route("/<string:conversation_id>/messages", methods=["POST"])
@login_required
@load_model(Conversation)
def create_message(conversation):
    user_input = request.json.get("input") if request.json else None
    if not user_input:
        return jsonify({"error": "No input provided"}), 400
        
    streaming = request.args.get("stream", "false").lower() == "true"

    pdf = conversation.pdf

    from app.chat.models import Metadata
    
    chat_args = ChatArgs(
        conversation_id=conversation.id,
        pdf_id=pdf.id,
        streaming=streaming,
        metadata=Metadata(
            conversation_id=conversation.id,
            user_id=g.user.id,
            pdf_id=pdf.id,
        ),
    )

    chat = build_chat(chat_args)

    if not chat:
        return "Chat not yet implemented!"

    # Get chat history for the LCEL chain
    from app.chat.memories.sql_memory import get_chat_history
    chat_history = get_chat_history(conversation.id)

    if streaming:
        # For streaming, we need to implement this differently with LCEL
        def generate():
            for chunk in chat.stream({"input": user_input, "chat_history": chat_history}):
                if "answer" in chunk:
                    yield f"data: {chunk['answer']}\n\n"
        
        return Response(
            stream_with_context(generate()), mimetype="text/event-stream"
        )
    else:
        # Use the new LCEL chain interface
        result = chat.invoke({"input": user_input, "chat_history": chat_history})
        
        # Extract the answer and optionally log source documents
        answer = result.get("answer", "I don't know")
        source_docs = result.get("context", [])
        
        # Log source documents for debugging
        if source_docs:
            print(f"📚 Source documents used ({len(source_docs)}):")
            for i, doc in enumerate(source_docs):
                print(f"  Source {i+1}: {doc.page_content[:150]}...")
        else:
            print("⚠️ No source documents returned")
        
        # Save both user message and AI response to database
        from app.web.api import add_message_to_conversation
        
        # Save user message
        add_message_to_conversation(
            conversation_id=conversation.id,
            role="human",
            content=user_input
        )
        
        # Save AI response
        add_message_to_conversation(
            conversation_id=conversation.id,
            role="ai", 
            content=answer
        )
        
        return jsonify({"role": "assistant", "content": answer})
