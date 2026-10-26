import { useState } from "react";
import { Link } from "react-router-dom";

import PlanHeader from "../components/plan/PlanHeader";
import PlanHealth from "../components/plan/PlanHealth";
import AgentInsight from "../components/plan/AgentInsight";
import TaskList from "../components/plan/TaskList";
import Schedule from "../components/plan/Schedule";
import UpdateSituation from "../components/plan/UpdateSituation";
import WhatIfModal from "../components/plan/WhatIfModal";
import ActivityTimeline from "../components/plan/ActivityTimeline";

function PlanDetails() {
  const [showUpdate, setShowUpdate] = useState(false);
  const [showWhatIf, setShowWhatIf] = useState(false);

  return (
    <div className="space-y-5 pb-8 sm:space-y-6">
      {/* Back navigation */}
      <div>
        <Link
          to="/plans"
          className="inline-flex items-center gap-2 text-xs font-medium text-slate-500 transition hover:text-violet-600"
        >
          <span>←</span>
          Back to My Plans
        </Link>
      </div>

      {/* Plan header */}
      <PlanHeader />

      {/* Plan health */}
      <PlanHealth />

      {/* Main command center */}
      <div className="grid gap-5 xl:grid-cols-[minmax(0,1.4fr)_minmax(320px,0.65fr)]">
        {/* Left */}
        <div className="min-w-0 space-y-5">
          <Schedule />
          <TaskList />
        </div>

        {/* Right */}
        <div className="min-w-0 space-y-5">
          <AgentInsight />

          {/* Decision actions */}
          <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-1">
            <button
              type="button"
              onClick={() => setShowUpdate(true)}
              className="group min-h-[120px] rounded-2xl border border-slate-200 bg-white/65 p-5 text-left shadow-sm transition duration-200 hover:-translate-y-0.5 hover:border-violet-200 hover:bg-white hover:shadow-lg"
            >
              <div className="flex items-start justify-between">
                <div className="flex h-10 w-10 items-center justify-center rounded-xl border border-violet-100 bg-violet-50 text-violet-600">
                  ↻
                </div>

                <span className="text-slate-300 transition group-hover:text-violet-400">
                  →
                </span>
              </div>

              <p className="mt-4 text-sm font-semibold text-slate-900">
                Update Situation
              </p>

              <p className="mt-1 text-xs leading-5 text-slate-500">
                Something changed? Tell the agent what happened.
              </p>
            </button>

            <button
              type="button"
              onClick={() => setShowWhatIf(true)}
              className="group min-h-[120px] rounded-2xl border border-slate-200 bg-white/65 p-5 text-left shadow-sm transition duration-200 hover:-translate-y-0.5 hover:border-violet-200 hover:bg-white hover:shadow-lg"
            >
              <div className="flex items-start justify-between">
                <div className="flex h-10 w-10 items-center justify-center rounded-xl border border-violet-100 bg-violet-50 text-violet-600">
                  ◇
                </div>

                <span className="text-slate-300 transition group-hover:text-violet-400">
                  →
                </span>
              </div>

              <p className="mt-4 text-sm font-semibold text-slate-900">
                What If?
              </p>

              <p className="mt-1 text-xs leading-5 text-slate-500">
                Simulate a change before actually changing your plan.
              </p>
            </button>
          </div>

          {/* Agent status */}
          <div className="glass rounded-2xl p-4 sm:p-5">
            <div className="flex items-start gap-3">
              <div className="agent-pulse mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-violet-50 text-sm text-violet-600">
                ◈
              </div>

              <div className="min-w-0">
                <div className="flex flex-wrap items-center gap-2">
                  <p className="text-sm font-semibold text-slate-800">
                    Agent monitoring
                  </p>

                  <span className="rounded-full border border-emerald-200 bg-emerald-50 px-2 py-0.5 text-[9px] font-semibold uppercase tracking-wide text-emerald-600">
                    Active
                  </span>
                </div>

                <p className="mt-1 text-xs leading-5 text-slate-500">
                  The decision engine is watching your available time,
                  workload and deadline.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Activity */}
      <ActivityTimeline />

      {/* Modals */}
      {showUpdate && (
        <UpdateSituation onClose={() => setShowUpdate(false)} />
      )}

      {showWhatIf && (
        <WhatIfModal onClose={() => setShowWhatIf(false)} />
      )}
    </div>
  );
}

export default PlanDetails;