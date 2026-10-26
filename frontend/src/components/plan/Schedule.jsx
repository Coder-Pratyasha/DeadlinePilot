import GlassCard from "../common/GlassCard";

const schedule = [
  {
    day: "Day 1",
    date: "Oct 27",
    tasks: [
      ["Model training", "3h"],
      ["Model evaluation", "1h"],
    ],
  },
  {
    day: "Day 2",
    date: "Oct 28",
    tasks: [
      ["Model training", "2h"],
      ["Documentation", "2h"],
    ],
  },
  {
    day: "Day 3",
    date: "Oct 29",
    tasks: [
      ["Documentation", "2h"],
      ["Final testing", "2h"],
    ],
  },
  {
    day: "Day 4",
    date: "Oct 30",
    tasks: [
      ["Presentation", "2h"],
      ["Final buffer", "1h"],
    ],
  },
];

function Schedule() {
  return (
    <GlassCard className="p-5 sm:p-6">

      <div>
        <p className="text-[10px] font-semibold uppercase tracking-[0.18em] text-violet-500">
          Execution
        </p>

        <h2 className="mt-1 text-sm font-semibold text-slate-800">
          Current Schedule
        </h2>
      </div>

      <div className="mt-5 space-y-3">

        {schedule.map((item, index) => (
          <div
            key={index}
            className="rounded-2xl border border-slate-200/70 bg-white/50 p-4"
          >

            <div className="flex items-center justify-between">

              <div>
                <p className="text-xs font-semibold text-slate-700">
                  {item.day}
                </p>

                <p className="mt-0.5 text-[10px] text-slate-400">
                  {item.date}
                </p>
              </div>

              <span className="rounded-full bg-slate-100 px-2.5 py-1 text-[9px] font-medium text-slate-500">
                {item.tasks.length} blocks
              </span>

            </div>

            <div className="mt-3 space-y-2">

              {item.tasks.map(([title, hours], taskIndex) => (
                <div
                  key={taskIndex}
                  className="flex items-center justify-between rounded-xl bg-slate-50/80 px-3 py-2.5"
                >

                  <span className="text-[11px] text-slate-600">
                    {title}
                  </span>

                  <span className="text-[10px] font-medium text-slate-400">
                    {hours}
                  </span>

                </div>
              ))}

            </div>

          </div>
        ))}

      </div>

    </GlassCard>
  );
}

export default Schedule;