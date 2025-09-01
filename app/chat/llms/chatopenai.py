from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI as LegacyChatOpenAI

def build_llm(chat_args):
    # Use the legacy ChatOpenAI that works with openai==0.28.1
    return LegacyChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.1,
        streaming=chat_args.streaming
    )
