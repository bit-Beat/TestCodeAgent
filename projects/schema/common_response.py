from pydantic import BaseModel, Field
from typing import List, Literal, Optional


class AgentCommonResponse(BaseModel):
    """Common response fields shared by sub-agents."""

    run_id: Optional[str] = Field(
        default=None,
        description="ID that groups one full agent execution, such as YYYYMMDD_HHmmss.",
    )
    step_id: Optional[int] = Field(
        default=None,
        description="Current sub-agent step number in the orchestration flow.",
    )
    agent_name: str = Field(
        default="",
        description="Name of the sub-agent that produced this response.",
    )
    user_request: str = Field(
        default="",
        description="Original user request or summarized input for this sub-agent.",
    )
    summary: str = Field(
        default="",
        description="Short summary of the sub-agent result.",
    )
    next_input: Optional[str] = Field(
        default=None,
        description="Suggested input or handoff note for the next sub-agent.",
    )
    target_classes: Optional[List[str]] = Field(
        default=None,
        description="Target Java classes related to this response.",
    )
    status: Literal["success", "partial_success", "failed", "blocked", "skipped"] = Field(
        default="success",
        description="Execution status of the sub-agent.",
    )
