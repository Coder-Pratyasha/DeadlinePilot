import re

def calculate_available_hours(
    daily_hours: float,
    days_remaining: int
) -> float:

    if daily_hours < 0 or days_remaining < 0:
        return 0.0

    return daily_hours * days_remaining


def calculate_required_hours(tasks: list) -> float:

    total_hours = 0.0

    for task in tasks:

        hours = task.get("remaining_hours")

        if hours is not None:
            total_hours += float(hours)

    return total_hours


def calculate_shortage(
    required_hours: float,
    available_hours: float
) -> float:

    shortage = required_hours - available_hours

    return max(0.0, shortage)


def calculate_risk(
    required_hours: float,
    available_hours: float
) -> str:

    if available_hours <= 0:

        if required_hours > 0:
            return "CRITICAL"

        return "LOW"

    ratio = required_hours / available_hours

    if ratio > 1.2:
        return "CRITICAL"

    if ratio > 1:
        return "HIGH"

    if ratio > 0.8:
        return "MEDIUM"

    return "LOW"


def calculate_task_priority(task: dict) -> float:

    importance = task.get("importance", 1)
    remaining_hours = task.get("remaining_hours", 0)

    priority = (
        importance * 10
    ) + (
        10 / max(float(remaining_hours), 1)
    )

    return round(priority, 2)


def prioritize_tasks(tasks: list) -> list:

    prioritized_tasks = []

    for task in tasks:

        task_copy = task.copy()

        priority_score = calculate_task_priority(
            task_copy
        )

        task_copy["priority_score"] = priority_score

        prioritized_tasks.append(task_copy)

    prioritized_tasks.sort(
        key=lambda task: task["priority_score"],
        reverse=True
    )

    return prioritized_tasks


def generate_schedule(
    tasks: list,
    daily_hours: float,
    days_remaining: int
) -> dict:

    schedule = {}

    if daily_hours <= 0 or days_remaining <= 0:
        return schedule

    remaining_task_hours = {}

    for task in tasks:

        remaining_task_hours[
            task["name"]
        ] = float(
            task.get("remaining_hours", 0)
        )

    for day in range(
        1,
        days_remaining + 1
    ):

        day_key = f"Day {day}"

        schedule[day_key] = []

        available_today = float(daily_hours)

        for task in tasks:

            task_name = task["name"]

            remaining = remaining_task_hours[
                task_name
            ]

            if remaining <= 0:
                continue

            if available_today <= 0:
                break

            allocated = min(
                remaining,
                available_today
            )

            schedule[day_key].append({
                "task": task_name,
                "hours": round(
                    allocated,
                    2
                )
            })

            remaining_task_hours[
                task_name
            ] -= allocated

            available_today -= allocated

    return schedule


