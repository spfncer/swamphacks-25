/// <reference path="chrome.intellisense.js" />
// THIS JS RUNS INSIDE THE POPUP WINDOW

(() => {
    let simplemde;
    let currentURL;
    let user = undefined;
    function formatURL(url) {
        const urlObj = new URL(url);
        return urlObj.host + urlObj.pathname;
    }
    function closePopup() {
        window.close();
    }

    // Get the current tab URL
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        var activeTab = tabs[0];
        var activeTabUrl = formatURL(activeTab.url);
        currentURL = activeTabUrl;
        document.querySelector(".site-url").innerText = activeTabUrl;
    });
    // Register the event listeners
    window.addEventListener("DOMContentLoaded", () => {
        const button = document.querySelector("#submit-comment");
        button.addEventListener("click", postComment);

        const hider = document.querySelector(".hider");
        hider.addEventListener("click", clickToClose);

        const logout = document.querySelector("#logout-link");
        logout.addEventListener("click", closePopup);
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

    //tell the background service to fetch user info
    (async () => {
        chrome.runtime.sendMessage({ type: "getUserInfo" }, function (response) {
            const loginsArea = document.querySelector(".logins");
            if (typeof response === "object" && response.auth) {
                //user signed in
                user = response.nickname;
                const login = document.querySelector("#login-link");
                login.remove();
                const helloMessage = document.createElement("p");
                helloMessage.innerText = `Howdy, ${response.nickname}`;
                loginsArea.prepend(helloMessage);

                simplemde = new SimpleMDE({
                    element: document.getElementById("comment-input"), toolbar: [
                        "bold", "italic", "heading", "|", "quote", "code", "table", "|", "preview", "guide"
                    ]
                });
            } else {
                //user not signed in
                const logout = document.querySelector("#logout-link");
                logout.remove();
                const helloMessage = document.createElement("p");
                helloMessage.innerText = `Howdy, stranger`;
                loginsArea.appendChild(helloMessage);

                const input = document.getElementById("comment-input");
                input.remove();
                const submit = document.getElementById("submit-comment");
                submit.remove();

                const message = document.createElement("p");
                message.classList.add("sign-in-message");
                message.innerText = "Please sign in to comment";
                document.querySelector(".inner").appendChild(message);
            }
        });
    })();

    async function postComment(e) {
        e.preventDefault();
        const body = simplemde.value();
        chrome.runtime.sendMessage({ type: "postComment", author: user, url: currentURL, body: body }, function (response) {
            console.log("raw response", response);
            if (typeof response === "object") {
                createNote(response.body, response.author);
                simplemde.value("");
            } else {
                console.log("No comments found");
            }
        });
    }
})();