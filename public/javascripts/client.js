var socket = io(),
    config,
    clientPlayerNum = -1,
    grid,
    players = [null, null],
    EOL = '\n',
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

            socket.on('user connected', function(playerNum, fieldSent, playersSent) {
                var player,
                    p;

                players = playersSent;

                if (clientPlayerNum === -1) {
                    clientPlayerNum = playerNum;
                    $('#playerNum').text(clientPlayerNum);

                    grid = fieldSent;
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
                draw();
            });

            socket.on('health changed', function(playerNum, health) {
                var player = players[playerNum - 1];
                player.health = health;
                draw();
            });

            socket.on('moved', function(playerNum, row, col) {
                var player = players[playerNum - 1];
                grid[player.row][player.col].character = null;
                player.row = row;
                player.col = col;
                grid[row][col].character = player;
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
