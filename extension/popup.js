/// <reference path="chrome.intellisense.js" />
// THIS JS RUNS INSIDE THE POPUP WINDOW

(() => {
    let simplemde;
    let currentURL;
    function formatURL(url) {
        const urlObj = new URL(url);
        return urlObj.host + urlObj.pathname;
    }
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        var activeTab = tabs[0];
        var activeTabUrl = formatURL(activeTab.url);
        currentURL = activeTabUrl;
        document.querySelector(".site-url").innerText = activeTabUrl;
        console.log("Active tab url", activeTabUrl);
    });
    window.addEventListener("DOMContentLoaded", () => {
        simplemde = new SimpleMDE({
            element: document.getElementById("comment-input"), toolbar: [
                "bold", "italic", "heading", "|", "quote", "code", "table", "|", "preview", "guide"
            ]
        });
    });

    function clickToClose(e) {
        e.stopPropagation();
        const hider = document.querySelector(".hider");
        const expanded = document.querySelector(".expanded");
        if (expanded) {
            expanded.classList.remove("expanded");
            hider.classList.remove("show");
        }
    }

    function expandNote(node) {
        // console.log("Expanding note", node);
        // const board = document.querySelector(".comments-area");
        // board?.addEventListener("click", clickToClose);
        node.classList.add("expanded");
        const hider = document.querySelector(".hider");
        hider.classList.add("show");
    }

    function createNote(text, author) {
        const commentsArea = document.querySelector(".comments-area");
        const commentLi = document.createElement("li");
        const commentDiv = document.createElement("div");
        commentDiv.classList.add("comment");
        const para = document.createElement("p");
        para.innerText = text;
        const user = document.createElement("p");
        user.classList.add("left");
        const userSpan = document.createElement("span");
        userSpan.innerText = author;
        user.appendChild(userSpan);
        commentDiv.appendChild(para);
        commentDiv.appendChild(user);
        commentLi.appendChild(commentDiv);
        commentsArea.appendChild(commentLi);

        commentLi.addEventListener("click", () => {expandNote(commentLi)});
    }


    //tell the background service to fetch comments
    (async () => {
        const [tab] = await chrome.tabs.query({ active: true, lastFocusedWindow: true });
        const formatted = formatURL(tab.url);
        currentURL = formatted;
        chrome.runtime.sendMessage({ type: "getComments", url: formatted }, function (response) {
            if (typeof response === "object" && typeof response.comments === "object") {
                response.comments.forEach(comment => {
                    createNote(comment.body, comment.author);
                });
            } else {
                console.log("No comments found");
            }
        });
    })();

    async function postComment(e) {
        e.preventDefault();
        console.log("Posting comment");
        const author = 'Fun Person'; //TODO: get author from user
        const body = simplemde.value();
        chrome.runtime.sendMessage({ type: "postComment", author, url: currentURL, body: body }, function (response) {
            if (typeof response === "object") {
                createNote(response.body, response.author);
                simplemde.value("");
            } else {
                console.log("No comments found");
            }
        });
    }
    window.addEventListener("DOMContentLoaded", () => {
        const button = document.querySelector("#submit-comment");
        console.log("Button", button);
        button.addEventListener("click", postComment);

        const hider = document.querySelector(".hider");
        hider.addEventListener("click", clickToClose);
    })
})();