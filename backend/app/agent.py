import json
import re

from langgraph.graph import (
    StateGraph,
    START,
    END
)

from .state import AgentState
from .llm import ask_gemini

from .prompts import (
    GOAL_EXTRACTION_PROMPT,
    ADVANCED_REPLANNING_PROMPT,
    WHAT_IF_PROMPT
)

from .tools import (
    # Original planning tools
    allocate_replanned_hours,
    calculate_available_hours,
    calculate_required_hours,
    calculate_shortage,
    calculate_risk,
    prioritize_tasks,
    generate_schedule,

    # Basic rescue
    generate_rescue_schedule,

    # Advanced replanning
    validate_replanned_tasks,
    generate_replan_schedule,
    calculate_replan_metrics,

    # What-if simulation tools
    calculate_simulated_available_hours,
    calculate_simulated_shortage,
    calculate_simulated_risk,
    get_simulated_risk_reason,
    apply_lost_time_simulation,
    apply_extra_time_simulation,
    apply_reduced_availability_simulation,
    apply_increased_availability_simulation,
    calculate_simulated_task_hours
)


# =========================================================
# JSON PARSER
# =========================================================

def parse_json_response(response: str) -> dict:
    """
    Safely parse JSON returned by Gemini.

    Gemini may sometimes return JSON inside Markdown
    code fences, so those fences are removed first.
    """

    response = response.strip()

    if response.startswith("```json"):
        response = response[7:]

    elif response.startswith("```"):
        response = response[3:]

    if response.endswith("```"):
        response = response[:-3]

    response = response.strip()

    try:
        return json.loads(response)

    except json.JSONDecodeError as e:

        raise ValueError(
            "Gemini returned invalid JSON.\n"
            f"Response:\n{response}\n"
            f"Error:\n{e}"
        )


# =========================================================
# NODE 1 — DETECT SIMULATION REQUEST
# =========================================================

def detect_simulation(state: AgentState):

    user_input = state.get(
        "user_input",
        ""
    ).lower().strip()

    simulation_patterns = [
        r"\bwhat if\b",
        r"\bwhat happens if\b",
        r"\bsuppose\b",
        r"\bif i lose\b",
        r"\bif i miss\b",
        r"\bif i gain\b",
        r"\bif i get extra\b",
        r"\bif i have extra\b"
    ]

    simulation_requested = any(
        re.search(
            pattern,
            user_input
        )
        for pattern in simulation_patterns
    )

    return {
        "simulation_requested": simulation_requested
    }

def detect_simulation_day(user_input: str) -> int | None:
    text = user_input.lower()

    if "today" in text:
        return 1

    if "tomorrow" in text:
        return 2

    match = re.search(
        r"in\s+(\d+)\s+days?",
        text
    )

    if match:
        return int(match.group(1)) + 1

    match = re.search(
        r"after\s+(\d+)\s+days?",
        text
    )

    if match:
        return int(match.group(1)) + 1

    return None

# =========================================================
# NODE 2 — UNDERSTAND ORIGINAL REQUEST
# =========================================================

def understand_request(state: AgentState):

    user_input = state["user_input"]

    prompt = GOAL_EXTRACTION_PROMPT.format(
        user_input=user_input
    )

    response = ask_gemini(prompt)

    extracted_data = parse_json_response(
        response
    )

    return {
        "goal": extracted_data.get(
            "goal",
            ""
        ),

        "tasks": extracted_data.get(
            "tasks",
            []
        ),

        "constraints": extracted_data.get(
            "constraints",
            {}
        )
    }


# =========================================================
# NODE 3 — CREATE PRIORITIES
# =========================================================

def create_priorities(state: AgentState):

    tasks = state.get(
        "tasks",
        []
    )

    prioritized_tasks = prioritize_tasks(
        tasks
    )

    return {
        "priorities": prioritized_tasks
    }


