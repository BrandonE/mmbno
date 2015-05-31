var socket = io(),
    config,
    clientPlayerNum,
    grid,
    players = [null, null],
    row,
    col,
    cols,
    panel;

function draw() {
    $('#grid').text(gridToString(config, grid, players, clientPlayerNum));
}

$(document).ready
(
    function ()
    {
        $.getJSON('config.json', function(data) {
            config = data;

            socket.on('user connected', function(playerNum, game) {
                var player,
                    p;

                players = game.players;

                if (clientPlayerNum === undefined) {
                    clientPlayerNum = playerNum;

                    if (clientPlayerNum) {
                        $('#playerNum').text(clientPlayerNum);
                        $('.playing').show();
                    } else {
                        $('.observing').show();
                    }

                    grid = game.field;
                }

                for (p in players) {
                    player = players[p];

                    if (player) {
                        grid[player.row][player.col].character = player;
                    }
                }

                draw();
            });

            socket.on('user disconnected', function(playerNum) {
                var player;

                if (playerNum) {
                    player = players[playerNum - 1];
                    grid[player.row][player.col].character = null;
                    delete player;
                    draw();
                }
            });

            socket.on('health changed', function(playerNum, health) {
                var player;

                if (playerNum) {
                    player = players[playerNum - 1];
                    player.health = health;
                    draw();
                }
            });

            socket.on('moved', function(playerNum, row, col) {
                var player;

                if (playerNum) {
                    player = players[playerNum - 1];
                    grid[player.row][player.col].character = null;
                    player.row = row;
                    player.col = col;
                    grid[row][col].character = player;
                    draw();
                }
            });

            socket.on('panel changed', function(panel) {
                grid[panel.row][panel.col].status = panel.status;
                grid[panel.row][panel.col].stolen = panel.stolen;
                draw();
            });

            $(document).keydown(function(e) {
                switch(e.which) {
                    case 37:
                        socket.emit('move', 'left');
                        break;

                    case 38:
                        socket.emit('move', 'up');
                        break;

                    case 39:
                        socket.emit('move', 'right');
                        break;

                    case 40:
                        socket.emit('move', 'down');
                        break;

                    case 65:
                        socket.emit('buster');
                        break;

                    default:
                        return;
                }

                e.preventDefault();
            });
        });
    }
);
