import {
    DndContext,
    DragOverlay,
    KeyboardSensor,
    PointerSensor,
    useSensor,
    useSensors,
} from "@dnd-kit/core";
import { useState } from "react";
import {COLUMNS} from "../constants";
import ApplicationCard from "./ApplicationCard";
import KanbanColumn from "./KanbanColumn";

export default function KanbanBoard({byStatus, onMove, onOpen}) {
    const [activeCard, setActiveCard] = useState(null);

    const sensors = useSensors(
        useSensor(PointerSensor, {activationConstraint: {distance: 8}}),
        useSensor(KeyboardSensor)
    );

    const handleDragStart = ({ active }) => {
        setActiveCard(active.data.current.application);
    };

    const handleDragEnd = ({ active, over }) => {
        setActiveCard(null);
        if (!over) return; 
        const { application } = active.data.current;
        if (over.id !== application.status) {
            onMove(application.id, application.status, over.id);
        }
    };

    return (
        <DndContext
            sensors={sensors}
            onDragStart={handleDragStart}
            onDragEnd={handleDragEnd}
            onDragCancel={() => setActiveCard(null)}
        >
            <div className="board">
                {COLUMNS.map((col) => (
                    <KanbanColumn 
                        key={col.id}
                        column={col}
                        items={byStatus[col.id]}
                        onOpen={onOpen}
                    />
                ))}
            </div>

            <DragOverlay>
                {activeCard ? (
                    <div className="overlay-card">
                        <ApplicationCard application={activeCard} />
                    </div>
                ) : null}
            </DragOverlay>
        </DndContext>
    );
}