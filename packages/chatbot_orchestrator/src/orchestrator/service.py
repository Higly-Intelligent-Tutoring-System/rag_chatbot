from typing import Callable


class ChatService:
    def __init__(
        self,
        graph_builder: Callable,
        llm,
        retriever=None,
        checkpointer=None,
        store=None,
    ):
        self.graph_builder = graph_builder
        self.llm = llm
        self.retriever = retriever
        self.checkpointer = checkpointer
        self.store = store

    async def compile(self):
        builder = self.graph_builder(self.llm, self.retriever)

        self._compiled_graph = builder.compile(
            checkpointer=self.checkpointer,
            store=self.store,
        )

    async def ainvoke(self, message: str, thread_id: str):

        if not self._compiled_graph:
            raise RuntimeError("Graph not compiled")

        config = {
            "configurable": {
                "thread_id": thread_id
            }
        }

        result = await self._compiled_graph.ainvoke(
            {"messages": [{"role": "user", "content": message}]},
            config=config,
        )

        return result["messages"][-1].content