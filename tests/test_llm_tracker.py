"""Tests for LLM Communication Tracker."""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'shared'))

from llm_communication_tracker import (
    LLMCommunicationTracker,
    LLMProvider,
    CommunicationType,
    AgentFramework,
)


class TestLLMCommunicationTracker:
    def setup_method(self):
        self.tracker = LLMCommunicationTracker()

    def _start(self):
        return self.tracker.start_communication(
            agent_id="agent-1",
            agent_name="Test Agent",
            agent_specialty="Internal Medicine",
            provider=LLMProvider.OPENAI,
            model="gpt-4",
            framework=AgentFramework.CREWAI,
        )

    def test_start_communication(self):
        comm_id = self._start()
        assert comm_id is not None
        assert comm_id.startswith("comm_")

    def test_add_message(self):
        comm_id = self._start()
        msg_id = self.tracker.add_message(
            comm_id=comm_id,
            role="user",
            content="Hello",
            tokens=10,
        )
        assert msg_id is not None

    def test_complete_communication(self):
        comm_id = self._start()
        self.tracker.add_message(comm_id, "user", "Hello", tokens=10)
        self.tracker.complete_communication(
            comm_id=comm_id,
            final_response="Hi there",
            response_time_ms=100,
        )
        comm = self.tracker.get_communication(comm_id)
        assert comm is not None
        assert comm.final_response == "Hi there"

    def test_get_communication_stats(self):
        stats = self.tracker.get_communication_stats()
        assert "total" in stats

    def test_get_recent_communications(self):
        comms = self.tracker.get_recent_communications(limit=5)
        assert isinstance(comms, list)


class TestEnums:
    def test_llm_provider(self):
        assert LLMProvider.OPENAI.value == "openai"

    def test_communication_type(self):
        assert CommunicationType.REQUEST.value == "request"

    def test_agent_framework(self):
        assert AgentFramework.CREWAI.value == "crewai"
        assert AgentFramework.AUTOGEN.value == "autogen"
