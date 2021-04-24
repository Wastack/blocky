
// constants

const wall_margin = 8;
const animation_speed = 30;

// variables

var currently_animated = false;
var images = {}

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

const frogImg = new Image();
frogImg.src = 'resources/frog.png';
images["F"] = frogImg;
images_ready = async function() {
    return new Promise((all_resolved, all_reject) => {
        let promises = [];
        for(var key in images) {
            promises.push(new Promise((resolve, reject) => {
                images[key].onload = function() {
                    return resolve();
                };
            }));
        }

        Promise.all(promises).then(function() {
            return all_resolved();
        });
    });
};

var ws;


images_ready().then(function() {
    console.log("Images are ready");
    // Init websocket
    ws = new WebSocket("ws://127.0.0.1:8765/");

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

});


// Init canvas
canvas = document.getElementById("gameCanvas");
canvas.width = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
canvas.height = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;


var phase = 1
var current_map = 0

var block_size = 40;
var half_block_size = Math.floor(block_size/2);


function keyDownHandler(e) {
    if(currently_animated) {
        return;
    }
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
                if (block.move_once) {
                    return "F";
                }
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

function drawWallsPx(block, pos_x_px, pos_y_px, ctx) {
    if(!block.walls) {
        return;
    }

    ctx.strokeStyle = "red";
    ctx.lineWidth = 8;
    ctx.beginPath();
    if(block.walls.down) {
        ctx.moveTo(pos_x_px + wall_margin, pos_y_px+block_size - wall_margin);
        ctx.lineTo(pos_x_px+block_size - wall_margin, pos_y_px+block_size - wall_margin);
        ctx.stroke();
    }
    if (block.walls.left) {
        ctx.moveTo(pos_x_px + wall_margin, pos_y_px + wall_margin);
        ctx.lineTo(pos_x_px + wall_margin, pos_y_px+block_size - wall_margin);
        ctx.stroke();
    }
    if (block.walls.up) {
        ctx.moveTo(pos_x_px + wall_margin, pos_y_px + wall_margin);
        ctx.lineTo(pos_x_px+block_size - wall_margin, pos_y_px + wall_margin);
        ctx.stroke();
    }
    if (block.walls.right) {
        ctx.moveTo(pos_x_px+block_size - wall_margin, pos_y_px + wall_margin);
        ctx.lineTo(pos_x_px+block_size - wall_margin, pos_y_px+block_size - wall_margin);
        ctx.stroke();
    }
    ctx.closePath();

}

function drawWalls(block, pos, ctx) {
    const pos_x_px = pos.x*block_size;
    const pos_y_px = pos.y*block_size;

    drawWallsPx(block, pos_x_px, pos_y_px, ctx);
}

function renderMap(map) {
    console.log(map);
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

    block_size = Math.min(Math.floor(canvas.height/height), 60);
    half_block_size = Math.floor(block_size/2);

    const width_px = width*block_size;
    const height_px = height*block_size;

    //ctx.beginPath();
    //for (let i = 0; i <= width; i++) {
    //    const x = i*block_size;
    //    ctx.moveTo(x, 0);
    //    ctx.lineTo(x, height_px)
    //    ctx.stroke();
    //}
    //for (let i = 0; i <= height; i++) {
    //    const y = i*block_size;
    //    ctx.moveTo(0, y);
    //    ctx.lineTo(width_px, y);
    //    ctx.stroke();
    //}
    //ctx.closePath();

    // blocks
    const cells = map.cells;
    console.log("number of cells: " + cells.length);
    for(let i=0; i<cells.length; ++i) {
        console.log("hit");
        let cell = cells[i];
        const pos = cell.pos;
        const blocks = cell.blocks;
        const block = blocks[blocks.length-1];

        current_map[pos.x + ":" + pos.y] = block;
        putToCell(block, pos, ctx);
    }
}

function onGameMapReceived(map_data) {
    const map = JSON.parse(map_data);
    renderMap(map);
    document.addEventListener("keydown", keyDownHandler, true);
}

function clearCell(position, ctx) {
    clearCellPx(position.x*block_size, position.y*block_size, ctx);
}

function clearCellPx(px_pos_x, px_pos_y, ctx) {
    ctx.clearRect(px_pos_x + 2,
                  px_pos_y + 2,
                  block_size - 4,
                  block_size - 4);
}

function putToCellPx(block, px, py, ctx) {
    const cellText = cellTextFromBlock(block);
    const image = imageFromCellText(cellText);
    if(image) {
        if(block.type === "Stone") {
            ctx.drawImage(image, px, py, block_size, block_size);
        }
        else {
            ctx.drawImage(image, px + 2, py + 2, block_size - 4, block_size - 4);
        }
    }
    else {
        ctx.fillText(cellTextFromBlock(block), px + half_block_size, py + half_block_size);
    }

    // draw Text to signal life of ice block
    if(block.type == "MeltingIce") {
        ctx.fillText(cellTextFromBlock(block), px+ half_block_size, py + half_block_size);
    }

    drawWallsPx(block, px, py, ctx);
}

function putToCell(block, position, ctx) {
    const px = position.x*block_size;
    const py = position.y*block_size;

    putToCellPx(block, px, py, ctx);
}

function onGameReports(data) {
    const data_obj = JSON.parse(data);
    const ctx = canvas.getContext("2d");
    ctx.font = "30px Arial";
    ctx.textAlign = "center";
    ctx.textBaseline = 'middle';

    const steps = data_obj.steps;
    var reports_done;
    var step_i = 0;
    let start;
    let blocks;
    let px = {};
    let py = {};

    function update(timestamp) {
        const reports = steps[step_i].reports;
        if(reports_done === undefined) {
            reports_done = new Array(reports.length).fill(false);

            // collect blocks for reports
            blocks = [];
            for(let i=0; i<reports.length; ++i) {
                let pos = reports[i].position;
                blocks.push(current_map[pos.x + ":" + pos.y]);
            }
        }

        if (start === undefined) {
                start = timestamp;
        }

        for(let report_i=0; report_i<reports.length; report_i++) {
            if(reports_done[report_i]) {
                continue;
            }

            console.log("Animating step " + step_i + ", record: " + report_i);

            let ms_passed = timestamp-start;
            start = timestamp;

            let report = reports[report_i];
            const pos = report.position;

            const target = report.target;

            const block = blocks[report_i];
            if(!block) {
                console.log("Ohh nooo. Block not found for step " + step_i + ", record " + report_i);
                return;
            }

            switch(report.type) {
                case "moving":
                    if(target !== null) {
                        if(!px[report_i]) {
                            px[report_i] = pos.x*block_size;
                            py[report_i] = pos.y*block_size;
                        }
                        let signum_x = target.x - pos.x;
                        let signum_y = target.y - pos.y;

                        clearCellPx(px[report_i], py[report_i], ctx);
                        px[report_i] += signum_x*animation_speed;
                        py[report_i] += signum_y*animation_speed;


                        let distance = (px[report_i] - target.x*block_size + py[report_i]-target.y*block_size )*(signum_x+signum_y);
                        if(distance > 0) {
                            // draw last
                            px[report_i] += -signum_x*distance;
                            py[report_i] += -signum_y*distance;
                            putToCellPx(block, px[report_i], py[report_i], ctx);

                            // report done
                            delete current_map[pos.x + ":" + pos.y];
                            current_map[target.x + ":" + target.y] = block;
                            delete px[report_i];
                            delete py[report_i];
                            reports_done[report_i] = true;
                            console.log("Move done");
                        } else {
                            putToCellPx(block, px[report_i], py[report_i], ctx);
                        }
                    }
                    else {
                        // captured
                        clearCell(pos, ctx);
                        reports_done[report_i] = true;
                        delete current_map[pos.x + ":" + pos.y];
                        console.log("captured");
                    }
                    break;
                case "melting":
                    clearCell(pos, ctx);
                    block.life = report.life_now;
                    if(block.life > 0) {
                        putToCell(block, pos, ctx);
                    }
                    reports_done[report_i] = true;
                    break;
                default:
                    reports_done[report_i] = true;
                    break;
            }
        }

        if( reports_done.every(function(b) { return b;})) {
            reports_done = undefined;
            step_i++;
        }

        if(step_i < steps.length) {
            window.requestAnimationFrame(update);
        }
        else {
            currently_animated = false;
        }
    }

    if(steps.length > 0) {
        console.log("Start animating");
        currently_animated = true;
        window.requestAnimationFrame(update);
    }
}