# =========================================================
# NODE 4 — CALCULATE ORIGINAL PLAN METRICS
# =========================================================

def calculate_plan_metrics(
    state: AgentState
):

    tasks = state.get(
        "tasks",
        []
    )

    constraints = state.get(
        "constraints",
        {}
    )

    daily_hours = float(
        constraints.get(
            "daily_hours",
            0
        )
    )

    days_remaining = int(
        constraints.get(
            "days_remaining",
            0
        )
    )

    required_hours = calculate_required_hours(
        tasks
    )

    available_hours = calculate_available_hours(
        daily_hours,
        days_remaining
    )

    shortage_hours = calculate_shortage(
        required_hours,
        available_hours
    )

    risk_level = calculate_risk(
        required_hours,
        available_hours
    )

    if risk_level == "LOW":

        risk_reason = (
            "The available time is sufficient "
            "to complete the planned tasks."
        )

    elif risk_level == "MEDIUM":

        risk_reason = (
            "The plan is feasible but has "
            "limited time buffer."
        )

    elif risk_level == "HIGH":

        risk_reason = (
            "The required work is greater "
            "than the available time."
        )

    else:

        risk_reason = (
            "The current plan is significantly "
            "infeasible and requires recovery."
        )

    return {
        "required_hours": round(
            required_hours,
            2
        ),

        "available_hours": round(
            available_hours,
            2
        ),

        "shortage_hours": round(
            shortage_hours,
            2
        ),

        "risk_level": risk_level,

        "risk_reason": risk_reason
    }


# =========================================================
# NODE 5 — CREATE ORIGINAL SCHEDULE
# =========================================================

def create_schedule(state: AgentState):

    priorities = state.get(
        "priorities",
        []
    )

    constraints = state.get(
        "constraints",
        {}
    )

    daily_hours = float(
        constraints.get(
            "daily_hours",
            0
        )
    )

    days_remaining = int(
        constraints.get(
            "days_remaining",
            0
        )
    )

    schedule = generate_schedule(
        priorities,
        daily_hours,
        days_remaining
    )

    return {
        "schedule": schedule
    }


# =========================================================
# ROUTER — AFTER ORIGINAL SCHEDULE
# =========================================================

def route_after_schedule(state: AgentState):

    if state.get(
        "simulation_requested",
        False
    ):

        return "simulation"

    return "risk"


# =========================================================
# NODE 6 — DETECT RISK
# =========================================================

def detect_risk(state: AgentState):

    risk_level = state.get(
        "risk_level",
        "LOW"
    )

    if risk_level in [
        "HIGH",
        "CRITICAL"
    ]:

        decision = "RESCUE_REQUIRED"

    else:

        decision = "PLAN_FEASIBLE"

    return {
        "decision": decision
    }


# =========================================================
# ROUTER — NORMAL RISK
# =========================================================

def route_after_risk(state: AgentState):

    decision = state.get(
        "decision"
    )

    if decision == "RESCUE_REQUIRED":

        return "rescue"

    return "complete"


# =========================================================
# NODE 7 — BASIC RESCUE
# =========================================================

def create_rescue_plan(state: AgentState):

    priorities = state.get(
        "priorities",
        []
    )

    constraints = state.get(
        "constraints",
        {}
    )

    daily_hours = float(
        constraints.get(
            "daily_hours",
            0
        )
    )

    days_remaining = int(
        constraints.get(
            "days_remaining",
            0
        )
    )

    (
        rescue_schedule,
        rescued_hours,
        unresolved_hours
    ) = generate_rescue_schedule(
        priorities,
        daily_hours,
        days_remaining
    )

    if unresolved_hours > 0:

        rescue_reason = (
            "The original plan cannot be completed "
            "within the available time. "
            f"The rescue plan schedules "
            f"{rescued_hours} hours of work, "
            f"leaving {unresolved_hours} hours unresolved."
        )

    else:

        rescue_reason = (
            "The rescue plan successfully fits "
            "all remaining work within the available time."
        )

    return {
        "rescue_schedule": rescue_schedule,

        "rescued_hours": rescued_hours,

        "unresolved_hours": unresolved_hours,

        "rescue_reason": rescue_reason
    }


