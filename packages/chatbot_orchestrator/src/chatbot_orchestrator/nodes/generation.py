from langchain_core.messages import AIMessage
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document

def build_generation_node(llm: BaseChatModel, prompt: ChatPromptTemplate):

    async def generate(state):
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

    return generate