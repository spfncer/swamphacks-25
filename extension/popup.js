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
            const commentLi = document.createElement("li");
            const commentDiv = document.createElement("div");
            commentDiv.classList.add("comment");
            const para = document.createElement("p");
            para.innerText = comment.body;
            commentDiv.appendChild(para);
            commentLi.appendChild(commentDiv);
            commentsArea.appendChild(commentLi);
        });
    } else {
        console.log("No comments found");
    }

});