# =========================================================
# NODE 8 — ADVANCED REPLANNING
# =========================================================

def advanced_replanning(state: AgentState):

    tasks = state.get(
        "tasks",
        []
    )

    constraints = state.get(
        "constraints",
        {}
    )

    prompt = ADVANCED_REPLANNING_PROMPT.format(

        goal=state.get(
            "goal",
            ""
        ),

        tasks=json.dumps(
            tasks,
            indent=2
        ),

        constraints=json.dumps(
            constraints,
            indent=2
        ),

        required_hours=state.get(
            "required_hours",
            0
        ),

        available_hours=state.get(
            "available_hours",
            0
        ),

        shortage_hours=state.get(
            "shortage_hours",
            0
        )
    )

    response = ask_gemini(
        prompt
    )

    data = parse_json_response(
        response
    )

    replanned_tasks = data.get(
        "tasks",
        []
    )

    validated_tasks = validate_replanned_tasks(
        tasks,
        replanned_tasks,
        float(
            state.get(
                "available_hours",
                0
            )
        )
    )

    replan_reason = data.get(
        "overall_reason",
        "The plan was adjusted based on available time."
    )

    return {
        "replanned_tasks": validated_tasks,

        "replan_reason": replan_reason
    }


# =========================================================
# NODE 9 — CREATE ADVANCED REPLAN SCHEDULE
# =========================================================

def create_replan_schedule(
    state: AgentState
):

    replanned_tasks = state.get(
        "replanned_tasks",
        []
    )

    constraints = state.get(
        "constraints",
        {}
    )

    daily_hours = float(
        constraints.get(
            "daily_hours",
            0
        )
    )

    days_remaining = int(
        constraints.get(
            "days_remaining",
            0
        )
    )

    replan_schedule = generate_replan_schedule(
        replanned_tasks,
        daily_hours,
        days_remaining
    )

    (
        replan_required_hours,
        replan_unresolved_hours
    ) = calculate_replan_metrics(
        replanned_tasks
    )

    preserved_tasks = [
        task
        for task in replanned_tasks
        if task["action"] == "PRESERVE"
    ]

    reduced_tasks = [
        task
        for task in replanned_tasks
        if task["action"] == "REDUCE"
    ]

    deferred_tasks = [
        task
        for task in replanned_tasks
        if task["action"] == "DEFER"
    ]

    return {
        "replan_schedule": replan_schedule,

        "replan_required_hours": replan_required_hours,

        "replan_unresolved_hours": replan_unresolved_hours,

        "preserved_tasks": preserved_tasks,

        "reduced_tasks": reduced_tasks,

        "deferred_tasks": deferred_tasks
    }


# =========================================================
# NODE 10 — RESCUE COMPLETE
# =========================================================

def rescue_complete(state: AgentState):

    return {
        "final_response": (
            "The deadline rescue agent generated "
            "an advanced recovery plan."
        )
    }


# =========================================================
# NODE 11 — NORMAL PLAN COMPLETE
# =========================================================

def plan_complete(state: AgentState):

    return {
        "final_response": (
            "The plan has been created successfully."
        )
    }


# =========================================================
# NODE 12 — UNDERSTAND SIMULATION
# =========================================================

