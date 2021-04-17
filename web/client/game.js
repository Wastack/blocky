
// Init canvas
canvas = document.getElementById("gameCanvas");
canvas.width = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
canvas.height = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;

// TODO init images


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

function renderMap(map) {
    const ctx = canvas.getContext("2d");
    ctx.strokeStyle = "black";
    ctx.lineWidth = 2;
    ctx.font = "30px Arial";
    ctx.textAlign = "center";
    ctx.textBaseline = 'middle';

    // border of rectangles
    const block_size = 40;
    const half_block_size = Math.floor(block_size/2);
    const width = map.map_size.width;
    const height = map.map_size.height;

    const width_px = width*block_size;
    const height_px = height*block_size;

    for (let i = 0; i <= width; i++) {
        const x = i*block_size;
        ctx.moveTo(x, 0);
        ctx.lineTo(x, height_px)
        ctx.stroke();
    }
    for (let i = 0; i <= height; i++) {
        const y = i*block_size;
        ctx.moveTo(0, y);
        ctx.lineTo(width_px, y);
        ctx.stroke();
    }

    const cells = map.cells;
    cells.forEach(function (cell) {
        const pos = cell.pos;
        const blocks = cell.blocks;
        const block = blocks[blocks.length-1];

        var cell_text = "?";
        switch(block.type) {
            case "Anna":
                cell_text = "A";
                break;
            case "MeltingIce":
                cell_text = "I";
                break;
            case "DuckPool":
                cell_text = "P";
                break;
            case "Stone":
                cell_text = "S";
                break;
            case "RollingBlock":
                cell_text = "R";
                break;
        }
        ctx.fillText(cell_text, pos.x*block_size + half_block_size, pos.y*block_size + half_block_size);
    });
}

function onGameMapReceived(map_data) {
    const map = JSON.parse(map_data);
    renderMap(map);
    document.addEventListener("keydown", keyDownHandler, true);
}

function onGameReports(data) {
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const map = JSON.parse(data);
    renderMap(map);
}

ws.onmessage = function (event) {
    console.log("received phase " + phase)
    var message = event.data;
    switch(phase) {
        case 1:
            onGameMapReceived(message);
            phase++;
            break;
        case 2:
            onGameReports(message);
            break;
    }
};

ws.onerror = function(evt) {
    document.getElementById("message").textContent = "Unable to connect to Game server.";
};
