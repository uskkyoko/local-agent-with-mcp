from typing import List
import json
import random
import string
from datetime import datetime, timedelta
from langchain_ollama import OllamaLLM
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from dotenv import load_dotenv

load_dotenv()


model = OllamaLLM(model="llama3.1:8b")

template = ChatPromptTemplate.from_messages([
    ("system", """You are DevHelper, an expert software development assistant. 
    Your job is to read, review, explain, and improve code. 
    You can help with debugging, refactoring, architecture decisions, and explaining difficult concepts. 

    BEHAVIOR RULES: 
    - Provide concise, accurate, developer-friendly explanations. 
    - When reviewing code, focus on correctness, clarity, maintainability, and best practices. 
    - Suggest improvements only when they add real value. 
    - If the user’s request is ambiguous, infer reasonable context rather than asking unnecessary questions. 
    - Always structure answers clearly (bullet points, short paragraphs, etc.). 
    - Do not generate sample data unless explicitly asked. 
    - Do not apply previous dataset logic from earlier versions of this prompt. 

    Your primary role: Be a highly reliable and technically skilled software development assistant.
    """),
    
    MessagesPlaceholder(variable_name="history"),

    ("user", "Here is the question to answer: {user_input}")
])


chain = template | model


def run_agent(user_input: str, history: List[BaseMessage]) -> AIMessage:
    try:
        result = chain.invoke(
            {
                "user_input": user_input,
                "history": history
            },
            config={"recursion_limit": 50}
        )

        if isinstance(result, BaseMessage):
            return result

        return AIMessage(content=str(result))

    except Exception as e:
        return AIMessage(content=f"Error: {str(e)}. Try phrasing it differently.")


if __name__ == "__main__": 
    print("=" * 60)
    print("DevHelper Agent")
    print("=" * 60)
    print("An interactive developer assistant for reviewing, debugging, ")
    print("and improving code. Ask anything related to software development.")
    print()
    print("Examples:")
    print("  - Review this function and suggest improvements")
    print("  - Explain why this FastAPI route throws an error")
    print("  - Refactor this class into a cleaner architecture")
    print("  - Help me design a database model for my service")
    print()
    print("Commands: 'quit' or 'exit' to end")
    print("=" * 60)

    history: List[BaseMessage] = []

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        print("Agent: ", end="", flush=True)
        response = run_agent(user_input, history)
        print(response.content)
        print()

        history += [HumanMessage(content=user_input), response]

    history: List[BaseMessage] = []

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ['quit', 'exit', 'q', ""]:
            print("Goodbye!")
            break

        print("Agent: ", end="", flush=True)
        response = run_agent(user_input, history)
        print(response.content)
        print()

        history += [HumanMessage(content=user_input), response]