def understand_simulation(
    state: AgentState
):

    user_input = state.get(
        "user_input",
        ""
    )

    prompt = WHAT_IF_PROMPT.format(
        user_input=user_input
    )

    response = ask_gemini(
        prompt
    )

    data = parse_json_response(
        response
    )

    simulation_type = data.get(
        "simulation_type",
        ""
    )

    simulation_change = dict(
        data.get(
            "change",
            {}
        )
    )

    affected_day = detect_simulation_day(
    user_input
    )

    if (
        simulation_type == "LOST_TIME"
        and affected_day is not None
    ):
        simulation_change["day"] = affected_day

    # Gemini may return task_name.
    # Our tools internally use task.

    if (
        "task_name" in simulation_change
        and "task" not in simulation_change
    ):

        simulation_change["task"] = (
            simulation_change["task_name"]
        )

    return {
        "simulation_type": simulation_type,

        "simulation_change": simulation_change,

        "simulation_description": data.get(
            "description",
            ""
        )
    }


# =========================================================
# NODE 13 — APPLY SIMULATION
# =========================================================

def apply_simulation(
    state: AgentState
):

    simulation_type = state.get(
        "simulation_type",
        ""
    )

    simulation_change = dict(
        state.get(
            "simulation_change",
            {}
        )
    )

    original_constraints = state.get(
        "constraints",
        {}
    )

    original_tasks = state.get(
        "tasks",
        []
    )

    # -----------------------------------------------------
    # Normalize task key
    # -----------------------------------------------------

    if (
        "task_name" in simulation_change
        and "task" not in simulation_change
    ):

        simulation_change["task"] = (
            simulation_change["task_name"]
        )

    # -----------------------------------------------------
    # Copy original state.
    #
    # The real plan must NEVER be modified.
    # -----------------------------------------------------

    simulated_constraints = dict(
        original_constraints
    )

    simulated_tasks = [
        dict(task)
        for task in original_tasks
    ]

    # -----------------------------------------------------
    # LOST TIME
    # -----------------------------------------------------

    if simulation_type == "LOST_TIME":

        hours = float(
            simulation_change.get(
                "hours",
                0
            )
        )

        affected_day = simulation_change.get(
            "day"
        )

        if affected_day is not None:
            affected_day = int(
                affected_day
            )

        simulated_constraints = (
            apply_lost_time_simulation(
                simulated_constraints,
                hours,
                affected_day
            )
        )
    # -----------------------------------------------------
    # EXTRA TIME
    # -----------------------------------------------------

    elif simulation_type == "EXTRA_TIME":

        hours = float(
            simulation_change.get(
                "hours",
                0
            )
        )

        simulated_constraints = (
            apply_extra_time_simulation(
                simulated_constraints,
                hours
            )
        )

    # -----------------------------------------------------
    # REDUCED AVAILABILITY
    # -----------------------------------------------------

    elif simulation_type == "REDUCED_AVAILABILITY":

        hours = float(
            simulation_change.get(
                "hours",
                0
            )
        )

        simulated_constraints = (
            apply_reduced_availability_simulation(
                simulated_constraints,
                hours
            )
        )

    # -----------------------------------------------------
    # INCREASED AVAILABILITY
    # -----------------------------------------------------

    elif simulation_type == "INCREASED_AVAILABILITY":

        hours = float(
            simulation_change.get(
                "hours",
                0
            )
        )

        simulated_constraints = (
            apply_increased_availability_simulation(
                simulated_constraints,
                hours
            )
        )

    # -----------------------------------------------------
    # DELAYED TASK
    #
    # We intentionally do not modify the tasks here.
    # calculate_simulated_plan() handles task simulation
    # centrally using calculate_simulated_task_hours().
    # -----------------------------------------------------

    elif simulation_type == "DELAYED_TASK":

        pass

    # -----------------------------------------------------
    # TASK COMPLETED
    # -----------------------------------------------------

    elif simulation_type == "TASK_COMPLETED":

        pass

    return {
        "simulated_constraints":
            simulated_constraints,

        "simulated_tasks":
            simulated_tasks,

        "simulation_change":
            simulation_change
    }


# =========================================================
# NODE 14 — CALCULATE SIMULATED PLAN
# =========================================================

