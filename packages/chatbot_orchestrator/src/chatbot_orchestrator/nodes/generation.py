from langchain_core.messages import AIMessage
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document

def build_single_rag_node(llm: BaseChatModel, prompt: ChatPromptTemplate):

    async def generate_single_turn(state):
        # Safe document loading
        docs = state.get("documents") or []

        # Prompt variable building
        context = "\n\n".join(
            f"Source: {doc.metadata.get('source', 'unknown')}\n{doc.page_content}"
            for doc in docs
        )
        question = state["messages"][-1].content

        formatted_messages = prompt.format_messages(
            context=context,
            question=question,
        )

        response = await llm.ainvoke(formatted_messages)

        return {
            "messages": [
                AIMessage(content=response.content)
            ]
        }

    return generate_single_turn


def build_multiple_rag_node(llm: BaseChatModel, prompt: ChatPromptTemplate):

    async def generate_multiple_turn(state):
        # Safe document loading
        docs = state.get("documents") or []

        # Prompt variable building
        context = "\n\n".join(
            f"Source: {doc.metadata.get('source', 'unknown')}\n{doc.page_content}"
            for doc in docs
        )
        question = state["messages"][-1].content

        formatted_messages = prompt.format_messages(
            context=context,
            question=question,
        )

        response = await llm.ainvoke(formatted_messages)

        return {
            "messages": [
                AIMessage(content=response.content)
            ]
        }

    return generate_multiple_turn
    

def build_single_generation_node(llm: BaseChatModel, prompt: ChatPromptTemplate):

    async def generate_single_turn(state):
        context = ""  # No retrieved documents for pure generation (Andrea Graph)
        question = state["messages"][-1].content

        formatted_messages = prompt.format_messages(
            context=context,
            question=question,
        )

        response = await llm.ainvoke(formatted_messages)

        return {
            "messages": [
                AIMessage(content=response.content)
            ]
        }

    return generate_single_turn


def build_multiple_generation_node(llm: BaseChatModel, prompt: ChatPromptTemplate):

    async def generate_multiple_turn(state):
        context = ""  # No retrieved documents for pure generation (Andrea Graph)
        question = state["messages"]

        formatted_messages = prompt.format_messages(
            context=context,
            question=question,
        )

        response = await llm.ainvoke(formatted_messages)

        return {
            "messages": [
                AIMessage(content=response.content)
            ]
        }

    return generate_multiple_turn


def build_andrea_generation_node(llm: BaseChatModel, prompt: ChatPromptTemplate):
    
    async def generate_multiple_turn(state):
        context = ""
        question = state["messages"]
        university = state.get("university", "")
        
        formatted_messages = prompt.format_messages(
            context=context,
            question=question,
            university=university,
        )
        
        response = await llm.ainvoke(formatted_messages)
        
        return {
            "messages": [AIMessage(content=response.content)]
        }
    
    return generate_multiple_turn