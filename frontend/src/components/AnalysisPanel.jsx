import MatchBadge from "./MatchBadge";

const pct = (v) => (v == null ? "–" : `${Math.round(v * 100)}%`);

function Chips({ title, items, tone = "" }) {
  if (!items?.length) return null;
  return (
    <div className="chips">
      <span className="chips-title">{title}</span>
      {items.map((item) => (
        <span key={item} className={`chip ${tone}`}>{item}</span>
      ))}
    </div>
  );
}

export default function AnalysisPanel({ application, canAnalyze, busy, onAnalyze }) {
  const { analysis, match_score } = application;
  return (
    <section className="analysis">
      <div className="analysis-head">
        <h3>AI match</h3>
        <button type="button" onClick={onAnalyze} disabled={!canAnalyze || busy}>
          {busy ? "Analyzing…" : analysis ? "Re-analyze" : "Analyze match"}
        </button>
      </div>
      {!canAnalyze && (
        <p className="hint">Save a job description (and any edits) before analyzing.</p>
      )}
      {analysis && (
        <>
          <p>
            <MatchBadge score={match_score} />{" "}
            {analysis.seniority && <span>Level: {analysis.seniority}</span>}
          </p>
          <Chips title="You have" items={analysis.matched_skills} tone="good" />
          <Chips title="Missing" items={analysis.missing_skills} tone="bad" />
          <Chips title="Keywords" items={analysis.keywords} />
          <p className="hint">
            Semantic {pct(analysis.semantic_score)} · Skill coverage {pct(analysis.skill_coverage)}
          </p>
        </>
      )}
    </section>
  );
}