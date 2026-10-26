import { Link } from "react-router-dom";

import GlassCard from "../components/common/GlassCard";
import RiskBadge from "../components/common/RiskBadge";

function Dashboard() {
  return (
    <div className="space-y-5 pb-8 sm:space-y-6">
      {/* Welcome */}
      <section>
        <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
          <div className="min-w-0">
            <p className="text-xs font-medium text-violet-600">
              Your decision workspace
            </p>

            <h1 className="mt-1 text-2xl font-semibold tracking-tight text-slate-900 sm:text-3xl">
              What needs your attention?
            </h1>

            <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-500">
              DeadlinePilot continuously evaluates your plans and helps you
              adapt when reality changes.
            </p>
          </div>

          <Link
            to="/new-plan"
            className="inline-flex min-h-11 shrink-0 items-center justify-center rounded-xl bg-violet-600 px-4 text-sm font-semibold text-white shadow-sm transition hover:bg-violet-700 hover:shadow-md"
          >
            + New Plan
          </Link>
        </div>
      </section>

      {/* Attention banner */}
      <GlassCard
        strong
        className="overflow-hidden border-red-100 bg-red-50/45 p-4 sm:p-5"
      >
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex min-w-0 items-start gap-3">
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-red-100 text-red-500">
              !
            </div>

            <div className="min-w-0">
              <div className="flex flex-wrap items-center gap-2">
                <p className="text-sm font-semibold text-slate-900">
                  AI/ML Final Project needs attention
                </p>

                <RiskBadge risk="HIGH" />
              </div>

              <p className="mt-1 text-xs leading-5 text-slate-500">
                You currently have 20h available for 21h of estimated work.
                The agent recommends recovering at least 1 hour.
              </p>
            </div>
          </div>

          <Link
            to="/plans/1"
            className="inline-flex min-h-10 shrink-0 items-center justify-center rounded-xl border border-red-200 bg-white/70 px-4 text-xs font-semibold text-red-600 transition hover:bg-white"
          >
            Review Plan →
          </Link>
        </div>
      </GlassCard>

      {/* Stats */}
      <div className="grid grid-cols-2 gap-3 sm:grid-cols-2 lg:grid-cols-4 lg:gap-4">
        <StatCard
          label="Active Plans"
          value="3"
          caption="Currently running"
        />

        <StatCard
          label="Hours Available"
          value="20h"
          caption="Across active plans"
        />

        <StatCard
          label="At Risk"
          value="1"
          caption="Needs attention"
          danger
        />

        <StatCard
          label="Completed"
          value="12"
          caption="Tasks completed"
        />
      </div>

      {/* Main section */}
      <div className="grid gap-5 xl:grid-cols-[minmax(0,1.35fr)_minmax(320px,0.65fr)]">
        {/* Current plan */}
        <GlassCard className="min-w-0 p-5 sm:p-6">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
            <div className="min-w-0">
              <p className="text-[10px] font-semibold uppercase tracking-[0.18em] text-violet-500">
                Current Plan
              </p>

              <h2 className="mt-2 truncate text-lg font-semibold text-slate-900">
                AI/ML Final Project
              </h2>

              <p className="mt-1 text-xs text-slate-500">
                Deadline · October 30, 2026
              </p>
            </div>

            <RiskBadge risk="HIGH" size="md" />
          </div>

          {/* Progress */}
          <div className="mt-7">
            <div className="flex items-center justify-between">
              <span className="text-xs font-medium text-slate-500">
                Overall progress
              </span>

              <span className="text-sm font-semibold text-slate-800">
                62%
              </span>
            </div>

            <div className="mt-2 h-2 overflow-hidden rounded-full bg-slate-100">
              <div
                className="h-full rounded-full bg-violet-500 transition-all duration-500"
                style={{ width: "62%" }}
              />
            </div>
          </div>

          {/* Metrics */}
          <div className="mt-6 grid grid-cols-3 gap-2 sm:gap-3">
            <MiniMetric label="Required" value="21h" />
            <MiniMetric label="Available" value="20h" />
            <MiniMetric label="Shortage" value="1h" danger />
          </div>

          <Link
            to="/plans/1"
            className="mt-6 flex min-h-11 w-full items-center justify-center rounded-xl border border-slate-200 bg-white/70 text-sm font-medium text-slate-600 transition hover:border-violet-200 hover:bg-violet-50 hover:text-violet-700"
          >
            Open Plan
          </Link>
        </GlassCard>

        {/* Agent insight */}
        <GlassCard
          strong
          className="min-w-0 ai-glow p-5 sm:p-6"
        >
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-violet-50 text-violet-600">
              ◈
            </div>

            <div>
              <p className="text-[10px] font-semibold uppercase tracking-[0.18em] text-violet-500">
                Agent Insight
              </p>

              <h3 className="mt-1 text-base font-semibold text-slate-900">
                Your plan is slightly over capacity
              </h3>
            </div>
          </div>

          <p className="mt-5 text-sm leading-6 text-slate-500">
            You have approximately 20 hours available but the current workload
            requires around 21 hours.
          </p>

          <div className="mt-5 rounded-2xl border border-violet-100 bg-violet-50/55 p-4">
            <p className="text-xs font-semibold text-violet-700">
              Recommended action
            </p>

            <p className="mt-1 text-xs leading-5 text-slate-500">
              Recover 1 hour or reduce effort on a lower-priority task.
            </p>
          </div>

          <Link
            to="/plans/1"
            className="mt-5 inline-flex items-center text-xs font-semibold text-violet-600 transition hover:text-violet-800"
          >
            View agent reasoning →
          </Link>
        </GlassCard>
      </div>

      {/* Activity */}
      <GlassCard className="p-5 sm:p-6">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-[10px] font-semibold uppercase tracking-[0.18em] text-slate-400">
              Recent Activity
            </p>

            <h3 className="mt-1 text-base font-semibold text-slate-900">
              What changed recently
            </h3>
          </div>

          <Link
            to="/plans/1"
            className="text-xs font-medium text-violet-600 hover:text-violet-800"
          >
            View plan
          </Link>
        </div>

        <div className="mt-5 space-y-4">
          <Activity
            icon="◈"
            title="Risk detected"
            description="Available time dropped below estimated workload."
            time="12 min ago"
          />

          <Activity
            icon="↻"
            title="Agent evaluated plan"
            description="High-priority tasks were preserved."
            time="13 min ago"
          />

          <Activity
            icon="✓"
            title="Feature engineering completed"
            description="One task moved closer to completion."
            time="Yesterday"
          />
        </div>
      </GlassCard>
    </div>
  );
}