def generate_rescue_schedule(
    tasks: list,
    daily_hours: float,
    days_remaining: int
) -> tuple:

    rescue_schedule = {}

    if daily_hours <= 0 or days_remaining <= 0:
        return rescue_schedule, 0.0, 0.0

    total_available_hours = (
        daily_hours * days_remaining
    )

    total_required_hours = sum(
        float(task.get("remaining_hours", 0))
        for task in tasks
    )

    if total_required_hours <= total_available_hours:

        normal_schedule = generate_schedule(
            tasks,
            daily_hours,
            days_remaining
        )

        return (
            normal_schedule,
            total_required_hours,
            0.0
        )

    total_priority = sum(
        float(task.get("priority_score", 0))
        for task in tasks
    )

    allocations = {}

    if total_priority <= 0:

        weight = 1 / len(tasks)

        for task in tasks:

            allocations[
                task["name"]
            ] = min(
                float(task.get("remaining_hours", 0)),
                total_available_hours * weight
            )

    else:

        for task in tasks:

            name = task["name"]

            required = float(
                task.get(
                    "remaining_hours",
                    0
                )
            )

            priority = float(
                task.get(
                    "priority_score",
                    0
                )
            )

            weighted_hours = (
                total_available_hours
                * priority
                / total_priority
            )

            allocations[name] = min(
                required,
                weighted_hours
            )

    allocated_total = sum(
        allocations.values()
    )

    remaining_capacity = (
        total_available_hours
        - allocated_total
    )

    while remaining_capacity > 0.01:

        candidates = []

        for task in tasks:

            name = task["name"]

            required = float(
                task.get(
                    "remaining_hours",
                    0
                )
            )

            allocated = allocations.get(
                name,
                0
            )

            remaining = required - allocated

            if remaining > 0.01:
                candidates.append(task)

        if not candidates:
            break

        candidates.sort(
            key=lambda task: float(
                task.get(
                    "priority_score",
                    0
                )
            ),
            reverse=True
        )

        progress = False

        for task in candidates:

            name = task["name"]

            required = float(
                task.get(
                    "remaining_hours",
                    0
                )
            )

            allocated = allocations[name]

            remaining = required - allocated

            extra = min(
                remaining,
                remaining_capacity
            )

            allocations[name] += extra
            remaining_capacity -= extra

            progress = True

            if remaining_capacity <= 0.01:
                break

        if not progress:
            break

    remaining_allocations = {
        name: round(hours, 2)
        for name, hours in allocations.items()
        if hours > 0.01
    }

    for day in range(
        1,
        days_remaining + 1
    ):

        day_key = f"Day {day}"

        rescue_schedule[day_key] = []

        available_today = float(daily_hours)

        for task in tasks:

            name = task["name"]

            remaining = remaining_allocations.get(
                name,
                0
            )

            if remaining <= 0.01:
                continue

            if available_today <= 0.01:
                break

            allocated_today = min(
                remaining,
                available_today
            )

            rescue_schedule[
                day_key
            ].append({
                "task": name,
                "hours": round(
                    allocated_today,
                    2
                ),
                "priority": task.get(
                    "priority_score",
                    0
                )
            })

            remaining_allocations[name] -= (
                allocated_today
            )

            available_today -= allocated_today

    rescued_hours = sum(
        sum(
            item["hours"]
            for item in day_tasks
        )
        for day_tasks in rescue_schedule.values()
    )

    unresolved_hours = max(
        0.0,
        total_required_hours - rescued_hours
    )

    return (
        rescue_schedule,
        round(rescued_hours, 2),
        round(unresolved_hours, 2)
    )


# =========================================================
# ADVANCED REPLANNING
# =========================================================

