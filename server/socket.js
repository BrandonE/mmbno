'use strict';

var Game = require(__dirname + '/game');

module.exports = function(config) {
    var games = [],
        activeConnections = 0;

    return {
        attach : function attach(io) {
            io.on('connection', function (socket) {
                var game = getAvailableGame();

                if (!game) {
                    game = new Game(io, config, games.length + 1);
                    games.push(game);
                }

                socket.join(game.getId());

                game.connect(socket);
                activeConnections++;
                io.emit('active connections', activeConnections);
                console.log('Active Connections: ' + activeConnections);

                socket.on('disconnect', function() {
                    game.disconnect(socket.id);
                    activeConnections--;
                    io.emit('active connections', activeConnections);
                    console.log('Active Connections: ' + activeConnections);
                });

                socket.on('move', function(direction) {
                    var player = game.getPlayerById(socket.id);

                    if (player && player.getHealth()) {
                        player.move(direction);
                    }
                });

                socket.on('buster', function() {
                    var player = game.getPlayerById(socket.id);

                    if (player && player.getHealth()) {
                        player.busterShot();
                    }
                });

                socket.on('use chip', function() {
                    var player = game.getPlayerById(socket.id);

                    if (player && player.getHealth()) {
                        player.useChip();
                    }
                });
            });
        }
    };

    function getAvailableGame() {
        var game,
            g;

        for (g = 0; g < games.length; g++) {
            game = games[g];

            if (game.isAvailable()) {
                return game;
            }
        }

        return null;
    }
};
