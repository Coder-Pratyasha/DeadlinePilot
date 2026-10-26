import { useState } from "react";

function UpdateSituation({ onClose }) {
  const [selected, setSelected] = useState("lost");
  const [hours, setHours] = useState(2);

  const options = [
    {
      id: "lost",
      icon: "◷",
      title: "I lost some time",
      description: "Something unexpected reduced my available time.",
    },
    {
      id: "longer",
      icon: "↗",
      title: "A task took longer",
      description: "The actual effort was higher than expected.",
    },
    {
      id: "completed",
      icon: "✓",
      title: "I completed a task",
      description: "Mark work as completed and update the plan.",
    },
    {
      id: "more",
      icon: "＋",
      title: "I have more time",
      description: "My available time has increased.",
    },
  ];

  return (
    <div
      className="fixed inset-0 z-[100] flex items-end justify-center bg-slate-900/20 p-0 backdrop-blur-sm sm:items-center sm:p-5"
      onClick={onClose}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        className="animate-modal glass-strong max-h-[94vh] w-full overflow-y-auto rounded-t-3xl p-5 shadow-2xl sm:max-w-xl sm:rounded-3xl sm:p-7"
      >
        {/* Header */}
        <div className="flex items-start justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-violet-50 text-violet-600">
                ◈
              </div>

              <div>
                <p className="text-[10px] font-semibold uppercase tracking-[0.18em] text-violet-500">
                  Update Reality
                </p>

                <h2 className="mt-1 text-lg font-semibold text-slate-900">
                  What changed?
                </h2>
              </div>
            </div>

            <p className="mt-3 text-sm leading-6 text-slate-500">
              Tell the agent what happened. It will reassess the plan and
              determine whether anything needs to change.
            </p>
          </div>

          <button
            onClick={onClose}
            className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl text-xl text-slate-400 transition hover:bg-slate-100 hover:text-slate-700"
          >
            ×
          </button>
        </div>

        {/* Options */}
        <div className="mt-6 grid gap-2.5">
          {options.map((option) => {
            const active = selected === option.id;

            return (
              <button
                key={option.id}
                onClick={() => setSelected(option.id)}
                className={`flex w-full items-start gap-3 rounded-2xl border p-3.5 text-left transition sm:p-4 ${
                  active
                    ? "border-violet-300 bg-violet-50/80 shadow-sm"
                    : "border-slate-200 bg-white/55 hover:border-violet-200 hover:bg-white/80"
                }`}
              >
                <div
                  className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-xl text-sm ${
                    active
                      ? "bg-violet-100 text-violet-600"
                      : "bg-slate-100 text-slate-500"
                  }`}
                >
                  {option.icon}
                </div>

                <div className="min-w-0 flex-1">
                  <p className="text-sm font-semibold text-slate-800">
                    {option.title}
                  </p>

                  <p className="mt-1 text-xs leading-5 text-slate-500">
                    {option.description}
                  </p>
                </div>

                <div
                  className={`mt-1 flex h-4 w-4 shrink-0 items-center justify-center rounded-full border ${
                    active
                      ? "border-violet-500 bg-violet-500"
                      : "border-slate-300 bg-white"
                  }`}
                >
                  {active && (
                    <div className="h-1.5 w-1.5 rounded-full bg-white" />
                  )}
                </div>
              </button>
            );
          })}
        </div>

        {/* Lost time input */}
        {selected === "lost" && (
          <div className="mt-5 rounded-2xl border border-violet-100 bg-violet-50/50 p-4">
            <label className="text-xs font-medium text-slate-600">
              How much time did you lose?
            </label>

            <div className="mt-3 flex items-center gap-3">
              <input
                type="number"
                min="0.5"
                step="0.5"
                value={hours}
                onChange={(e) => setHours(e.target.value)}
                className="h-11 w-full rounded-xl border border-slate-200 bg-white px-3 text-sm text-slate-800 outline-none transition focus:border-violet-300 focus:ring-4 focus:ring-violet-100 sm:w-32"
              />

              <span className="text-sm text-slate-500">
                hours
              </span>
            </div>
          </div>
        )}

        {/* Agent message */}
        <div className="mt-5 flex gap-3 rounded-2xl border border-slate-200 bg-white/60 p-4">
          <div className="agent-pulse mt-0.5 text-violet-500">◈</div>

          <div>
            <p className="text-sm font-semibold text-slate-800">
              Agent will reassess
            </p>

            <p className="mt-1 text-xs leading-5 text-slate-500">
              Your update will be evaluated against the deadline, remaining
              workload, priorities and available time.
            </p>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-6 flex flex-col-reverse gap-3 sm:flex-row sm:justify-end">
          <button
            onClick={onClose}
            className="min-h-11 rounded-xl border border-slate-200 bg-white px-5 text-sm font-medium text-slate-600 transition hover:bg-slate-50"
          >
            Cancel
          </button>

          <button className="min-h-11 rounded-xl bg-violet-600 px-5 text-sm font-semibold text-white shadow-sm transition hover:bg-violet-700 hover:shadow-md">
            Update Situation
          </button>
        </div>
      </div>
    </div>
  );
}

export default UpdateSituation;