def validate_replanned_tasks(
    original_tasks: list,
    replanned_tasks: list,
    available_hours: float
) -> list:
    """
    Validate Gemini's replanning decisions.

    The original task data is never modified.
    """

    original_map = {
        task["name"]: task
        for task in original_tasks
    }

    validated = []
    seen = set()

    for item in replanned_tasks:

        name = item.get("name")

        if name not in original_map:
            continue

        if name in seen:
            continue

        seen.add(name)

        original_task = original_map[name]

        original_hours = float(
            original_task.get(
                "remaining_hours",
                0
            )
        )

        action = item.get(
            "action",
            "REDUCE"
        )

        if action not in {
            "PRESERVE",
            "REDUCE",
            "DEFER"
        }:
            action = "REDUCE"

        replanned_hours = float(
            item.get(
                "replanned_hours",
                0
            )
        )

        replanned_hours = max(
            0.0,
            replanned_hours
        )

        replanned_hours = min(
            original_hours,
            replanned_hours
        )

        if action == "PRESERVE":

            replanned_hours = original_hours

        elif action == "DEFER":

            replanned_hours = 0.0

        validated.append({
            "name": name,
            "action": action,
            "original_hours": round(
                original_hours,
                2
            ),
            "replanned_hours": round(
                replanned_hours,
                2
            ),
            "importance": original_task.get(
                "importance",
                1
            ),
            "deadline": original_task.get(
                "deadline"
            ),
            "reason": item.get(
                "reason",
                "Adjusted based on available time."
            )
        })

    # Safety fallback:
    # if Gemini missed any task, add it as deferred.
    for task in original_tasks:

        name = task["name"]

        if name in seen:
            continue

        validated.append({
            "name": name,
            "action": "DEFER",
            "original_hours": float(
                task.get(
                    "remaining_hours",
                    0
                )
            ),
            "replanned_hours": 0.0,
            "importance": task.get(
                "importance",
                1
            ),
            "deadline": task.get(
                "deadline"
            ),
            "reason": (
                "Deferred because it was not possible "
                "to fit all work within the available time."
            )
        })

    # -----------------------------------------------------
    # Make sure the replan never exceeds available hours.
    # -----------------------------------------------------

    total_replanned = sum(
        task["replanned_hours"]
        for task in validated
    )

    if total_replanned > available_hours:

        overflow = (
            total_replanned
            - available_hours
        )

        # Reduce lower-importance work first.
        adjustable = sorted(
            validated,
            key=lambda task: (
                task["importance"],
                -task["replanned_hours"]
            )
        )

        for task in adjustable:

            if overflow <= 0:
                break

            reducible = min(
                task["replanned_hours"],
                overflow
            )

            task["replanned_hours"] -= reducible

            overflow -= reducible

            if task["replanned_hours"] <= 0.01:

                task["replanned_hours"] = 0.0

                if task["action"] != "PRESERVE":
                    task["action"] = "DEFER"

    return validated

