var socket = io(),
    config,
    game;

function draw() {
    $('#game').text(gameToString(config, game, game.clientPlayerNum));
}

function showChips() {
    var chips,
        chipNames,
        chip,
        c;

    if (game.clientPlayerNum) {
        chips = game.players[game.clientPlayerNum - 1].chips;
        chipNames = [];

        for (c in chips) {
            chip = chips[c];
            chipNames.push(chip.name);
        }

        $('#chips').text(chipNames.join(', '));
    }
}

$(document).ready
(
    function ()
    {
        $.getJSON('config.json', function(data) {
            config = data;

            socket.on('user connected', function(playerNum, gameSent) {
                var player,
                    playerIndex;

                if (game) {
                    if (playerNum) {
                        playerIndex = playerNum - 1;
                        player = gameSent.players[playerIndex];

                        game.players[playerIndex] = player;
                        game.field[player.row][player.col].character = player;
                    } else {
                        game.observers++;
                    }
                } else {
                    game = {
                        field           : gameSent.field,
                        players         : gameSent.players,
                        observers       : gameSent.observers,
                        clientPlayerNum : playerNum
                    };

                    if (playerNum) {
                        $('#playerNum').text(playerNum);
                        $('.playing').show();
                    } else {
                        $('.observing').show();
                    }
                }

                showChips();
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

            socket.on('chip used', function(playerNum, chip) {
                var player,
                    c;

                if (playerNum) {
                    player = game.players[playerNum - 1];

                    for (c in player.chips) {
                        if (chip.name === player.chips[c].name) {
                            delete player.chips[c];
                        }
                    }

                    showChips();
                }
            });

            socket.on('panel type changed', function(panelRow, panelCol, type) {
                game.field[panelRow][panelCol].type = type;
                draw();
            });

            socket.on('panel stolen changed', function(panelRow, panelCol, stolen) {
                game.field[panelRow][panelCol].stolen = stolen;
                draw();
            });

            socket.on('player health changed', function(playerNum, health) {
                var player;

                if (playerNum) {
                    player = game.players[playerNum - 1];
                    player.health = health;
                    draw();
                }
            });

            socket.on('player moved', function(playerNum, row, col) {
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
