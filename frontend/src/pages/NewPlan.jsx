import { useState } from "react";
import { Link } from "react-router-dom";

import GlassCard from "../components/common/GlassCard";

function NewPlan() {
  const [goal, setGoal] = useState("");
  const [deadline, setDeadline] = useState("");
  const [hoursPerDay, setHoursPerDay] = useState(4);

  const [tasks, setTasks] = useState([
    {
      id: 1,
      title: "",
      hours: "",
      priority: "5",
    },
  ]);

  const addTask = () => {
    setTasks((prev) => [
      ...prev,
      {
        id: Date.now(),
        title: "",
        hours: "",
        priority: "3",
      },
    ]);
  };

  const removeTask = (id) => {
    if (tasks.length === 1) return;

    setTasks((prev) => prev.filter((task) => task.id !== id));
  };

  const updateTask = (id, field, value) => {
    setTasks((prev) =>
      prev.map((task) =>
        task.id === id
          ? {
              ...task,
              [field]: value,
            }
          : task
      )
    );
  };

  return (
    <div className="space-y-5 pb-8 sm:space-y-6">
      {/* Header */}
      <div>
        <Link
          to="/plans"
          className="inline-flex items-center gap-2 text-xs font-medium text-slate-500 transition hover:text-violet-600"
        >
          ← Back to My Plans
        </Link>

        <div className="mt-5">
          <p className="text-xs font-medium text-violet-600">
            Create a decision plan
          </p>

          <h1 className="mt-1 text-2xl font-semibold tracking-tight text-slate-900 sm:text-3xl">
            Start with the outcome.
          </h1>

          <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-500">
            Give the agent your goal, deadline, tasks and available time. It
            will determine how the work should be organized.
          </p>
        </div>
      </div>

      {/* Main */}
      <div className="grid gap-5 xl:grid-cols-[minmax(0,1fr)_360px]">
        {/* Form */}
        <GlassCard className="min-w-0 p-5 sm:p-6">
          {/* Goal */}
          <section>
            <label className="text-sm font-semibold text-slate-800">
              What are you trying to accomplish?
            </label>

            <p className="mt-1 text-xs text-slate-400">
              Describe the final outcome clearly.
            </p>

            <textarea
              value={goal}
              onChange={(e) => setGoal(e.target.value)}
              placeholder="Example: Complete my final-year AI/ML project..."
              rows={4}
              className="mt-3 w-full rounded-2xl border border-slate-200 bg-white/65 p-4 text-sm leading-6 text-slate-800 outline-none transition placeholder:text-slate-400 focus:border-violet-300 focus:ring-4 focus:ring-violet-100"
            />
          </section>

          {/* Basic constraints */}
          <section className="mt-7">
            <div className="grid gap-4 sm:grid-cols-2">
              <div>
                <label className="text-sm font-semibold text-slate-800">
                  Deadline
                </label>

                <input
                  type="date"
                  value={deadline}
                  onChange={(e) => setDeadline(e.target.value)}
                  className="mt-2 h-11 w-full rounded-xl border border-slate-200 bg-white/65 px-3 text-sm text-slate-700 outline-none transition focus:border-violet-300 focus:ring-4 focus:ring-violet-100"
                />
              </div>

              <div>
                <label className="text-sm font-semibold text-slate-800">
                  Available hours / day
                </label>

                <input
                  type="number"
                  min="1"
                  max="24"
                  value={hoursPerDay}
                  onChange={(e) => setHoursPerDay(e.target.value)}
                  className="mt-2 h-11 w-full rounded-xl border border-slate-200 bg-white/65 px-3 text-sm text-slate-700 outline-none transition focus:border-violet-300 focus:ring-4 focus:ring-violet-100"
                />
              </div>
            </div>
          </section>

          {/* Tasks */}
          <section className="mt-7">
            <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
              <div>
                <h2 className="text-sm font-semibold text-slate-800">
                  Tasks
                </h2>

                <p className="mt-1 text-xs text-slate-400">
                  Break the goal into concrete pieces of work.
                </p>
              </div>

              <button
                type="button"
                onClick={addTask}
                className="inline-flex min-h-10 items-center justify-center rounded-xl border border-violet-200 bg-violet-50 px-3 text-xs font-semibold text-violet-700 transition hover:bg-violet-100"
              >
                + Add Task
              </button>
            </div>

            <div className="mt-4 space-y-3">
              {tasks.map((task, index) => (
                <div
                  key={task.id}
                  className="rounded-2xl border border-slate-200 bg-white/50 p-4"
                >
                  <div className="mb-3 flex items-center justify-between">
                    <span className="text-[10px] font-semibold uppercase tracking-[0.16em] text-slate-400">
                      Task {index + 1}
                    </span>

                    {tasks.length > 1 && (
                      <button
                        type="button"
                        onClick={() => removeTask(task.id)}
                        className="text-xs font-medium text-slate-400 transition hover:text-red-500"
                      >
                        Remove
                      </button>
                    )}
                  </div>

                  <div className="grid gap-3 sm:grid-cols-[minmax(0,1fr)_110px_130px]">
                    <div>
                      <label className="text-[10px] font-medium text-slate-400">
                        Task title
                      </label>

                      <input
                        type="text"
                        value={task.title}
                        onChange={(e) =>
                          updateTask(task.id, "title", e.target.value)
                        }
                        placeholder="e.g. Model training"
                        className="mt-1 h-11 w-full rounded-xl border border-slate-200 bg-white/70 px-3 text-sm outline-none transition placeholder:text-slate-400 focus:border-violet-300 focus:ring-4 focus:ring-violet-100"
                      />
                    </div>

                    <div>
                      <label className="text-[10px] font-medium text-slate-400">
                        Hours
                      </label>

                      <input
                        type="number"
                        min="0.5"
                        step="0.5"
                        value={task.hours}
                        onChange={(e) =>
                          updateTask(task.id, "hours", e.target.value)
                        }
                        placeholder="4"
                        className="mt-1 h-11 w-full rounded-xl border border-slate-200 bg-white/70 px-3 text-sm outline-none transition placeholder:text-slate-400 focus:border-violet-300 focus:ring-4 focus:ring-violet-100"
                      />
                    </div>

                    <div>
                      <label className="text-[10px] font-medium text-slate-400">
                        Priority
                      </label>

                      <select
                        value={task.priority}
                        onChange={(e) =>
                          updateTask(task.id, "priority", e.target.value)
                        }
                        className="mt-1 h-11 w-full rounded-xl border border-slate-200 bg-white/70 px-3 text-sm outline-none transition focus:border-violet-300 focus:ring-4 focus:ring-violet-100"
                      >
                        <option value="5">Critical</option>
                        <option value="4">High</option>
                        <option value="3">Medium</option>
                        <option value="2">Low</option>
                        <option value="1">Optional</option>
                      </select>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </section>

          {/* Submit */}
          <div className="mt-7 flex flex-col-reverse gap-3 border-t border-slate-100 pt-5 sm:flex-row sm:justify-end">
            <Link
              to="/plans"
              className="inline-flex min-h-11 items-center justify-center rounded-xl border border-slate-200 bg-white px-5 text-sm font-medium text-slate-600 transition hover:bg-slate-50"
            >
              Cancel
            </Link>

            <button
              type="button"
              className="min-h-11 rounded-xl bg-violet-600 px-5 text-sm font-semibold text-white shadow-sm transition hover:bg-violet-700 hover:shadow-md"
            >
              Create Plan
            </button>
          </div>
        </GlassCard>

        {/* Agent Preview */}
        <div className="min-w-0">
          <GlassCard
            strong
            className="ai-glow sticky top-5 p-5 sm:p-6"
          >
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-violet-50 text-violet-600">
                ◈
              </div>

              <div>
                <p className="text-[10px] font-semibold uppercase tracking-[0.18em] text-violet-500">
                  Agent Preview
                </p>

                <h2 className="mt-1 text-base font-semibold text-slate-900">
                  What happens next?
                </h2>
              </div>
            </div>

            <div className="mt-6 space-y-5">
              <PreviewStep
                number="01"
                title="Understand"
                text="The agent analyzes your goal, deadline and constraints."
              />

              <PreviewStep
                number="02"
                title="Prioritize"
                text="Tasks are evaluated based on effort and importance."
              />

              <PreviewStep
                number="03"
                title="Plan"
                text="A schedule is generated around your available time."
              />

              <PreviewStep
                number="04"
                title="Adapt"
                text="If reality changes, the agent can reassess and replan."
                last
              />
            </div>

            <div className="mt-6 rounded-2xl border border-violet-100 bg-violet-50/55 p-4">
              <p className="text-xs font-semibold text-violet-700">
                ◈ The plan is not static.
              </p>

              <p className="mt-1 text-xs leading-5 text-slate-500">
                DeadlinePilot is designed to continuously adapt your plan as
                your situation changes.
              </p>
            </div>
          </GlassCard>
        </div>
      </div>
    </div>
  );
}

function PreviewStep({ number, title, text, last = false }) {
  return (
    <div className="relative flex gap-3">
      {!last && (
        <div className="absolute left-[15px] top-8 h-[calc(100%+12px)] w-px bg-violet-100" />
      )}

      <div className="relative z-10 flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-violet-50 text-[9px] font-semibold text-violet-600">
        {number}
      </div>

      <div className="min-w-0">
        <p className="text-xs font-semibold text-slate-800">
          {title}
        </p>

        <p className="mt-1 text-xs leading-5 text-slate-500">
          {text}
        </p>
      </div>
    </div>
  );
}

export default NewPlan;