def allocate_replanned_hours(
    tasks: list,
    available_hours: float
) -> list:
    """
    Allocate available hours across tasks according to priority.

    Higher importance and priority score receive more time.

    If all tasks have equal priority, the allocation becomes
    proportional/equal.
    """

    available_hours = max(
        0.0,
        float(available_hours)
    )

    if not tasks:
        return []

    total_required = sum(
        max(
            0.0,
            float(task.get("remaining_hours", 0))
        )
        for task in tasks
    )

    if total_required <= 0:
        return [
            {
                "name": task.get("name", ""),
                "action": "DEFER",
                "original_hours": 0.0,
                "replanned_hours": 0.0,
                "importance": task.get("importance", 1),
                "priority_score": task.get(
                    "priority_score",
                    calculate_task_priority(task)
                ),
                "reason": "No remaining work is required."
            }
            for task in tasks
        ]

    # If enough time exists, preserve everything.
    if available_hours >= total_required:

        result = []

        for task in tasks:

            original_hours = max(
                0.0,
                float(task.get("remaining_hours", 0))
            )

            importance = int(
                task.get("importance", 1)
            )

            priority_score = float(
                task.get(
                    "priority_score",
                    calculate_task_priority(task)
                )
            )

            result.append(
                {
                    "name": task.get("name", ""),
                    "action": "PRESERVE",
                    "original_hours": round(
                        original_hours,
                        2
                    ),
                    "replanned_hours": round(
                        original_hours,
                        2
                    ),
                    "importance": importance,
                    "priority_score": round(
                        priority_score,
                        2
                    ),
                    "reason": (
                        "The task can be fully preserved "
                        "within the available time."
                    )
                }
            )

        return result

    # ---------------------------------------------------------
    # Calculate priority weights
    # ---------------------------------------------------------

    weighted_tasks = []

    for task in tasks:

        original_hours = max(
            0.0,
            float(task.get("remaining_hours", 0))
        )

        importance = max(
            1,
            int(task.get("importance", 1))
        )

        priority_score = float(
            task.get(
                "priority_score",
                calculate_task_priority(task)
            )
        )

        # Importance has the strongest influence.
        # Priority score provides additional urgency.
        weight = (
            importance * 10
        ) + max(
            priority_score,
            0.0
        )

        weighted_tasks.append(
            {
                "task": task,
                "original_hours": original_hours,
                "weight": max(weight, 0.01)
            }
        )

    # ---------------------------------------------------------
    # Weighted allocation with task-hour caps
    # ---------------------------------------------------------

    allocations = {
        item["task"].get("name", ""): 0.0
        for item in weighted_tasks
    }

    remaining_available = available_hours

    active = [
        item
        for item in weighted_tasks
        if item["original_hours"] > 0
    ]

    while active and remaining_available > 0.01:

        total_weight = sum(
            item["weight"]
            for item in active
        )

        if total_weight <= 0:
            break

        next_active = []

        for item in active:

            name = item["task"].get(
                "name",
                ""
            )

            current = allocations[name]

            remaining_need = (
                item["original_hours"]
                - current
            )

            if remaining_need <= 0.01:
                continue

            share = (
                remaining_available
                * item["weight"]
                / total_weight
            )

            allocation = min(
                share,
                remaining_need
            )

            allocations[name] = round(
                current + allocation,
                4
            )

        allocated_total = sum(
            allocations.values()
        )

        new_remaining = max(
            0.0,
            available_hours - allocated_total
        )

        if (
            abs(
                new_remaining
                - remaining_available
            ) < 0.0001
        ):
            break

        remaining_available = new_remaining

        next_active = [
            item
            for item in active
            if (
                item["original_hours"]
                - allocations[
                    item["task"].get("name", "")
                ]
            ) > 0.01
        ]

        active = next_active

    # ---------------------------------------------------------
    # Build final result
    # ---------------------------------------------------------

    result = []

    for item in weighted_tasks:

        task = item["task"]

        name = task.get(
            "name",
            ""
        )

        original_hours = item[
            "original_hours"
        ]

        replanned_hours = round(
            min(
                original_hours,
                allocations.get(
                    name,
                    0.0
                )
            ),
            2
        )

        if replanned_hours >= original_hours - 0.01:
            replanned_hours = round(
                original_hours,
                2
            )
            action = "PRESERVE"

        elif replanned_hours > 0:
            action = "REDUCE"

        else:
            action = "DEFER"

        importance = int(
            task.get("importance", 1)
        )

        priority_score = float(
            task.get(
                "priority_score",
                calculate_task_priority(task)
            )
        )

        if action == "PRESERVE":
            reason = (
                "The task has sufficient priority and "
                "available time to preserve its full "
                "preparation."
            )
        elif action == "REDUCE":
            reason = (
                "Preparation was reduced according "
                "to task priority because available "
                "time is limited."
            )
        else:
            reason = (
                "The task was deferred because higher-"
                "priority work consumed the available time."
            )

        result.append(
            {
                "name": name,
                "action": action,
                "original_hours": round(
                    original_hours,
                    2
                ),
                "replanned_hours": replanned_hours,
                "importance": importance,
                "priority_score": round(
                    priority_score,
                    2
                ),
                "reason": reason
            }
        )

    return result

def generate_replan_schedule(
    replanned_tasks: list,
    daily_hours: float,
    days_remaining: int,
    daily_hours_by_day: dict | None = None
) -> dict:
    """
    Generate a schedule from replanned tasks.

    daily_hours:
        Default available hours per day.

    daily_hours_by_day:
        Optional dictionary such as:
        {
            "Day 1": 3,
            "Day 2": 1,
            "Day 3": 3,
            "Day 4": 3
        }

        This is used when availability changes on a
        specific day.
    """

    schedule = {}

    if days_remaining <= 0:
        return schedule

    remaining = {
        task["name"]: max(
            0.0,
            float(task.get("replanned_hours", 0))
        )
        for task in replanned_tasks
    }

    # Higher importance first.
    # If importance is equal, higher priority score wins.
    ordered_tasks = sorted(
        replanned_tasks,
        key=lambda task: (
            float(task.get("importance", 1)),
            float(task.get("priority_score", 0)),
            float(task.get("replanned_hours", 0))
        ),
        reverse=True
    )

    for day in range(1, days_remaining + 1):

        day_key = f"Day {day}"

        schedule[day_key] = []

        if daily_hours_by_day is not None:
            available_today = float(
                daily_hours_by_day.get(
                    day_key,
                    daily_hours
                )
            )
        else:
            available_today = float(daily_hours)

        available_today = max(
            0.0,
            available_today
        )

        for task in ordered_tasks:

            name = task["name"]

            remaining_hours = remaining.get(
                name,
                0.0
            )

            if remaining_hours <= 0.01:
                continue

            if available_today <= 0.01:
                break

            allocated = min(
                remaining_hours,
                available_today
            )

            schedule[day_key].append(
                {
                    "task": name,
                    "hours": round(
                        allocated,
                        2
                    ),
                    "action": task.get(
                        "action",
                        "PRESERVE"
                    ),
                    "importance": task.get(
                        "importance",
                        1
                    )
                }
            )

            remaining[name] = round(
                remaining_hours - allocated,
                2
            )

            available_today = round(
                available_today - allocated,
                2
            )

    return schedule