def calculate_simulated_plan(state: AgentState):

    original_tasks = state.get(
        "tasks",
        []
    )

    simulation_type = state.get(
        "simulation_type",
        ""
    )

    simulation_change = state.get(
        "simulation_change",
        {}
    )

    simulated_constraints = state.get(
        "simulated_constraints",
        {}
    ).copy()

    # -----------------------------------------------------
    # Create simulated tasks
    # -----------------------------------------------------
    #
    # For time/availability simulations, the tasks themselves
    # do not change.
    #
    # For task-based simulations, we modify the relevant task.
    # -----------------------------------------------------

    if simulation_type in [
        "DELAYED_TASK",
        "TASK_COMPLETED"
    ]:

        simulated_tasks = calculate_simulated_task_hours(
            original_tasks,
            simulation_change,
            simulation_type
        )

    else:

        simulated_tasks = [
            dict(task)
            for task in original_tasks
        ]

    # -----------------------------------------------------
    # Calculate required hours
    # -----------------------------------------------------

    simulated_required_hours = round(
        sum(
            float(
                task.get(
                    "remaining_hours",
                    0
                )
            )
            for task in simulated_tasks
        ),
        2
    )

    # -----------------------------------------------------
    # Calculate available hours
    # -----------------------------------------------------

    if "total_available_hours" in simulated_constraints:

        simulated_available_hours = float(
            simulated_constraints[
                "total_available_hours"
            ]
        )

    else:

        daily_hours = float(
            simulated_constraints.get(
                "daily_hours",
                0
            )
        )

        days_remaining = int(
            simulated_constraints.get(
                "days_remaining",
                0
            )
        )

        simulated_available_hours = (
            daily_hours * days_remaining
        )

    simulated_available_hours = round(
        simulated_available_hours,
        2
    )

    # -----------------------------------------------------
    # Calculate shortage
    # -----------------------------------------------------

    simulated_shortage_hours = round(
        max(
            0,
            simulated_required_hours
            - simulated_available_hours
        ),
        2
    )

    # -----------------------------------------------------
    # Calculate risk
    # -----------------------------------------------------

    simulated_risk_level = calculate_simulated_risk(
        simulated_required_hours,
        simulated_available_hours
    )

    simulated_risk_reason = get_simulated_risk_reason(
        simulated_risk_level
    )

    return {
        "simulated_tasks":
            simulated_tasks,

        "simulated_required_hours":
            simulated_required_hours,

        "simulated_available_hours":
            simulated_available_hours,

        "simulated_shortage_hours":
            simulated_shortage_hours,

        "simulated_risk_level":
            simulated_risk_level,

        "simulated_risk_reason":
            simulated_risk_reason
    }

# =========================================================
# NODE 15 — CREATE SIMULATED REPLAN
# =========================================================

