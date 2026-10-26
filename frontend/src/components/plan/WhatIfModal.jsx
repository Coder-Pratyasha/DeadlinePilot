function WhatIfModal({ onClose }) {
  return (
    <div
      className="fixed inset-0 z-[100] flex items-end justify-center bg-slate-900/20 p-0 backdrop-blur-sm sm:items-center sm:p-5"
      onClick={onClose}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        className="animate-modal glass-strong max-h-[92vh] w-full overflow-y-auto rounded-t-3xl p-5 shadow-2xl sm:max-w-2xl sm:rounded-3xl sm:p-7"
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
                  Decision Simulation
                </p>

                <h2 className="mt-1 text-lg font-semibold text-slate-900">
                  What if something changes?
                </h2>
              </div>
            </div>

            <p className="mt-3 max-w-lg text-sm leading-6 text-slate-500">
              Explore how the agent would adapt the plan without changing your
              actual plan.
            </p>
          </div>

          <button
            onClick={onClose}
            className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl text-xl text-slate-400 transition hover:bg-slate-100 hover:text-slate-700"
          >
            ×
          </button>
        </div>

        {/* Simulation */}
        <div className="mt-6 rounded-2xl border border-violet-100 bg-violet-50/60 p-4 sm:p-5">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p className="text-xs font-medium text-slate-500">
                Scenario
              </p>

              <p className="mt-1 text-sm font-semibold text-slate-900">
                Lose another 2 hours
              </p>
            </div>

            <div className="rounded-xl bg-white px-3 py-2 text-center shadow-sm">
              <p className="text-[10px] text-slate-400">Risk</p>
              <p className="text-sm font-semibold text-red-500">HIGH</p>
            </div>
          </div>
        </div>

        {/* Comparison */}
        <div className="mt-5 grid gap-4 sm:grid-cols-2">
          <ComparisonCard
            title="Current Plan"
            hours="20h"
            shortage="1h"
            risk="High"
          />

          <ComparisonCard
            title="Simulated Plan"
            hours="18h"
            shortage="3h"
            risk="High"
            simulated
          />
        </div>

        {/* Message */}
        <div className="mt-5 rounded-2xl border border-slate-200 bg-white/70 p-4">
          <div className="flex gap-3">
            <div className="mt-0.5 text-violet-500">◈</div>

            <div>
              <p className="text-sm font-semibold text-slate-800">
                Agent Decision
              </p>

              <p className="mt-1 text-sm leading-6 text-slate-500">
                The agent would preserve high-priority work while compressing
                lower-priority activities to absorb the additional lost time.
              </p>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-6 flex flex-col-reverse gap-3 sm:flex-row sm:justify-end">
          <button
            onClick={onClose}
            className="min-h-11 rounded-xl border border-slate-200 bg-white px-5 text-sm font-medium text-slate-600 transition hover:bg-slate-50"
          >
            Close
          </button>

          <div className="flex min-h-11 items-center justify-center rounded-xl border border-violet-200 bg-violet-50 px-5 text-sm font-medium text-violet-700">
            Simulation only
          </div>
        </div>
      </div>
    </div>
  );
}

function ComparisonCard({
  title,
  hours,
  shortage,
  risk,
  simulated = false,
}) {
  return (
    <div
      className={`rounded-2xl border p-4 ${
        simulated
          ? "border-violet-200 bg-violet-50/40"
          : "border-slate-200 bg-white/60"
      }`}
    >
      <div className="flex items-center justify-between gap-2">
        <p className="text-xs font-semibold text-slate-600">{title}</p>

        {simulated && (
          <span className="rounded-full bg-violet-100 px-2 py-1 text-[9px] font-semibold uppercase tracking-wide text-violet-600">
            Simulated
          </span>
        )}
      </div>

      <div className="mt-4 grid grid-cols-3 gap-2">
        <Metric label="Available" value={hours} />
        <Metric label="Shortage" value={shortage} />
        <Metric label="Risk" value={risk} />
      </div>
    </div>
  );
}

function Metric({ label, value }) {
  return (
    <div className="rounded-xl bg-white/70 p-2.5 text-center">
      <p className="text-[9px] uppercase tracking-wide text-slate-400">
        {label}
      </p>

      <p className="mt-1 text-sm font-semibold text-slate-800">
        {value}
      </p>
    </div>
  );
}

export default WhatIfModal;