def calculate_replan_metrics(
    replanned_tasks: list
) -> tuple:

    required_hours = sum(
        float(
            task.get(
                "replanned_hours",
                0
            )
        )
        for task in replanned_tasks
    )

    unresolved_hours = sum(
        max(
            0.0,
            float(
                task.get(
                    "original_hours",
                    0
                )
            )
            -
            float(
                task.get(
                    "replanned_hours",
                    0
                )
            )
        )
        for task in replanned_tasks
    )

    return (
        round(required_hours, 2),
        round(unresolved_hours, 2)
    )

def calculate_simulated_available_hours(
    daily_hours: float,
    days_remaining: int
) -> float:

    if daily_hours < 0 or days_remaining < 0:
        return 0.0

    return round(
        daily_hours * days_remaining,
        2
    )


def calculate_simulated_shortage(
    required_hours: float,
    available_hours: float
) -> float:

    shortage = (
        required_hours
        - available_hours
    )

    return round(
        max(0.0, shortage),
        2
    )


def calculate_simulated_risk(
    required_hours: float,
    available_hours: float
) -> str:

    if available_hours <= 0:

        if required_hours > 0:
            return "CRITICAL"

        return "LOW"

    ratio = (
        required_hours
        / available_hours
    )

    if ratio > 1.2:
        return "CRITICAL"

    if ratio > 1:
        return "HIGH"

    if ratio > 0.8:
        return "MEDIUM"

    return "LOW"


def get_simulated_risk_reason(
    risk_level: str
) -> str:

    if risk_level == "LOW":

        return (
            "The simulated plan has enough available "
            "time to complete the required work."
        )

    if risk_level == "MEDIUM":

        return (
            "The simulated plan is feasible but has "
            "a limited time buffer."
        )

    if risk_level == "HIGH":

        return (
            "The simulated scenario creates a time "
            "shortage and requires replanning."
        )

    return (
        "The simulated scenario creates a severe "
        "time shortage and requires a rescue strategy."
    )


