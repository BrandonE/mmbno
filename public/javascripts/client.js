var socket = io(),
    chipSelectionTime = 0,
    config,
    game,
    chips,
    canvas,
    ctx,
    ready = false,
    background,
    grid,
    lastTime;

function draw() {
    var now = Date.now(),
        dt = (now - lastTime) / 1000.0,
        col,
        player,
        p;

    ctx.fillStyle = background;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.save();
    ctx.translate(0, 100);
    grid.render(ctx);
    ctx.restore();

    if (game) {
        for (p in game.players) {
            if (game.players.hasOwnProperty(p)) {
                player = game.players[p];

                if (player && player.health) {
                    col = player.col;

                    if (game.clientPlayerNum === 2) {
                        col = config.cols - col - 1;
                    }

                    player.x = 27 + (col * 40);
                    player.y = 75 + (player.row * 25);

                    player.sprite.update(dt);
                    ctx.save();
                    ctx.translate(player.x, player.y);

                    player.sprite.render(ctx);
                    ctx.restore();
                }
            }
        }
    }

    lastTime = now;
    getRequestAnimationFrame()(draw);

    $('#game').text(gameToString(config, game, game.clientPlayerNum));
}

function getRequestAnimationFrame() {
    return window.requestAnimationFrame ||
        window.webkitRequestAnimationFrame ||
        window.mozRequestAnimationFrame    ||
        window.oRequestAnimationFrame      ||
        window.msRequestAnimationFrame     ||
        function(callback){
            window.setTimeout(callback, 1000 / 60);
        };
}

function setPlayerSprite(player) {
    if (game.clientPlayerNum === player.playerNum) {
        player.sprite = new Sprite('/images/spritesheets/megaman.png', -2, 0, 50, 64);
    } else {
        player.sprite = new Sprite('/images/spritesheets/megaman_flipped.png', 802, 0, 50, 64);
    }
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

            canvas = document.createElement('canvas');
            ctx = canvas.getContext('2d');

            canvas.width = 300;
            canvas.height = 205;
            document.body.appendChild(canvas);

            Image.load([
                '/images/backgrounds/acdc.png',
                '/images/spritesheets/panels_mmbn6.gif',
                '/images/spritesheets/megaman.png',
                '/images/spritesheets/megaman_flipped.png',
            ]);

            Image.onReady(function() {
                ready = true;

                background = ctx.createPattern(Image.get('/images/backgrounds/acdc.png'), 'repeat');
                grid = new Sprite('/images/spritesheets/panels_mmbn6.gif', 0, 0, 480, 100);

                lastTime = Date.now();

                draw();
            });
        });

        socket.on('user connected', function(playerNum, gameSent) {
            var player,
                playerIndex,
                p;

            if (game) {
                if (playerNum) {
                    playerIndex = playerNum - 1;
                    player = gameSent.players[playerIndex];

                    game.players[playerIndex] = player;
                    game.field[player.row][player.col].character = player;

                    setPlayerSprite(player);
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

                for (p in game.players) {
                    if (game.players.hasOwnProperty(p)) {
                        player = game.players[p];

                        if (player) {
                            setPlayerSprite(player);
                        }
                    }
                }
            }

            if (ready) {
                draw();
            }
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

            if (ready) {
                draw();
            }
        });

        socket.on('active connections', function(activeConnections) {
            $('#activeConnections').text(activeConnections);
        });

        socket.on('chips', function(chipsSent) {
            chips = chipsSent;
            showChips();

            chipSelectionTime = Math.floor(config.chipSelectionInterval / 1000);
            $('#chipSelectionTime').text(chipSelectionTime);
        });

        socket.on('chip used', function(playerNum, chip) {
            var c;

            if (playerNum && game.clientPlayerNum === playerNum) {
                for (c in chips) {
                    if (chips.hasOwnProperty(c)) {
                        if (chip.name === chips[c].name) {
                            chips.splice(c, 1);
                            break;
                        }
                    }
                }

                showChips();
            }
        });

        socket.on('panel type changed', function(panelRow, panelCol, type) {
            game.field[panelRow][panelCol].type = type;

            if (ready) {
                draw();
            }
        });

        socket.on('panel flip stolen', function(panelRow, panelCol) {
            game.field[panelRow][panelCol].stolen = !game.field[panelRow][panelCol].stolen;

            if (ready) {
                draw();
            }
        });

        socket.on('player damage handler changed', function(playerNum, damageHandler, priority) {
            var player;

            if (playerNum) {
                player = game.players[playerNum - 1];
                player.damageHandlers[priority] = damageHandler;

                if (ready) {
                    draw();
                }
            }
        });

        socket.on('player health changed', function(playerNum, health) {
            var player;

            if (playerNum) {
                player = game.players[playerNum - 1];
                player.health = health;

                if (ready) {
                    draw();
                }
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

                if (ready) {
                    if (game.clientPlayerNum === playerNum) {
                        player.sprite = new Sprite(
                            '/images/spritesheets/megaman.png', -2, 0, 50, 64, 16, [3, 2, 1, 0], 'right', true
                        );
                    } else {
                        player.sprite = new Sprite(
                            '/images/spritesheets/megaman_flipped.png', 802, 0, 50, 64, 16, [3, 2, 1, 0], 'left', true
                        );
                    }

                    draw();
                }
            }
        });

        socket.on('player status added', function(playerNum, status) {
            var player,
                index;

            if (playerNum) {
                player = game.players[playerNum - 1];
                index = player.statuses.indexOf(status);

                if (index === -1) {
                    player.statuses.push(status);
                }

                if (ready) {
                    if (status === 'attacking') {
                        if (game.clientPlayerNum === playerNum) {
                            player.sprite = new Sprite(
                                '/images/spritesheets/megaman.png', 194, 0, 55, 64
                            );
                        } else {
                            player.sprite = new Sprite(
                                '/images/spritesheets/megaman_flipped.png', 606, 0, 55, 64
                            );
                        }
                    }

                    draw();
                }
            }
        });

        socket.on('player status removed', function(playerNum, status) {
            var player,
                index;

            if (playerNum) {
                player = game.players[playerNum - 1];
                index = player.statuses.indexOf(status);

                if (index > -1) {
                    player.statuses.splice(index, 1);
                }

                if (ready) {
                    if (status === 'attacking') {
                        setPlayerSprite(player);
                    }

                    draw();
                }
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

        $('#chipSelectionTime').text(chipSelectionTime);

        setInterval(function chipSelectionInterval() {
            chipSelectionTime--;

            if (chipSelectionTime < 0) {
                chipSelectionTime = 0;
            }
            
            $('#chipSelectionTime').text(chipSelectionTime);
        }, 1000);
    }
);
