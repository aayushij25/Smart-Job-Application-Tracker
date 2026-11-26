import MatchBadge from "./MatchBadge";

export default function ApplicationCard({application}) {
    const {company, role, applied_date, match_score} = application;
    return (
        <article className="card">
            <h3>{company}</h3>
            <p className="role">{role}</p>
            <div className="card-meta">
                <span>{applied_date ? `Applied ${applied_date}`: "Not applied yet"}</span>
                {match_score !== null && (
                    <span className="badge"><MatchBadge score={match_score} /></span>
                )}
            </div>
        </article>
    );
}