from langchain_core.messages import AIMessage


def build_generation_node(llm, prompt):

    async def generate(state):
        context = "\n\n".join(state.get("documents", []))
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