def create_simulated_replan(state: AgentState):

    # Use simulated tasks if available.
    # Otherwise fall back to the original tasks.
    # This prevents the recovery plan from becoming empty
    # if the simulated task state was not preserved.
    simulated_tasks = state.get(
        "simulated_tasks"
    ) or state.get(
        "tasks",
        []
    )

    simulated_constraints = state.get(
        "simulated_constraints",
        {}
    )

    simulated_required_hours = float(
        state.get(
            "simulated_required_hours",
            0
        )
    )

    simulated_available_hours = float(
        state.get(
            "simulated_available_hours",
            0
        )
    )

    simulated_shortage_hours = float(
        state.get(
            "simulated_shortage_hours",
            0
        )
    )

    # -----------------------------------------------------
    # No tasks
    # -----------------------------------------------------

    if not simulated_tasks:

        return {
            "simulated_replanned_tasks": [],
            "simulated_schedule": {},
            "simulation_reason": (
                "No tasks are available for the "
                "simulated recovery plan."
            )
        }

    # -----------------------------------------------------
    # If simulation is feasible
    # -----------------------------------------------------

    if simulated_shortage_hours <= 0:

        daily_hours = float(
            simulated_constraints.get(
                "daily_hours",
                0
            )
        )

        days_remaining = int(
            simulated_constraints.get(
                "days_remaining",
                0
            )
        )

        if (
            "total_available_hours"
            in simulated_constraints
            and days_remaining > 0
        ):

            effective_daily_hours = (
                simulated_available_hours
                / days_remaining
            )

        else:

            effective_daily_hours = daily_hours

        simulated_priorities = prioritize_tasks(
            simulated_tasks
        )

        simulated_schedule = generate_schedule(
            simulated_priorities,
            effective_daily_hours,
            days_remaining
        )

        return {
            "simulated_replanned_tasks":
                simulated_tasks,

            "simulated_schedule":
                simulated_schedule,

            "simulation_reason": (
                "The hypothetical change does not "
                "create a time shortage, so the "
                "original task requirements can "
                "still be maintained."
            )
        }

    # =====================================================
    # RECOVERY IS REQUIRED
    # =====================================================

    total_available = max(
        0.0,
        simulated_available_hours
    )

    total_required = max(
        0.0,
        simulated_required_hours
    )

    # -----------------------------------------------------
    # Priority-aware allocation
    # -----------------------------------------------------

    replanned_tasks = allocate_replanned_hours(
        simulated_tasks,
        simulated_available_hours
    )
    # -----------------------------------------------------
    # Fix rounding difference
    # -----------------------------------------------------

    total_replanned = round(
        sum(
            task["replanned_hours"]
            for task in replanned_tasks
        ),
        2
    )

    difference = round(
        total_available - total_replanned,
        2
    )

    if difference > 0:

        for task in replanned_tasks:

            if difference <= 0:
                break

            original_hours = float(
                task["original_hours"]
            )

            current_hours = float(
                task["replanned_hours"]
            )

            remaining_capacity = (
                original_hours
                - current_hours
            )

            addition = min(
                difference,
                remaining_capacity
            )

            if addition > 0:

                task["replanned_hours"] = round(
                    current_hours + addition,
                    2
                )

                if (
                    task["replanned_hours"]
                    >= original_hours
                ):
                    task["action"] = "PRESERVE"
                else:
                    task["action"] = "REDUCE"

                difference = round(
                    difference - addition,
                    2
                )

    # -----------------------------------------------------
    # Generate simulated schedule
    # -----------------------------------------------------

    daily_hours = float(
        simulated_constraints.get(
            "daily_hours",
            0
        )
    )

    days_remaining = int(
        simulated_constraints.get(
            "days_remaining",
            0
        )
    )

    daily_hours_by_day = (
        simulated_constraints.get(
            "daily_hours_by_day"
        )
    )

    simulated_schedule = generate_replan_schedule(
        replanned_tasks,
        daily_hours,
        days_remaining,
        daily_hours_by_day
    )

    simulation_reason = (
        f"The simulated scenario leaves "
        f"{simulated_available_hours:.1f} hours "
        f"available against "
        f"{simulated_required_hours:.1f} hours "
        f"of required work. "
        f"The recovery plan allocates the available "
        f"time according to task priority."
    )
    return {
        "simulated_replanned_tasks":
            replanned_tasks,

        "simulated_schedule":
            simulated_schedule,

        "simulation_reason":
            simulation_reason
    }

# =========================================================
# NODE 16 — CALCULATE SIMULATION IMPACT
# =========================================================

