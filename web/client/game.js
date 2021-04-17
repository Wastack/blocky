
var phase = 1
var ws = new WebSocket("ws://127.0.0.1:8765/"),
    messages = document.createElement('ul');

function keyDownHandler(e) {
    var message = "?";
    switch (e.keyCode) {
        case 37:
            message = "left";
            break;
        case 38:
            message = "up";
            break;
        case 39:
            message = "right";
            break;
        case 40:
            message = "down";
            break;
    }
    if (message === "?") {
        console.log('Unknown keycode: ' + e.keyCode);
        return;
    }
    console.log('Send movement: ' + message);
    ws.send(message);
}

function onGameMapReceived(map_data) {
    // TODO render map
    document.addEventListener("keydown", keyDownHandler, true);
}

function onPhaseTwo(data) {
    // TODO acknowledge reports/changes
}

ws.onmessage = function (event) {
    console.log("received phase " + phase)
    var message = event.data;
    switch(phase) {
        case 1:
            onGameMapReceived(message);
            break;
        case 2:
            onPhaseTwo(message);
            break;
    }
};

ws.onerror = function(evt) {
    document.getElementById("message").textContent = "Unable to connect to Game server.";
};