def apply_lost_time_simulation(
    constraints: dict,
    lost_hours: float,
    affected_day: int | None = None
) -> dict:
    """
    Simulate lost time.

    If affected_day is provided, only that day's
    availability is reduced.

    Example:

    Original:
        Day 1 = 3
        Day 2 = 3
        Day 3 = 3
        Day 4 = 3

    Lose 2 hours on Day 2:

        Day 1 = 3
        Day 2 = 1
        Day 3 = 3
        Day 4 = 3
    """

    simulated_constraints = constraints.copy()

    daily_hours = max(
        0.0,
        float(
            simulated_constraints.get(
                "daily_hours",
                0
            )
        )
    )

    days_remaining = max(
        0,
        int(
            simulated_constraints.get(
                "days_remaining",
                0
            )
        )
    )

    lost_hours = max(
        0.0,
        float(lost_hours)
    )

    daily_hours_by_day = {}

    for day in range(
        1,
        days_remaining + 1
    ):
        daily_hours_by_day[
            f"Day {day}"
        ] = daily_hours

    if (
        affected_day is not None
        and 1 <= affected_day <= days_remaining
    ):
        day_key = f"Day {affected_day}"

        daily_hours_by_day[day_key] = round(
            max(
                0.0,
                daily_hours_by_day[day_key]
                - lost_hours
            ),
            2
        )

    else:
        # If no specific day is known,
        # preserve the old total-time behavior.
        total_available = (
            daily_hours
            * days_remaining
        )

        total_available = max(
            0.0,
            total_available - lost_hours
        )

        if days_remaining > 0:
            average_available = (
                total_available
                / days_remaining
            )

            for day in range(
                1,
                days_remaining + 1
            ):
                daily_hours_by_day[
                    f"Day {day}"
                ] = round(
                    average_available,
                    2
                )

    total_available = round(
        sum(
            daily_hours_by_day.values()
        ),
        2
    )

    simulated_constraints[
        "daily_hours_by_day"
    ] = daily_hours_by_day

    simulated_constraints[
        "total_available_hours"
    ] = total_available

    return simulated_constraints

def apply_extra_time_simulation(
    constraints: dict,
    extra_hours: float
) -> dict:

    simulated_constraints = constraints.copy()

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

    total_available = (
        daily_hours
        * days_remaining
    )

    total_available += max(
        0.0,
        extra_hours
    )

    simulated_constraints[
        "total_available_hours"
    ] = round(
        total_available,
        2
    )

    return simulated_constraints


def apply_reduced_availability_simulation(
    constraints: dict,
    new_daily_hours: float
) -> dict:

    simulated_constraints = constraints.copy()

    simulated_constraints[
        "daily_hours"
    ] = max(
        0.0,
        new_daily_hours
    )

    return simulated_constraints


def apply_increased_availability_simulation(
    constraints: dict,
    new_daily_hours: float
) -> dict:

    simulated_constraints = constraints.copy()

    simulated_constraints[
        "daily_hours"
    ] = max(
        0.0,
        new_daily_hours
    )

    return simulated_constraints

def normalize_task_name(name: str) -> str:
    if not name:
        return ""

    name = str(name).lower().strip()
    name = re.sub(r"[^a-z0-9\s]", " ", name)
    name = re.sub(r"\s+", " ", name)

    return name.strip()


def task_names_match(
    actual_name: str,
    requested_name: str
) -> bool:
    actual = normalize_task_name(actual_name)
    requested = normalize_task_name(requested_name)

    if not actual or not requested:
        return False

    if actual == requested:
        return True

    if actual in requested or requested in actual:
        return True

    actual_tokens = set(actual.split())
    requested_tokens = set(requested.split())

    if len(requested_tokens) == 1:
        return requested in actual_tokens

    if len(actual_tokens) == 1:
        return actual in requested_tokens

    intersection = actual_tokens & requested_tokens

    return len(intersection) >= 2

def calculate_simulated_task_hours(
    tasks: list,
    simulation_change: dict,
    simulation_type: str
) -> list:

    simulated_tasks = []

    target_task = simulation_change.get("task")

    additional_hours = max(
        0.0,
        float(
            simulation_change.get(
                "hours",
                0
            )
        )
    )

    for task in tasks:

        task_copy = task.copy()

        task_name = task_copy.get(
            "name",
            ""
        )

        matched = task_names_match(
            task_name,
            target_task
        )

        if (
            simulation_type == "DELAYED_TASK"
            and matched
        ):

            original_hours = max(
                0.0,
                float(
                    task_copy.get(
                        "remaining_hours",
                        0
                    )
                )
            )

            task_copy["remaining_hours"] = round(
                original_hours + additional_hours,
                2
            )

        elif (
            simulation_type == "TASK_COMPLETED"
            and matched
        ):

            task_copy["remaining_hours"] = 0.0

        simulated_tasks.append(
            task_copy
        )

    return simulated_tasks