def calculate_simulation_impact(
    state: AgentState
):

    original_available = float(
        state.get(
            "available_hours",
            0
        )
    )

    simulated_available = float(
        state.get(
            "simulated_available_hours",
            0
        )
    )

    original_shortage = float(
        state.get(
            "shortage_hours",
            0
        )
    )

    simulated_shortage = float(
        state.get(
            "simulated_shortage_hours",
            0
        )
    )

    available_difference = (
        simulated_available
        - original_available
    )

    shortage_difference = (
        simulated_shortage
        - original_shortage
    )

    # -----------------------------------------------------
    # Available time impact
    # -----------------------------------------------------

    if available_difference < 0:

        time_impact = (
            f"You lose "
            f"{abs(available_difference):.2f} "
            f"hours of available time."
        )

    elif available_difference > 0:

        time_impact = (
            f"You gain "
            f"{available_difference:.2f} "
            f"hours of available time."
        )

    else:

        time_impact = (
            "The total available time remains unchanged."
        )

    # -----------------------------------------------------
    # Shortage impact
    # -----------------------------------------------------

    if shortage_difference > 0:

        shortage_impact = (
            f"The time shortage increases by "
            f"{shortage_difference:.2f} hours."
        )

    elif shortage_difference < 0:

        shortage_impact = (
            f"The time shortage decreases by "
            f"{abs(shortage_difference):.2f} hours."
        )

    else:

        shortage_impact = (
            "The time shortage remains unchanged."
        )

    simulation_impact = (
        f"{time_impact} "
        f"{shortage_impact}"
    )

    return {
        "simulation_impact":
            simulation_impact
    }


# =========================================================
# NODE 17 — SIMULATION COMPLETE
# =========================================================

def simulation_complete(state: AgentState):

    description = state.get(
        "simulation_description",
        ""
    )

    original_risk = state.get(
        "risk_level",
        "UNKNOWN"
    )

    simulated_risk = state.get(
        "simulated_risk_level",
        "UNKNOWN"
    )

    original_available = state.get(
        "available_hours",
        0
    )

    simulated_available = state.get(
        "simulated_available_hours",
        0
    )

    original_shortage = state.get(
        "shortage_hours",
        0
    )

    simulated_shortage = state.get(
        "simulated_shortage_hours",
        0
    )

    simulation_reason = state.get(
        "simulation_reason",
        ""
    )

    simulation_impact = state.get(
        "simulation_impact",
        ""
    )

    replanned_tasks = state.get(
        "simulated_replanned_tasks",
        []
    )

    simulated_schedule = state.get(
        "simulated_schedule",
        {}
    )

    # -----------------------------------------------------
    # Build recovery plan text
    # -----------------------------------------------------

    recovery_text = ""

    if replanned_tasks:

        recovery_text += (
            "\nSimulated Recovery Plan\n"
        )

        for task in replanned_tasks:

            recovery_text += (
                f"- {task['name']}: "
                f"{task['replanned_hours']:.2f} hours "
                f"({task['action']})\n"
            )

        recovery_text += "\nSimulated Schedule\n"

        for day, tasks in simulated_schedule.items():

            recovery_text += f"{day}:\n"

            for task in tasks:

                recovery_text += (
                    f"  - {task['task']}: "
                    f"{task['hours']:.2f} hours\n"
                )

    else:

        recovery_text = (
            "\nSimulated Recovery Plan\n"
            "No recovery plan could be generated."
        )

    final_response = (
        "What-If Simulation\n\n"

        f"Scenario: {description}\n\n"

        "Original Plan\n"
        f"- Available time: "
        f"{original_available} hours\n"
        f"- Shortage: "
        f"{original_shortage} hours\n"
        f"- Risk: "
        f"{original_risk}\n\n"

        "Simulated Plan\n"
        f"- Available time: "
        f"{simulated_available} hours\n"
        f"- Shortage: "
        f"{simulated_shortage} hours\n"
        f"- Risk: "
        f"{simulated_risk}\n\n"

        f"Impact: {simulation_impact}\n"

        f"{recovery_text}\n"

        f"\nDecision: {simulation_reason}"
    )

    return {
        "final_response": final_response
    }
# =========================================================
# LANGGRAPH WORKFLOW
# =========================================================

