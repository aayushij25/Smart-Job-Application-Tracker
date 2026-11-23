import {COLUMNS} from "../constants";
import ApplicationCard from "./ApplicationCard";

export default function KanbanBoard({byStatus}) {
    return (
        <div className="board">
            {COLUMNS.map((col) => (
                <section key={col.id} className="column">
                    <header className="column-header">
                        <h2>{col.title}</h2>
                        <span className="count">{byStatus[col.id].length}</span>
                    </header>
                    <div className="column-body">
                        {byStatus[col.id].map((app) => (
                            <ApplicationCard key={app.id} application={app} />
                        ))}
                        {byStatus[col.id].length === 0 && <p className="empty">Nothing here yet</p>}
                    </div>
                </section>
            ))}
        </div>
    );
}