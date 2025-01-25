function makeElementDraggable(drag) {
    console.log("Making draggable", drag);
    const boundingBox = drag.getBoundingClientRect();

    drag.style.x = `${boundingBox.x}px`;
    drag.style.y = `${boundingBox.y}px`;
    drag.style.width = `${boundingBox.width}px`;
    drag.style.height = `${boundingBox.height}px`;
    drag.style.position = "absolute";

    drag.addEventListener("mousedown", (e) => {
        const x = e.clientX - drag.getBoundingClientRect().left;
        const y = e.clientY - drag.getBoundingClientRect().top;

        drag.style.x = `${drag.getBoundingClientRect().left}px`;
        drag.style.y = `${drag.getBoundingClientRect().top}px`;

        const onMouseMove = (e) => {
            drag.style.left = `${e.clientX - x}px`;
            drag.style.top = `${e.clientY - y}px`;
        }

        const onMouseUp = () => {
            window.removeEventListener("mousemove", onMouseMove);
            window.removeEventListener("mouseup", onMouseUp);
        }

        window.addEventListener("mousemove", onMouseMove);
        window.addEventListener("mouseup", onMouseUp);
    });
}
window.makeElementDraggable = makeElementDraggable;

window.addEventListener("DOMContentLoaded", () => {
    const drags = document.querySelectorAll("[data-draggable]");
    drags.forEach((drag) => {
        makeElementDraggable(drag);
    })
})