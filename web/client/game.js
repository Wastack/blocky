
// Init canvas
canvas = document.getElementById("gameCanvas");
canvas.width = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
canvas.height = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;

// TODO init images
images = {}

const boulderImg = new Image();
boulderImg.src = 'resources/boulder.png';
images["R"] = boulderImg;

const brickImg = new Image();
brickImg.src = 'resources/brick.png';
images["S"] = brickImg;

const duckImg = new Image();
duckImg.src = 'resources/duck.png';
images["A"] = duckImg;

const duckPoolImg = new Image();
duckPoolImg.src = 'resources/duck_pool.png';
images["P"] = duckPoolImg;

const iceImg = new Image();
iceImg.src = 'resources/ice.png';
images["I"] = iceImg;

var phase = 1
var ws = new WebSocket("ws://127.0.0.1:8765/"),
    messages = document.createElement('ul');
var current_map = 0

var block_size = 40;
var half_block_size = Math.floor(block_size/2);


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

function cellTextFromBlock(block) {
        switch(block.type) {
            case "Anna":
                return "A";
            case "MeltingIce":
                if(block.life > 0) {
                    return "I" + block.life;
                }
                break;
            case "DuckPool":
                return "P";
            case "Stone":
                return "S";
            case "RollingBlock":
                return "R";
        }
        return "?"
}

function imageFromCellText(cellText) {
    // 0 for Ice
    return images[cellText[0]];
}

function drawWalls(block, pos, ctx) {
    if(!block.walls) {
        return;
    }

    const pos_x_px = pos.x*block_size;
    const pos_y_px = pos.y*block_size;

    ctx.strokeStyle = "red";
    ctx.beginPath();
    if(block.walls.down) {
        ctx.moveTo(pos_x_px + 4, pos_y_px+block_size - 4);
        ctx.lineTo(pos_x_px+block_size - 4, pos_y_px+block_size - 4);
        ctx.stroke();
    }
    if (block.walls.left) {
        ctx.moveTo(pos_x_px + 4, pos_y_px + 4);
        ctx.lineTo(pos_x_px + 4, pos_y_px+block_size - 4);
        ctx.stroke();
    }
    if (block.walls.up) {
        ctx.moveTo(pos_x_px + 4, pos_y_px + 4);
        ctx.lineTo(pos_x_px+block_size - 4, pos_y_px + 4);
        ctx.stroke();
    }
    if (block.walls.right) {
        ctx.moveTo(pos_x_px+block_size - 4, pos_y_px + 4);
        ctx.lineTo(pos_x_px+block_size - 4, pos_y_px+block_size - 4);
        ctx.stroke();
    }
    ctx.closePath();
}

function renderMap(map) {
    current_map = {};
    const ctx = canvas.getContext("2d");
    ctx.strokeStyle = "black";
    ctx.lineWidth = 2;
    ctx.font = "30px Arial";
    ctx.textAlign = "center";
    ctx.textBaseline = 'middle';


    // border of rectangles
    const width = map.map_size.width;
    const height = map.map_size.height;

    block_size = Math.floor(canvas.height/height);
    half_block_size = Math.floor(block_size/2);

    const width_px = width*block_size;
    const height_px = height*block_size;

    ctx.beginPath();
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
    ctx.closePath();

    // blocks
    const cells = map.cells;
    cells.forEach(function (cell) {
        const pos = cell.pos;
        const blocks = cell.blocks;
        const block = blocks[blocks.length-1];

        current_map[pos.x + ":" + pos.y] = block;
        putToCell(block, pos, ctx);
    });
}

function onGameMapReceived(map_data) {
    const map = JSON.parse(map_data);
    renderMap(map);
    document.addEventListener("keydown", keyDownHandler, true);
}

function clearCell(position, ctx) {
    ctx.clearRect(position.x*block_size + 2,
                  position.y*block_size + 2,
                  block_size - 4,
                  block_size - 4);
}

function putToCell(block, position, ctx) {
    const cellText = cellTextFromBlock(block);
    const image = imageFromCellText(cellText);
    if(image) {
        ctx.drawImage(image,
                      position.x*block_size + 2,
                      position.y*block_size + 2,
                      block_size - 4,
                      block_size - 4);
    }
    else {
        ctx.fillText(cellTextFromBlock(block),
                     position.x*block_size + half_block_size,
                     position.y*block_size + half_block_size);
    }

    drawWalls(block, position, ctx);
}

function onGameReports(data) {
    const data_obj = JSON.parse(data);
    const ctx = canvas.getContext("2d");
    ctx.font = "30px Arial";
    ctx.textAlign = "center";
    ctx.textBaseline = 'middle';

    const steps = data_obj.steps;
    steps.forEach(function(step) {
        const reports = step.reports;
        reports.forEach(function(report) {
            const pos = report.position;
            const target = report.target;

            const block = current_map[pos.x + ":" + pos.y];
            if(!block) {
                console.log("OHHH noooo WTF.");
                return;
            }

            switch(report.type) {
                case "moving":
                    delete current_map[pos.x + ":" + pos.y];
                    clearCell(pos, ctx);
                    if(target !== null) {
                        current_map[target.x + ":" + target.y] = block;
                        putToCell(block, target, ctx);
                    }
                    break;
                case "melting":
                    clearCell(pos, ctx);
                    block.life = report.life_now;
                    if(block.life > 0) {
                        putToCell(block, pos, ctx);
                    }
                    break;
                case "player":
                    break;
            }
            // TODO apply report
        });
    });
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
