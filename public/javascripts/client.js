var socket = io(),
    config,
    game,
    chips;

function draw() {
    $('#game').text(gameToString(config, game, game.clientPlayerNum));
}

function showChips() {
    var chipNames,
        chip,
        c;

    if (chips) {
        chipNames = [];

        for (c in chips) {
            if (chips.hasOwnProperty(c)) {
                chip = chips[c];
                chipNames.push(chip.name);
            }
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

            socket.on('chips', function(chipsSent) {
                chips = chipsSent;
                showChips();
            });

            socket.on('chip used', function(playerNum, chip) {
                var c;

                if (playerNum && game.clientPlayerNum === playerNum) {
                    for (c in chips) {
                        if (chips.hasOwnProperty(c)) {
                            if (chip.name === chips[c].name) {
                                delete chips[c];
                                break;
                            }
                        }
                    }

                    showChips();
                }
            });

            socket.on('panel type changed', function(panelRow, panelCol, type) {
                game.field[panelRow][panelCol].type = type;
                draw();
            });

            socket.on('panel flip stolen', function(panelRow, panelCol) {
                game.field[panelRow][panelCol].stolen = !game.field[panelRow][panelCol].stolen;
                draw();
            });

            socket.on('player damage handler changed', function(playerNum, damageHandler) {
                var player;

                if (playerNum) {
                    player = game.players[playerNum - 1];
                    player.damageHandler = damageHandler;
                    draw();
                }
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

                    // A
                    case 65:
                        socket.emit('use chip');
                        break;

                    // S
                    case 83:
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
