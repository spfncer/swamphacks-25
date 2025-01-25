function makeResizable(node) {
    node.style.overflowY = 'visible';

	function onChange() {
		const oldHeight = node.style.height;
		node.style.height = 'auto';
		const newHeight = node.scrollHeight;

		//set the height BACK to the old height so that the sizing can be transitioned
		node.style.height = oldHeight;

		//if uses more than 2 lines, use adjusting height
		if (newHeight >= 2 * parseFloat(getComputedStyle(node).fontSize)) {
			node.style.height = newHeight + 'px';
		}
		//if only one line is needed, hardcode at 1
		else node.style.height = '1em';
	}
	function onReset() {
		node.style.height = '1em';
	}
	node.addEventListener('input', onChange);
	node.addEventListener('reset', onReset);
}

window.addEventListener("DOMContentLoaded", () => {
    const boxes = document.querySelectorAll("[data-resizeable]");
    boxes.forEach(makeResizable);
})