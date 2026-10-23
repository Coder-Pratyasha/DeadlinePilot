GOAL_EXTRACTION_PROMPT = """
You are the information extraction component of a Deadline Rescue Agent.

Extract structured planning information from the user's request.

Extract:

1. goal
2. tasks
3. constraints

For every task, extract:
- name
- remaining_hours
- deadline
- importance

For constraints, extract:
- daily_hours
- days_remaining

Rules:

- Return ONLY JSON.
- Do not add explanations.
- Do not use Markdown.
- Do not wrap the JSON in ```json or ``` blocks.
- If a value is unknown, use null.
- importance must be an integer from 1 to 5.
- If task duration is not explicitly provided, estimate a reasonable value.
- If a deadline is given as a day such as Friday, calculate days_remaining using today's date.

Return exactly this structure:

{{
    "goal": "string",
    "tasks": [
        {{
            "name": "string",
            "remaining_hours": 0,
            "deadline": "string",
            "importance": 1
        }}
    ],
    "constraints": {{
        "daily_hours": 0,
        "days_remaining": 0
    }}
}}

User request:
{user_input}
"""


ADVANCED_REPLANNING_PROMPT = """
You are the decision-making component of a Deadline Rescue Agent.

The original plan is not feasible because there is not enough time.

Your job is to create an intelligent recovery strategy.

For every task, decide whether it should be:

1. PRESERVED
   - Keep most or all of its required preparation.
   - Use this for high-importance or deadline-critical tasks.

2. REDUCED
   - Reduce the amount of preparation.
   - Keep the task active but focus on essential preparation.

3. DEFERRED
   - Move the task out of the current planning window.
   - Use this when time is severely limited.

Important rules:

- Never change the user's original task data.
- original_hours represents the actual work still required.
- Create a NEW replanned_hours value for the recovery plan.
- The total replanned hours should fit within available hours whenever possible.
- Higher importance should generally receive more time.
- Do not arbitrarily delete tasks.
- Every task must appear exactly once.
- Give a short reason for every decision.

Return ONLY valid JSON.

Return exactly this structure:

{{
    "tasks": [
        {{
            "name": "string",
            "action": "PRESERVE",
            "original_hours": 0,
            "replanned_hours": 0,
            "reason": "string"
        }}
    ],
    "overall_reason": "string"
}}

Possible action values:

PRESERVE
REDUCE
DEFER

Current goal:
{goal}

Current tasks:
{tasks}

Current constraints:
{constraints}

Required hours:
{required_hours}

Available hours:
{available_hours}

Shortage:
{shortage_hours}
"""


WHAT_IF_PROMPT = """
You are the What-If Simulation component of a Deadline Rescue Agent.

The user wants to understand what would happen if a hypothetical change
were applied to their current plan.

IMPORTANT:

- This is a simulation only.
- NEVER modify the original plan.
- NEVER assume the hypothetical change has actually happened.
- Analyze only the simulated scenario.
- Explain the impact clearly.
- The simulation should help the user make a decision.

Possible simulation types include:

1. LOST_TIME
   The user loses a certain number of available hours.

2. EXTRA_TIME
   The user gains additional available hours.

3. DELAYED_TASK
   A specific task takes longer than expected.

4. TASK_COMPLETED
   A specific task is completed earlier than expected.

5. REDUCED_AVAILABILITY
   The user's daily available time decreases.

6. INCREASED_AVAILABILITY
   The user's daily available time increases.

For task-based simulations, use the exact task name
from the user's request.

Return ONLY valid JSON.

Return exactly this structure:

{{
    "simulation_type": "LOST_TIME",
    "change": {{
        "hours": 0,
        "task": null
    }},
    "description": "string"
}}

Rules:

For LOST_TIME:
- simulation_type = "LOST_TIME"
- hours = number of hours lost
- task = null

For EXTRA_TIME:
- simulation_type = "EXTRA_TIME"
- hours = number of additional hours available
- task = null

For REDUCED_AVAILABILITY:
- simulation_type = "REDUCED_AVAILABILITY"
- hours = number of daily hours reduced
- task = null

For INCREASED_AVAILABILITY:
- simulation_type = "INCREASED_AVAILABILITY"
- hours = number of daily hours increased
- task = null

For DELAYED_TASK:
- simulation_type = "DELAYED_TASK"
- hours = additional hours required by the task
- task = exact task name

For TASK_COMPLETED:
- simulation_type = "TASK_COMPLETED"
- hours = 0
- task = exact task name

Possible simulation_type values:

LOST_TIME
EXTRA_TIME
DELAYED_TASK
TASK_COMPLETED
REDUCED_AVAILABILITY
INCREASED_AVAILABILITY

User request:
{user_input}
"""