import { Link } from "react-router-dom";

import GlassCard from "../common/GlassCard";
import RiskBadge from "../common/RiskBadge";

function PlanHeader() {
  return (
    <GlassCard className="p-5 sm:p-6">

      <div className="flex flex-col gap-5 lg:flex-row lg:items-center lg:justify-between">

        <div className="flex items-start gap-4">

          <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-2xl border border-violet-200 bg-violet-50 text-violet-600">
            ◈
          </div>

          <div>

            <div className="flex flex-wrap items-center gap-2">
              <p className="text-[10px] font-semibold uppercase tracking-[0.18em] text-violet-500">
                Active Plan
              </p>

              <RiskBadge risk="HIGH" />
            </div>

            <h1 className="mt-2 text-xl font-semibold tracking-tight text-slate-900 sm:text-2xl">
              AI/ML Final Project
            </h1>

            <p className="mt-1 text-xs text-slate-400">
              Complete final-year AI/ML project by October 30, 2026
            </p>

          </div>

        </div>

        <div className="flex flex-wrap items-center gap-3">

          <div className="rounded-xl border border-slate-200 bg-white/60 px-4 py-2.5">
            <p className="text-[10px] text-slate-400">
              Deadline
            </p>

            <p className="mt-0.5 text-xs font-semibold text-slate-700">
              Oct 30, 2026
            </p>
          </div>

          <div className="rounded-xl border border-amber-200 bg-amber-50 px-4 py-2.5">
            <p className="text-[10px] text-amber-500">
              Time left
            </p>

            <p className="mt-0.5 text-xs font-semibold text-amber-700">
              4 days
            </p>
          </div>

        </div>

      </div>

      <div className="mt-5 flex items-center justify-between border-t border-slate-200/70 pt-4">

        <Link
          to="/plans"
          className="text-xs font-medium text-slate-400 hover:text-violet-600"
        >
          ← All plans
        </Link>

        <span className="text-[10px] text-slate-400">
          Last updated · just now
        </span>

      </div>

    </GlassCard>
  );
}

export default PlanHeader;