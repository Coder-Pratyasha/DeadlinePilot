function LoadingSpinner({ size = "md", text = "Loading..." }) {
  const sizeClass = {
    sm: "h-4 w-4 border-2",
    md: "h-6 w-6 border-2",
    lg: "h-8 w-8 border-[3px]",
  }[size];

  return (
    <div className="flex items-center justify-center gap-3 text-slate-500">
      <div
        className={`animate-spin rounded-full border-violet-200 border-t-violet-600 ${sizeClass}`}
      />

      {text && <span className="text-sm">{text}</span>}
    </div>
  );
}

export default LoadingSpinner;