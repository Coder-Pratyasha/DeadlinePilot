import { useMemo, useState } from "react";
import { Link } from "react-router-dom";

import GlassCard from "../components/common/GlassCard";
import RiskBadge from "../components/common/RiskBadge";

function Plans() {
  const [search, setSearch] = useState("");
  const [filter, setFilter] = useState("All");

  const plans = [
    {
      id: 1,
      title: "AI/ML Final Project",
      deadline: "Oct 30, 2026",
      progress: 62,
      risk: "HIGH",
      hours: "20h",
      description: "Complete final-year AI/ML project and documentation.",
    },
    {
      id: 2,
      title: "Placement Preparation",
      deadline: "Nov 15, 2026",
      progress: 38,
      risk: "ON TRACK",
      hours: "46h",
      description: "Prepare DSA, ML, system design and interview topics.",
    },
    {
      id: 3,
      title: "GenAI Portfolio",
      deadline: "Nov 28, 2026",
      progress: 24,
      risk: "LOW",
      hours: "31h",
      description: "Build and polish GenAI projects for portfolio.",
    },
  ];

  const filteredPlans = useMemo(() => {
    return plans.filter((plan) => {
      const matchesSearch = plan.title
        .toLowerCase()
        .includes(search.toLowerCase());

      const matchesFilter =
        filter === "All" ||
        (filter === "At Risk" && plan.risk === "HIGH") ||
        (filter === "On Track" && plan.risk === "ON TRACK") ||
        (filter === "Low Risk" && plan.risk === "LOW");

      return matchesSearch && matchesFilter;
    });
  }, [search, filter]);

  return (
    <div className="space-y-5 pb-8 sm:space-y-6">
      {/* Header */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-xs font-medium text-violet-600">
            Workspace
          </p>

          <h1 className="mt-1 text-2xl font-semibold tracking-tight text-slate-900 sm:text-3xl">
            My Plans
          </h1>

          <p className="mt-2 text-sm text-slate-500">
            Your active and upcoming decision plans.
          </p>
        </div>

        <Link
          to="/new-plan"
          className="inline-flex min-h-11 items-center justify-center rounded-xl bg-violet-600 px-4 text-sm font-semibold text-white shadow-sm transition hover:bg-violet-700 hover:shadow-md"
        >
          + New Plan
        </Link>
      </div>

      {/* Search / filter */}
      <GlassCard className="p-3 sm:p-4">
        <div className="flex flex-col gap-3 sm:flex-row">
          <div className="relative min-w-0 flex-1">
            <span className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-sm text-slate-400">
              ⌕
            </span>

            <input
              type="text"
              placeholder="Search plans..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="h-11 w-full rounded-xl border border-slate-200 bg-white/70 pl-9 pr-3 text-sm text-slate-800 outline-none transition placeholder:text-slate-400 focus:border-violet-300 focus:ring-4 focus:ring-violet-100"
            />
          </div>

          <div className="mobile-scroll flex gap-2">
            {["All", "At Risk", "On Track", "Low Risk"].map((item) => (
              <button
                key={item}
                type="button"
                onClick={() => setFilter(item)}
                className={`min-h-11 shrink-0 rounded-xl border px-4 text-xs font-medium transition ${
                  filter === item
                    ? "border-violet-200 bg-violet-50 text-violet-700"
                    : "border-slate-200 bg-white/60 text-slate-500 hover:bg-white hover:text-slate-800"
                }`}
              >
                {item}
              </button>
            ))}
          </div>
        </div>
      </GlassCard>

      {/* Plans */}
      {filteredPlans.length > 0 ? (
        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
          {filteredPlans.map((plan) => (
            <PlanCard key={plan.id} plan={plan} />
          ))}
        </div>
      ) : (
        <GlassCard className="p-10 text-center sm:p-14">
          <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-2xl bg-violet-50 text-violet-600">
            ◫
          </div>

          <h3 className="mt-4 text-sm font-semibold text-slate-900">
            No plans found
          </h3>

          <p className="mx-auto mt-1 max-w-sm text-xs leading-5 text-slate-500">
            Try another search or create a new decision plan.
          </p>

          <Link
            to="/new-plan"
            className="mt-5 inline-flex min-h-10 items-center justify-center rounded-xl bg-violet-600 px-4 text-xs font-semibold text-white"
          >
            Create New Plan
          </Link>
        </GlassCard>
      )}
    </div>
  );
}

function PlanCard({ plan }) {
  return (
    <Link
      to={`/plans/${plan.id}`}
      className="group block min-w-0"
    >
      <GlassCard
        hover
        className="h-full p-5 transition duration-200"
      >
        {/* Top */}
        <div className="flex items-start justify-between gap-3">
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-violet-50 text-violet-600">
            ◈
          </div>

          <RiskBadge risk={plan.risk} />
        </div>

        {/* Title */}
        <h2 className="mt-5 truncate text-base font-semibold text-slate-900">
          {plan.title}
        </h2>

        <p className="mt-1 min-h-10 text-xs leading-5 text-slate-500">
          {plan.description}
        </p>

        {/* Progress */}
        <div className="mt-5">
          <div className="flex items-center justify-between">
            <span className="text-[10px] text-slate-400">
              Progress
            </span>

            <span className="text-xs font-semibold text-slate-700">
              {plan.progress}%
            </span>
          </div>

          <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-slate-100">
            <div
              className="h-full rounded-full bg-violet-500"
              style={{ width: `${plan.progress}%` }}
            />
          </div>
        </div>

        {/* Bottom metrics */}
        <div className="mt-5 grid grid-cols-2 gap-2">
          <div className="rounded-xl bg-slate-50/80 p-3">
            <p className="text-[9px] uppercase tracking-wide text-slate-400">
              Deadline
            </p>

            <p className="mt-1 text-xs font-semibold text-slate-700">
              {plan.deadline}
            </p>
          </div>

          <div className="rounded-xl bg-slate-50/80 p-3">
            <p className="text-[9px] uppercase tracking-wide text-slate-400">
              Available
            </p>

            <p className="mt-1 text-xs font-semibold text-slate-700">
              {plan.hours}
            </p>
          </div>
        </div>

        {/* Open */}
        <div className="mt-5 flex items-center justify-between border-t border-slate-100 pt-4">
          <span className="text-xs font-medium text-slate-400">
            Open plan
          </span>

          <span className="text-sm text-violet-500 transition group-hover:translate-x-1">
            →
          </span>
        </div>
      </GlassCard>
    </Link>
  );
}

export default Plans;