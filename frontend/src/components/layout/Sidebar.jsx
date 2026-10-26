import { NavLink } from "react-router-dom";

function Sidebar({ mobileMenuOpen, setMobileMenuOpen }) {
  return (
    <>
      {/* Mobile overlay */}
      <div
        onClick={() => setMobileMenuOpen(false)}
        className={`fixed inset-0 z-40 bg-slate-900/20 backdrop-blur-[2px] transition-opacity duration-300 lg:hidden ${
          mobileMenuOpen
            ? "pointer-events-auto opacity-100"
            : "pointer-events-none opacity-0"
        }`}
      />

      {/* Desktop + Mobile Sidebar */}
      <aside
        className={`fixed left-0 top-0 z-50 h-screen w-72 border-r border-slate-200/70 bg-white/85 p-5 backdrop-blur-2xl transition-transform duration-300 ease-out lg:z-40 lg:w-64 lg:translate-x-0 ${
          mobileMenuOpen ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        {/* Brand */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3 px-2 py-2">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl border border-violet-200 bg-violet-50 text-lg text-violet-600 shadow-sm">
              ◈
            </div>

            <div>
              <h1 className="text-sm font-semibold tracking-wide text-slate-900">
                DeadlinePilot
              </h1>

              <p className="text-[10px] text-slate-400">
                AI Decision Engine
              </p>
            </div>
          </div>

          {/* Mobile close */}
          <button
            type="button"
            onClick={() => setMobileMenuOpen(false)}
            className="flex h-9 w-9 items-center justify-center rounded-xl text-xl text-slate-400 transition hover:bg-slate-100 hover:text-slate-700 lg:hidden"
            aria-label="Close navigation"
          >
            ×
          </button>
        </div>

        {/* Navigation */}
        <nav className="mt-10 space-y-2">
          <p className="mb-3 px-3 text-[10px] font-semibold uppercase tracking-[0.18em] text-slate-400">
            Workspace
          </p>

          <NavItem
            to="/"
            icon="⌂"
            label="Overview"
            closeMenu={() => setMobileMenuOpen(false)}
          />

          <NavItem
            to="/plans"
            icon="◫"
            label="My Plans"
            closeMenu={() => setMobileMenuOpen(false)}
          />

          <NavItem
            to="/new-plan"
            icon="＋"
            label="New Plan"
            closeMenu={() => setMobileMenuOpen(false)}
          />
        </nav>

        {/* Recent */}
        <div className="mt-10">
          <p className="mb-3 px-3 text-[10px] font-semibold uppercase tracking-[0.18em] text-slate-400">
            Recent
          </p>

          <NavLink
            to="/plans/1"
            onClick={() => setMobileMenuOpen(false)}
            className="block rounded-xl px-3 py-2.5 text-left text-xs text-slate-500 transition hover:bg-slate-100 hover:text-slate-900"
          >
            AI/ML Final Project
          </NavLink>

          <NavLink
            to="/plans/2"
            onClick={() => setMobileMenuOpen(false)}
            className="mt-1 block rounded-xl px-3 py-2.5 text-left text-xs text-slate-500 transition hover:bg-slate-100 hover:text-slate-900"
          >
            Placement Preparation
          </NavLink>
        </div>

        {/* Agent status */}
        <div className="absolute bottom-5 left-5 right-5">
          <div className="glass rounded-2xl p-3">
            <div className="flex items-center gap-2">
              <div className="h-2 w-2 rounded-full bg-emerald-500 shadow-[0_0_10px_rgba(16,185,129,0.35)]" />

              <span className="text-xs font-medium text-slate-600">
                Agent Online
              </span>
            </div>

            <p className="mt-2 text-[10px] leading-4 text-slate-400">
              Decision engine ready
            </p>
          </div>
        </div>
      </aside>
    </>
  );
}

function NavItem({ to, icon, label, closeMenu }) {
  return (
    <NavLink
      to={to}
      end={to === "/"}
      onClick={closeMenu}
      className={({ isActive }) =>
        `flex min-h-11 w-full items-center gap-3 rounded-xl px-3 py-2.5 text-sm transition ${
          isActive
            ? "border border-violet-200 bg-violet-50 font-medium text-violet-700 shadow-sm"
            : "text-slate-500 hover:bg-slate-100 hover:text-slate-900"
        }`
      }
    >
      <span className="text-base">{icon}</span>
      {label}
    </NavLink>
  );
}

export default Sidebar;