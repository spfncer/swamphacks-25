 /// <reference path="chrome.intellisense.js" />
console.log("Background script loaded");
chrome.runtime.onMessage.addListener(function (message, sender, senderResponse){
    if(message.type == "getComments") {
        const commentResponse = fetch("http://127.0.0.1:8000/comments/", {method: "GET"})
        .then(response => response.json())
        .then(data => {
            senderResponse(data);
        })
        return true;
    }
});