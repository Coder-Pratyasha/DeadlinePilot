import GlassCard from "../common/GlassCard";

function AgentInsight() {
  return (
    <GlassCard className="ai-glow overflow-hidden p-5 sm:p-6">

      <div className="flex items-start gap-4">

        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl border border-violet-200 bg-violet-50 text-violet-600">
          ◈
        </div>

        <div className="min-w-0">

          <p className="text-[10px] font-semibold uppercase tracking-[0.18em] text-violet-500">
            Agent Decision
          </p>

          <h2 className="mt-1 text-base font-semibold text-slate-900">
            Your plan is slightly over capacity.
          </h2>

        </div>

      </div>

      <p className="mt-5 text-sm leading-7 text-slate-500">
        You have 20 available hours remaining, while the current task
        set requires approximately 21 hours. This creates a small
        capacity shortage before the deadline.
      </p>

      <div className="mt-5 grid gap-3 sm:grid-cols-2">

        <div className="rounded-2xl border border-amber-100 bg-amber-50/70 p-4">

          <p className="text-[10px] font-semibold uppercase tracking-wide text-amber-600">
            Situation
          </p>

          <p className="mt-2 text-xs leading-5 text-amber-700">
            Workload is slightly higher than available capacity.
          </p>

        </div>

        <div className="rounded-2xl border border-violet-100 bg-violet-50/70 p-4">

          <p className="text-[10px] font-semibold uppercase tracking-wide text-violet-600">
            Recommendation
          </p>

          <p className="mt-2 text-xs leading-5 text-violet-700">
            Protect high-priority work and reduce lower-priority load.
          </p>

        </div>

      </div>

      <div className="mt-5 flex items-center gap-2 text-[10px] text-slate-400">
        <span className="h-1.5 w-1.5 rounded-full bg-violet-500 animate-pulse-soft" />
        Decision generated from current plan state
      </div>

    </GlassCard>
  );
}

export default AgentInsight;