import GlassCard from "../common/GlassCard";

const tasks = [
  {
    title: "Dataset preprocessing",
    hours: 3,
    progress: 100,
    priority: 5,
    status: "Completed",
  },
  {
    title: "Feature engineering",
    hours: 4,
    progress: 100,
    priority: 5,
    status: "Completed",
  },
  {
    title: "Model training and tuning",
    hours: 5,
    progress: 35,
    priority: 5,
    status: "In progress",
  },
  {
    title: "Model evaluation",
    hours: 2,
    progress: 0,
    priority: 3,
    status: "Pending",
  },
  {
    title: "Documentation and report",
    hours: 4,
    progress: 0,
    priority: 3,
    status: "Pending",
  },
  {
    title: "Final testing and presentation",
    hours: 3,
    progress: 0,
    priority: 5,
    status: "Pending",
  },
];

function TaskList() {
  return (
    <GlassCard className="p-5 sm:p-6">

      <div className="flex items-center justify-between">

        <div>
          <p className="text-[10px] font-semibold uppercase tracking-[0.18em] text-violet-500">
            Work Breakdown
          </p>

          <h2 className="mt-1 text-sm font-semibold text-slate-800">
            Tasks
          </h2>
        </div>

        <span className="text-[10px] text-slate-400">
          6 tasks
        </span>

      </div>

      <div className="mt-5 space-y-2">

        {tasks.map((task, index) => (
          <div
            key={index}
            className="rounded-2xl border border-slate-200/70 bg-white/45 p-4 transition hover:bg-white/70"
          >

            <div className="flex items-start gap-3">

              <div
                className={`mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full border ${
                  task.progress === 100
                    ? "border-emerald-200 bg-emerald-50 text-emerald-600"
                    : task.progress > 0
                      ? "border-violet-200 bg-violet-50 text-violet-600"
                      : "border-slate-200 bg-white text-slate-300"
                }`}
              >
                {task.progress === 100 ? "✓" : index + 1}
              </div>

              <div className="min-w-0 flex-1">

                <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">

                  <div>
                    <p className="text-xs font-medium text-slate-700">
                      {task.title}
                    </p>

                    <p className="mt-1 text-[10px] text-slate-400">
                      {task.hours} hours · Priority {task.priority}
                    </p>
                  </div>

                  <span
                    className={`w-fit rounded-full px-2 py-1 text-[9px] font-medium ${
                      task.status === "Completed"
                        ? "bg-emerald-50 text-emerald-600"
                        : task.status === "In progress"
                          ? "bg-violet-50 text-violet-600"
                          : "bg-slate-100 text-slate-500"
                    }`}
                  >
                    {task.status}
                  </span>

                </div>

                <div className="mt-3 h-1.5 overflow-hidden rounded-full bg-slate-100">

                  <div
                    className={`h-full rounded-full ${
                      task.progress === 100
                        ? "bg-emerald-500"
                        : "bg-violet-500"
                    }`}
                    style={{
                      width: `${task.progress}%`,
                    }}
                  />

                </div>

              </div>

            </div>

          </div>
        ))}

      </div>

    </GlassCard>
  );
}

export default TaskList;