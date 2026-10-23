from typing import TypedDict, List, Dict, Any


class AgentState(TypedDict, total=False):

    # -----------------------------
    # User input
    # -----------------------------

    user_input: str

    # -----------------------------
    # Goal and planning information
    # -----------------------------

    goal: str

    tasks: List[Dict[str, Any]]

    constraints: Dict[str, Any]

    priorities: List[Dict[str, Any]]

    schedule: Dict[str, List[Dict[str, Any]]]

    # -----------------------------
    # Progress information
    # -----------------------------

    completed_tasks: List[str]

    delayed_tasks: List[str]

    # -----------------------------
    # Original plan metrics
    # -----------------------------

    required_hours: float

    available_hours: float

    shortage_hours: float

    risk_level: str

    risk_reason: str

    decision: str

    # -----------------------------
    # Basic rescue
    # -----------------------------

    rescue_schedule: Dict[str, List[Dict[str, Any]]]

    rescued_hours: float

    unresolved_hours: float

    rescue_reason: str

    # -----------------------------
    # Advanced replanning
    # -----------------------------

    replanned_tasks: List[Dict[str, Any]]

    replan_schedule: Dict[str, List[Dict[str, Any]]]

    preserved_tasks: List[Dict[str, Any]]

    reduced_tasks: List[Dict[str, Any]]

    deferred_tasks: List[Dict[str, Any]]

    replan_reason: str

    replan_required_hours: float

    replan_unresolved_hours: float

    # -----------------------------
    # What-if simulation
    # -----------------------------

    simulation_requested: bool

    simulation_type: str

    simulation_change: Dict[str, Any]

    simulation_description: str

    simulated_constraints: Dict[str, Any]

    simulated_required_hours: float

    simulated_available_hours: float

    simulated_shortage_hours: float

    simulated_risk_level: str

    simulated_risk_reason: str

    simulated_replanned_tasks: List[Dict[str, Any]]

    simulated_schedule: Dict[str, List[Dict[str, Any]]]

    simulation_reason: str

    simulation_impact: str

    # -----------------------------
    # Final response
    # -----------------------------

    final_response: str