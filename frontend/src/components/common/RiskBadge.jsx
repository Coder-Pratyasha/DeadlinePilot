function RiskBadge({ risk = "LOW", size = "sm" }) {
  const normalizedRisk = risk.toUpperCase();

  const styles = {
    HIGH: {
      wrapper: "border-red-200 bg-red-50 text-red-600",
      dot: "bg-red-500",
    },
    MEDIUM: {
      wrapper: "border-amber-200 bg-amber-50 text-amber-600",
      dot: "bg-amber-500",
    },
    LOW: {
      wrapper: "border-emerald-200 bg-emerald-50 text-emerald-600",
      dot: "bg-emerald-500",
    },
    "ON TRACK": {
      wrapper: "border-emerald-200 bg-emerald-50 text-emerald-600",
      dot: "bg-emerald-500",
    },
  };

  const style = styles[normalizedRisk] || styles.LOW;

  const sizeClasses =
    size === "md"
      ? "px-3 py-1.5 text-xs"
      : "px-2.5 py-1 text-[10px]";

  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full border font-semibold uppercase tracking-wide ${style.wrapper} ${sizeClasses}`}
    >
      <span className={`h-1.5 w-1.5 rounded-full ${style.dot}`} />

      {normalizedRisk}
    </span>
  );
}

export default RiskBadge;