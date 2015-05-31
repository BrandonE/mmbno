var socket = io(),
    config,
    game;

function draw() {
    $('#game').text(gameToString(config, game, game.clientPlayerNum));
}

$(document).ready
(
    function ()
    {
        $.getJSON('config.json', function(data) {
            config = data;

            socket.on('user connected', function(playerNum, gameSent) {
                if (!game) {
                    game = {
                        clientPlayerNum : playerNum
                    };

                    if (playerNum) {
                        $('#playerNum').text(playerNum);
                        $('.playing').show();
                    } else {
                        $('.observing').show();
                    }
                }

                game.field = gameSent.field;
                game.players = gameSent.players;
                game.observers = gameSent.observers;

                draw();
            });

            socket.on('user disconnected', function(playerNum) {
                var player,
                    playerIndex;

                if (playerNum) {
                    playerIndex = playerNum - 1;
                    player = game.players[playerIndex];

                    game.field[player.row][player.col].character = null;
                    delete game.players[playerIndex];
                } else {
                    game.observers--;
                }

                draw();
            });

            socket.on('active connections', function(activeConnections) {
                $('#activeConnections').text(activeConnections);
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
                    player = game.players[playerNum - 1];
                    game.field[player.row][player.col].character = null;
                    player.row = row;
                    player.col = col;
                    game.field[row][col].character = player;
                    draw();
                }
            });

            socket.on('panel changed', function(panel) {
                game.field[panel.row][panel.col].status = panel.status;
                game.field[panel.row][panel.col].stolen = panel.stolen;
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
