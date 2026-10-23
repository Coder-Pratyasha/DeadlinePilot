from fastapi import FastAPI

from pydantic import BaseModel

from .agent import agent

from .state import AgentState


app = FastAPI(

    title="Deadline Rescue Agent",

    description=(
        "Stateful Agentic AI system for "
        "deadline planning, rescue, "
        "replanning and what-if simulation."
    ),

    version="1.0.0"
)


class UserRequest(BaseModel):

    message: str


@app.get("/")
def root():

    return {

        "message":
            "Deadline Rescue Agent is running."
    }


@app.post("/analyze")
def analyze(
    request: UserRequest
):

    initial_state: AgentState = {

        "user_input":
            request.message
    }

    result = agent.invoke(
        initial_state
    )

    return {

        # --------------------------------
        # Original plan
        # --------------------------------

        "goal":
            result.get("goal"),

        "tasks":
            result.get("tasks"),

        "priorities":
            result.get("priorities"),

        "constraints":
            result.get("constraints"),

        "schedule":
            result.get("schedule"),

        "required_hours":
            result.get("required_hours"),

        "available_hours":
            result.get("available_hours"),

        "shortage_hours":
            result.get("shortage_hours"),

        "risk_level":
            result.get("risk_level"),

        "risk_reason":
            result.get("risk_reason"),

        "decision":
            result.get("decision"),

        # --------------------------------
        # Basic rescue
        # --------------------------------

        "rescue_schedule":
            result.get("rescue_schedule"),

        "rescued_hours":
            result.get("rescued_hours"),

        "unresolved_hours":
            result.get("unresolved_hours"),

        "rescue_reason":
            result.get("rescue_reason"),

        # --------------------------------
        # Advanced replanning
        # --------------------------------

        "replanned_tasks":
            result.get("replanned_tasks"),

        "preserved_tasks":
            result.get("preserved_tasks"),

        "reduced_tasks":
            result.get("reduced_tasks"),

        "deferred_tasks":
            result.get("deferred_tasks"),

        "replan_schedule":
            result.get("replan_schedule"),

        "replan_required_hours":
            result.get(
                "replan_required_hours"
            ),

        "replan_unresolved_hours":
            result.get(
                "replan_unresolved_hours"
            ),

        "replan_reason":
            result.get(
                "replan_reason"
            ),

        # --------------------------------
        # What-if simulation
        # --------------------------------

        "simulation_requested":
            result.get(
                "simulation_requested"
            ),

        "simulation_type":
            result.get(
                "simulation_type"
            ),

        "simulation_change":
            result.get(
                "simulation_change"
            ),

        "simulation_description":
            result.get(
                "simulation_description"
            ),

        "simulated_constraints":
            result.get(
                "simulated_constraints"
            ),

        "simulated_required_hours":
            result.get(
                "simulated_required_hours"
            ),

        "simulated_available_hours":
            result.get(
                "simulated_available_hours"
            ),

        "simulated_shortage_hours":
            result.get(
                "simulated_shortage_hours"
            ),

        "simulated_risk_level":
            result.get(
                "simulated_risk_level"
            ),

        "simulated_risk_reason":
            result.get(
                "simulated_risk_reason"
            ),

        "simulated_replanned_tasks":
            result.get(
                "simulated_replanned_tasks"
            ),

        "simulated_schedule":
            result.get(
                "simulated_schedule"
            ),

        "simulation_reason":
            result.get(
                "simulation_reason"
            ),

        "simulation_impact":
            result.get(
                "simulation_impact"
            ),

        # --------------------------------
        # Final
        # --------------------------------

        "final_response":
            result.get(
                "final_response"
            )
    }