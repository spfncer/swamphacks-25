/// <reference path="chrome.intellisense.js" />
console.log("Background script loaded");
chrome.runtime.onMessage.addListener(function (message, sender, senderResponse) {
    if (message.type == "getComments") {
        fetch("http://127.0.0.1:8000/comments/search", {
            method: "POST",
            headers: { "Content-Type": "application/json" }, 
            body: JSON.stringify({
                "webpage": message.url
            })
        })
            .then(response => response.json())
            .then(data => {
                console.log("Raw data", data);
                senderResponse(data);
            })
        return true;
    } else if (message.type == "postComment"){
        fetch("http://127.0.0.1:8000/comments/search", {
            method: "POST",
            headers: { "Content-Type": "application/json" }, 
            body: JSON.stringify({
                "author": message.author,
                "webpage": message.url,
                "body": message.body
            })
        })
            .then(response => response.json())
            .then(data => {
                console.log("Raw data", data);
                senderResponse(data);
            })
        }
    });
