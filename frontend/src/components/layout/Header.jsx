function Header({ mobileMenuOpen, setMobileMenuOpen }) {
  return (
    <header className="mb-5 flex items-center justify-between sm:mb-6">
      <div className="flex min-w-0 items-center gap-3">
        {/* Mobile menu */}
        <button
          type="button"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl border border-slate-200 bg-white/80 text-slate-600 shadow-sm transition hover:border-violet-200 hover:bg-violet-50 hover:text-violet-600 lg:hidden"
          aria-label="Open navigation"
        >
          {mobileMenuOpen ? (
            <span className="text-lg">×</span>
          ) : (
            <div className="space-y-1">
              <span className="block h-0.5 w-4 rounded-full bg-current" />
              <span className="block h-0.5 w-4 rounded-full bg-current" />
              <span className="block h-0.5 w-4 rounded-full bg-current" />
            </div>
          )}
        </button>

        <div className="min-w-0">
          <p className="hidden text-xs font-medium text-slate-400 sm:block">
            AI Decision Workspace
          </p>

          <h2 className="truncate text-lg font-semibold tracking-tight text-slate-900 sm:mt-1 sm:text-xl">
            Good evening.
          </h2>
        </div>
      </div>

      <div className="flex shrink-0 items-center gap-2 sm:gap-3">
        <div className="hidden items-center gap-2 rounded-full border border-violet-200 bg-violet-50 px-3 py-1.5 sm:flex">
          <div className="h-1.5 w-1.5 rounded-full bg-violet-500 shadow-[0_0_8px_rgba(124,58,237,0.45)]" />

          <span className="text-xs font-medium text-violet-700">
            AI Ready
          </span>
        </div>

        <div className="flex h-9 w-9 items-center justify-center rounded-full border border-slate-200 bg-white text-xs font-semibold text-slate-600 shadow-sm sm:h-10 sm:w-10">
          PP
        </div>
      </div>
    </header>
  );
}

export default Header;