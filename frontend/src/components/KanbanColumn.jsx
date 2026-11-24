import { useDroppable } from "@dnd-kit/core";
import DraggableCard from "./DraggableCard";

export default function KanbanColumn({ column, items, onOpen}) {
    const {setNodeRef, isOver} = useDroppable({ id: column.id });

    return (
        <section ref={setNodeRef} className={`column${isOver ? "over" : ""}`}>
            <header className="column-header">
                <h2>{column.title}</h2>
                <span className="count">{items.length}</span>
            </header>
            <div className="column-body">
                {items.map((app) => (
                    <DraggableCard key={app.id} application={app} onOpen={onOpen} />
                ))}
                {items.length === 0 && <p className="empty">Nothing here yet</p>}
            </div>
        </section>
    );
}