from langchain_openai import ChatOpenAI

def build_llm(chat_args):
    return ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.1,
        streaming=chat_args.streaming
    )
