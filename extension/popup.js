 /// <reference path="chrome.intellisense.js" />

// THIS JS RUNS INSIDE THE POPUP WINDOW
chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    var activeTab = tabs[0];
    var activeTabUrl = activeTab.url;
    document.querySelector(".site-url").innerText = activeTabUrl;
    console.log("Active tab url", activeTabUrl);
});
window.addEventListener("DOMContentLoaded", () => {
    var simplemde = new SimpleMDE({ element: document.getElementById("comment-input"), toolbar: [
        "bold", "italic", "heading", "|", "quote", "code", "table", "|", "preview", "guide"
    ]
     });
});

chrome.runtime.sendMessage({ type: "getComments" }, function (response) {
    if(typeof response === "object" && typeof response.comments === "object") {
        const commentsArea = document.querySelector(".comments-area");
        response.comments.forEach(comment => {
            const commentDiv = document.createElement("div");
            commentDiv.classList.add("comment");
            commentDiv.innerText = comment.body;
            commentsArea.appendChild(commentDiv);
        });
    } else {
        console.log(response);
    }

});

