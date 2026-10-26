from datetime import datetime, timezone
import os

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError


# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

if not MONGODB_URI:
    raise ValueError(
        "MONGODB_URI is not set in the .env file."
    )


# --------------------------------------------------
# MongoDB Connection
# --------------------------------------------------

client = MongoClient(
    MONGODB_URI,
    serverSelectionTimeoutMS=5000
)

database = client["deadline_rescue"]

plans_collection = database["plans"]


# --------------------------------------------------
# Test Connection
# --------------------------------------------------

def test_database_connection() -> bool:

    try:
        client.admin.command("ping")
        return True

    except PyMongoError:
        return False


# --------------------------------------------------
# Save Plan
# --------------------------------------------------

def save_plan(result: dict) -> str:

    document = {
        "goal": result.get("goal"),
        "tasks": result.get("tasks"),
        "priorities": result.get("priorities"),
        "constraints": result.get("constraints"),
        "schedule": result.get("schedule"),

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

        "simulation_requested":
            result.get("simulation_requested"),

        "simulation_type":
            result.get("simulation_type"),

        "simulation_change":
            result.get("simulation_change"),

        "simulation_description":
            result.get("simulation_description"),

        "simulated_constraints":
            result.get("simulated_constraints"),

        "simulated_required_hours":
            result.get("simulated_required_hours"),

        "simulated_available_hours":
            result.get("simulated_available_hours"),

        "simulated_shortage_hours":
            result.get("simulated_shortage_hours"),

        "simulated_risk_level":
            result.get("simulated_risk_level"),

        "simulated_risk_reason":
            result.get("simulated_risk_reason"),

        "simulated_replanned_tasks":
            result.get("simulated_replanned_tasks"),

        "simulated_schedule":
            result.get("simulated_schedule"),

        "simulation_reason":
            result.get("simulation_reason"),

        "simulation_impact":
            result.get("simulation_impact"),

        "final_response":
            result.get("final_response"),

        "created_at":
            datetime.now(timezone.utc)
    }

    try:

        inserted = plans_collection.insert_one(
            document
        )

        return str(inserted.inserted_id)

    except PyMongoError as error:

        raise RuntimeError(
            f"Failed to save plan: {error}"
        )


# --------------------------------------------------
# Get Plan
# --------------------------------------------------

def get_plan(plan_id: str):

    from bson import ObjectId

    try:

        document = plans_collection.find_one(
            {"_id": ObjectId(plan_id)}
        )

        if document is None:
            return None

        document["_id"] = str(
            document["_id"]
        )

        return document

    except Exception as error:

        raise RuntimeError(
            f"Failed to retrieve plan: {error}"
        )


# --------------------------------------------------
# Get Recent Plans
# --------------------------------------------------

def get_recent_plans(limit: int = 10):

    documents = plans_collection.find(
        {}
    ).sort(
        "created_at",
        -1
    ).limit(limit)

    plans = []

    for document in documents:

        document["_id"] = str(
            document["_id"]
        )

        plans.append(document)

    return plans