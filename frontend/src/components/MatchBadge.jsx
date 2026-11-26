export default function MatchBadge({ score }) {
  if (score === null || score === undefined) return null;
  const pct = Math.round(score * 100);
  const tone = pct >= 70 ? "high" : pct >= 40 ? "mid" : "low";
  return <span className={`badge ${tone}`}>{pct}% match</span>;
}