'use strict';

var Game = require(__dirname + '/game');

module.exports = function(config) {
    var games = [];

    return {
        attach : function attach(io) {
            io.on('connection', function (socket) {
                var game = getAvailableGame();

                if (!game) {
                    game = new Game(io, config);
                    games.push(game);
                }

                socket.join(game.getId());

                game.connect(socket);

                socket.on('disconnect', function() {
                    game.disconnect(socket.id);
                });

                socket.on('move', function(direction) {
                    var player = game.getPlayerById(socket.id);

                    if (player) {
                        player.move(direction);
                    }
                });

                socket.on('buster', function() {
                    var player = game.getPlayerById(socket.id);

                    if (player) {
                        player.busterShot();
                    }
                });
            });
        }
    };

    function getAvailableGame() {
        var game,
            g;

        for (g in games) {
            game = games[g];

            if (game.isAvailable()) {
                return game;
            }
        }

        return null;
    }
};
