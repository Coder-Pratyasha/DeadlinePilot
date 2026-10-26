import GlassCard from "../common/GlassCard";

function PlanHealth() {
  return (
    <GlassCard className="p-5 sm:p-6">

      <div className="flex items-center justify-between">
        <div>
          <p className="text-[10px] font-semibold uppercase tracking-[0.18em] text-violet-500">
            Plan Health
          </p>

          <p className="mt-1 text-sm font-semibold text-slate-800">
            Current capacity
          </p>
        </div>

        <span className="rounded-full bg-red-50 px-2.5 py-1 text-[10px] font-semibold text-red-500">
          HIGH RISK
        </span>
      </div>

      <div className="mt-6 grid grid-cols-2 gap-3 lg:grid-cols-4">

        <Metric
          label="Progress"
          value="62%"
        />

        <Metric
          label="Required"
          value="21h"
        />

        <Metric
          label="Available"
          value="20h"
        />

        <Metric
          label="Shortage"
          value="1h"
          danger
        />

      </div>

      <div className="mt-6">

        <div className="flex justify-between text-[10px]">
          <span className="text-slate-400">
            Progress
          </span>

          <span className="font-medium text-slate-600">
            62%
          </span>
        </div>

        <div className="mt-2 h-2 overflow-hidden rounded-full bg-slate-100">
          <div
            className="h-full rounded-full bg-violet-500"
            style={{ width: "62%" }}
          />
        </div>

      </div>

    </GlassCard>
  );
}

function Metric({
  label,
  value,
  danger = false,
}) {
  return (
    <div className="rounded-2xl bg-slate-50/80 p-3.5">

      <p className="text-[10px] text-slate-400">
        {label}
      </p>

      <p
        className={`mt-1 text-lg font-semibold ${
          danger ? "text-red-500" : "text-slate-800"
        }`}
      >
        {value}
      </p>

    </div>
  );
}

export default PlanHealth;