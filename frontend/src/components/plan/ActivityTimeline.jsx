import GlassCard from "../common/GlassCard";

const events = [
  {
    icon: "◈",
    title: "Risk detected",
    text: "Current workload exceeds available capacity by 1 hour.",
    time: "Just now",
  },
  {
    icon: "↻",
    title: "Plan recalculated",
    text: "Agent evaluated current workload and deadline pressure.",
    time: "12 min ago",
  },
  {
    icon: "✓",
    title: "Feature engineering completed",
    text: "Task marked as completed.",
    time: "1 hour ago",
  },
  {
    icon: "＋",
    title: "Plan created",
    text: "AI/ML Final Project plan initialized.",
    time: "Yesterday",
  },
];

function ActivityTimeline() {
  return (
    <GlassCard className="p-5 sm:p-6">

      <div>
        <p className="text-[10px] font-semibold uppercase tracking-[0.18em] text-violet-500">
          History
        </p>

        <h2 className="mt-1 text-sm font-semibold text-slate-800">
          Activity
        </h2>
      </div>

      <div className="mt-6">

        {events.map((event, index) => (
          <div
            key={index}
            className="relative flex gap-4 pb-6 last:pb-0"
          >

            {index !== events.length - 1 && (
              <div className="absolute left-[15px] top-8 h-[calc(100%-16px)] w-px bg-slate-200" />
            )}

            <div className="relative z-10 flex h-8 w-8 shrink-0 items-center justify-center rounded-xl border border-slate-200 bg-white text-xs text-violet-600 shadow-sm">
              {event.icon}
            </div>

            <div className="min-w-0 pt-0.5">

              <div className="flex flex-col gap-1 sm:flex-row sm:items-center sm:gap-3">

                <p className="text-xs font-semibold text-slate-700">
                  {event.title}
                </p>

                <span className="text-[9px] text-slate-300">
                  {event.time}
                </span>

              </div>

              <p className="mt-1 text-[10px] leading-5 text-slate-400">
                {event.text}
              </p>

            </div>

          </div>
        ))}

      </div>

    </GlassCard>
  );
}

export default ActivityTimeline;