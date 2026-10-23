from app.agent import agent


def main():

    user_input = """
    I have an interview on Friday.
    I need to prepare DSA, DBMS, OS and CN.
    Each subject needs 6 hours.
    I have 3 hours available every day for 4 days.
    """

    initial_state = {
        "user_input": user_input
    }

    result = agent.invoke(
        initial_state
    )

    print("\n================================")
    print("GOAL")
    print("================================")

    print(
        result.get("goal")
    )

    print("\n================================")
    print("ORIGINAL TASKS")
    print("================================")

    for task in result.get(
        "tasks",
        []
    ):

        print(task)

    print("\n================================")
    print("PLAN METRICS")
    print("================================")

    print(
        "Required hours:",
        result.get(
            "required_hours"
        )
    )

    print(
        "Available hours:",
        result.get(
            "available_hours"
        )
    )

    print(
        "Shortage:",
        result.get(
            "shortage_hours"
        )
    )

    print(
        "Risk:",
        result.get(
            "risk_level"
        )
    )

    print(
        "Decision:",
        result.get(
            "decision"
        )
    )

    print("\n================================")
    print("BASIC RESCUE SCHEDULE")
    print("================================")

    rescue_schedule = result.get(
        "rescue_schedule",
        {}
    )

    for day, tasks in rescue_schedule.items():

        print(f"\n{day}")

        for task in tasks:

            print(
                f"  {task['task']} "
                f"→ {task['hours']} hours"
            )

    print("\n================================")
    print("ADVANCED REPLANNING")
    print("================================")

    for task in result.get(
        "replanned_tasks",
        []
    ):

        print(
            f"\n{task['name']}"
        )

        print(
            "Action:",
            task["action"]
        )

        print(
            "Original hours:",
            task["original_hours"]
        )

        print(
            "Replanned hours:",
            task["replanned_hours"]
        )

        print(
            "Reason:",
            task["reason"]
        )

    print("\n================================")
    print("PRESERVED TASKS")
    print("================================")

    for task in result.get(
        "preserved_tasks",
        []
    ):

        print(
            task["name"],
            "→",
            task["replanned_hours"],
            "hours"
        )

    print("\n================================")
    print("REDUCED TASKS")
    print("================================")

    for task in result.get(
        "reduced_tasks",
        []
    ):

        print(
            task["name"],
            ":",
            task["original_hours"],
            "→",
            task["replanned_hours"],
            "hours"
        )

    print("\n================================")
    print("DEFERRED TASKS")
    print("================================")

    for task in result.get(
        "deferred_tasks",
        []
    ):

        print(
            task["name"],
            "→ DEFERRED"
        )

    print("\n================================")
    print("REPLANNED SCHEDULE")
    print("================================")

    replan_schedule = result.get(
        "replan_schedule",
        {}
    )

    for day, tasks in replan_schedule.items():

        print(f"\n{day}")

        for task in tasks:

            print(
                f"  {task['task']} "
                f"→ {task['hours']} hours "
                f"({task['action']})"
            )

    print("\n================================")
    print("REPLAN METRICS")
    print("================================")

    print(
        "Replanned required hours:",
        result.get(
            "replan_required_hours"
        )
    )

    print(
        "Remaining unresolved hours:",
        result.get(
            "replan_unresolved_hours"
        )
    )

    print(
        "\nReason:",
        result.get(
            "replan_reason"
        )
    )


if __name__ == "__main__":
    main()