builder = StateGraph(
    AgentState
)


# =========================================================
# REGISTER NORMAL PLANNING NODES
# =========================================================

builder.add_node(
    "detect_simulation",
    detect_simulation
)

builder.add_node(
    "understand_request",
    understand_request
)

builder.add_node(
    "create_priorities",
    create_priorities
)

builder.add_node(
    "calculate_plan_metrics",
    calculate_plan_metrics
)

builder.add_node(
    "create_schedule",
    create_schedule
)

builder.add_node(
    "detect_risk",
    detect_risk
)

builder.add_node(
    "create_rescue_plan",
    create_rescue_plan
)

builder.add_node(
    "advanced_replanning",
    advanced_replanning
)

builder.add_node(
    "create_replan_schedule",
    create_replan_schedule
)

builder.add_node(
    "rescue_complete",
    rescue_complete
)

builder.add_node(
    "plan_complete",
    plan_complete
)


# =========================================================
# REGISTER SIMULATION NODES
# =========================================================

builder.add_node(
    "understand_simulation",
    understand_simulation
)

builder.add_node(
    "apply_simulation",
    apply_simulation
)

builder.add_node(
    "calculate_simulated_plan",
    calculate_simulated_plan
)

builder.add_node(
    "create_simulated_replan",
    create_simulated_replan
)

builder.add_node(
    "calculate_simulation_impact",
    calculate_simulation_impact
)

builder.add_node(
    "simulation_complete",
    simulation_complete
)


# =========================================================
# INITIAL WORKFLOW
#
# IMPORTANT:
# Every request first builds the original plan.
# This is required for What-If simulation because the
# simulation needs the original tasks and metrics.
# =========================================================

builder.add_edge(
    START,
    "detect_simulation"
)

builder.add_edge(
    "detect_simulation",
    "understand_request"
)


# =========================================================
# ORIGINAL PLAN
# =========================================================

builder.add_edge(
    "understand_request",
    "create_priorities"
)

builder.add_edge(
    "create_priorities",
    "calculate_plan_metrics"
)

builder.add_edge(
    "calculate_plan_metrics",
    "create_schedule"
)


# =========================================================
# AFTER ORIGINAL SCHEDULE
# =========================================================

builder.add_conditional_edges(
    "create_schedule",
    route_after_schedule,
    {
        "simulation": "understand_simulation",
        "risk": "detect_risk"
    }
)


# =========================================================
# NORMAL RISK ROUTING
# =========================================================

builder.add_conditional_edges(
    "detect_risk",
    route_after_risk,
    {
        "rescue": "create_rescue_plan",
        "complete": "plan_complete"
    }
)


# =========================================================
# BASIC RESCUE
# =========================================================

builder.add_edge(
    "create_rescue_plan",
    "advanced_replanning"
)


# =========================================================
# ADVANCED REPLANNING
# =========================================================

builder.add_edge(
    "advanced_replanning",
    "create_replan_schedule"
)

builder.add_edge(
    "create_replan_schedule",
    "rescue_complete"
)


# =========================================================
# NORMAL WORKFLOW END
# =========================================================

builder.add_edge(
    "rescue_complete",
    END
)

builder.add_edge(
    "plan_complete",
    END
)


# =========================================================
# WHAT-IF SIMULATION WORKFLOW
# =========================================================

builder.add_edge(
    "understand_simulation",
    "apply_simulation"
)

builder.add_edge(
    "apply_simulation",
    "calculate_simulated_plan"
)

builder.add_edge(
    "calculate_simulated_plan",
    "create_simulated_replan"
)

builder.add_edge(
    "create_simulated_replan",
    "calculate_simulation_impact"
)

builder.add_edge(
    "calculate_simulation_impact",
    "simulation_complete"
)

builder.add_edge(
    "simulation_complete",
    END
)


# =========================================================
# COMPILE AGENT
# =========================================================

agent = builder.compile()