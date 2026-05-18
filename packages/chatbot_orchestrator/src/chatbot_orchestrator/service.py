from langgraph.graph import StateGraph
from chatbot_orchestrator.graphs.base import GraphBuilder


class ChatService:
    def __init__(
        self,
        graph_builder: GraphBuilder,
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
        self.graph_builder.__init__(llm=self.llm, retriever=self.retriever)
        uncompiled_graph : StateGraph = self.graph_builder.build()

        self._compiled_graph = uncompiled_graph.compile(
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

        return self.parse_output(result["messages"][-1].content)


    def parse_output(self, output) -> str:
        if output is None:
            return "Error."
        if isinstance(output, str):
            return output
        if isinstance(output, list):
            return str(output[-1]["text"])
    