function StatCard({ label, value, caption, danger = false }) {
  return (
    <GlassCard
      hover
      className="min-w-0 p-4 sm:p-5"
    >
      <p className="truncate text-xs font-medium text-slate-400">
        {label}
      </p>

      <p
        className={`mt-2 text-2xl font-semibold tracking-tight sm:text-3xl ${
          danger ? "text-red-500" : "text-slate-900"
        }`}
      >
        {value}
      </p>

      <p className="mt-1 truncate text-[10px] text-slate-400 sm:text-xs">
        {caption}
      </p>
    </GlassCard>
  );
}

function MiniMetric({ label, value, danger = false }) {
  return (
    <div className="min-w-0 rounded-xl bg-slate-50/80 p-3 text-center">
      <p className="truncate text-[9px] uppercase tracking-wide text-slate-400">
        {label}
      </p>

      <p
        className={`mt-1 text-sm font-semibold ${
          danger ? "text-red-500" : "text-slate-800"
        }`}
      >
        {value}
      </p>
    </div>
  );
}

function Activity({ icon, title, description, time }) {
  return (
    <div className="flex gap-3">
      <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-violet-50 text-xs text-violet-600">
        {icon}
      </div>

      <div className="min-w-0 flex-1">
        <div className="flex flex-col gap-1 sm:flex-row sm:items-center sm:justify-between">
          <p className="text-xs font-semibold text-slate-700">
            {title}
          </p>

          <span className="text-[10px] text-slate-400">
            {time}
          </span>
        </div>

        <p className="mt-1 text-xs leading-5 text-slate-500">
          {description}
        </p>
      </div>
    </div>
  );
}

export default Dashboard;