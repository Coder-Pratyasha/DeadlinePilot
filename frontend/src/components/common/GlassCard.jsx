function GlassCard({
  children,
  className = "",
  strong = false,
  hover = false,
}) {
  return (
    <div
      className={`${strong ? "glass-strong" : "glass"} ${
        hover ? "glass-hover" : ""
      } rounded-2xl ${className}`}
    >
      {children}
    </div>
  );
}

export default GlassCard;