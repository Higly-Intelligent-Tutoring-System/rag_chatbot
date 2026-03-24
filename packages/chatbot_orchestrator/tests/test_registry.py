from __future__ import annotations

import pytest

from chatbot_orchestrator.graphs.registry import get_graph_builder, available_graphs
from chatbot_orchestrator.graphs.base import GraphBuilder


class TestRegistry:

    def test_rag_graph_is_registered(self):
        assert "BasicRagGraph" in available_graphs()

    def test_get_existing_graph(self):
        builder = get_graph_builder("BasicRagGraph")
        assert isinstance(builder, GraphBuilder)
        assert builder.name == "BasicRagGraph"

    def test_get_unknown_graph_raises(self):
        with pytest.raises(ValueError, match="Unknown graph"):
            get_graph_builder("nonexistent-graph")

    def test_available_graphs_returns_list(self):
        graphs = available_graphs()
        assert isinstance(graphs, list)
        assert len(graphs) >= 1