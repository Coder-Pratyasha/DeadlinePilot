from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .agent import agent
from .state import AgentState
from .database import (
    save_plan,
    get_plan,
    get_recent_plans,
    test_database_connection
)


app = FastAPI(
    title="Deadline Rescue Agent",
    description=(
        "Stateful Agentic AI system for "
        "deadline planning, rescue, "
        "replanning and what-if simulation."
    ),
    version="1.0.0"
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Request Model
# --------------------------------------------------

class UserRequest(BaseModel):
    message: str


# --------------------------------------------------
# Root
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "Deadline Rescue Agent is running."
    }


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/health")
def health_check():

    database_status = test_database_connection()

    return {
        "status": "ok",
        "api": "healthy",
        "database": (
            "connected"
            if database_status
            else "disconnected"
        )
    }


# --------------------------------------------------
# Analyze User Request
# --------------------------------------------------

@app.post("/analyze")
def analyze(
    request: UserRequest
) -> Dict[str, Any]:

    if not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty."
        )

    initial_state: AgentState = {
        "user_input": request.message
    }

    try:

        # Run LangGraph agent
        result = agent.invoke(
            initial_state
        )

        # Save complete plan to MongoDB
        plan_id = save_plan(result)

        return {
            "plan_id": plan_id,

            "goal": result.get("goal"),

            "tasks": result.get("tasks"),

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

            "rescue_schedule":
                result.get("rescue_schedule"),

            "rescued_hours":
                result.get("rescued_hours"),

            "unresolved_hours":
                result.get("unresolved_hours"),

            "rescue_reason":
                result.get("rescue_reason"),

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
                result.get("replan_required_hours"),

            "replan_unresolved_hours":
                result.get("replan_unresolved_hours"),

            "replan_reason":
                result.get("replan_reason"),

            # What-if simulation
            "simulation_requested":
                result.get("simulation_requested"),

            "simulation_type":
                result.get("simulation_type"),

            "simulation_change":
                result.get("simulation_change"),

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

            "final_response":
                result.get("final_response")
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                "Agent execution failed: "
                f"{str(error)}"
            )
        )


# --------------------------------------------------
# Get Saved Plan
# --------------------------------------------------

@app.get("/plans/{plan_id}")
def get_saved_plan(plan_id: str):

    try:

        plan = get_plan(plan_id)

        if plan is None:
            raise HTTPException(
                status_code=404,
                detail="Plan not found."
            )

        return plan

    except HTTPException:
        raise

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to retrieve plan: "
                f"{str(error)}"
            )
        )


# --------------------------------------------------
# Get Recent Plans
# --------------------------------------------------

@app.get("/plans")
def recent_plans():

    try:

        plans = get_recent_plans()

        return {
            "count": len(plans),
            "plans": plans
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to retrieve plans: "
                f"{str(error)}"
            )
        )