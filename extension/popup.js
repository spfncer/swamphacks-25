console.log('This is a popup!');
chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    var activeTab = tabs[0];
    var activeTabUrl = activeTab.url;
    document.querySelector(".site-url").innerText = activeTabUrl;
});
window.addEventListener("DOMContentLoaded", () => {
    var simplemde = new SimpleMDE({ element: document.getElementById("comment-input") });
});