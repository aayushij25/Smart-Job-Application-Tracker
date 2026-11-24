import { useDraggable } from "@dnd-kit/core"
import ApplicationCard from "./ApplicationCard";

export default function DraggableCard({application, onOpen}) {
    const {attributes, listeners, setNodeRef, isDragging} = useDraggable({
        id: application.id,
        data: {application},
    });

    return (
        <div
        ref={setNodeRef}
        className={`draggable${isDragging ? "dragging": ""}`}
        onClick={() => onOpen(application)}
        {...listeners}
        {...attributes}
        >
            <ApplicationCard application={application}/>
        </div>
    );
}