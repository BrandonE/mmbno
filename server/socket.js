'use strict';

var Character = require(__dirname + '/character'),
    Field = require(__dirname + '/field');

module.exports = function(config) {
    var IO = null,
        field,
        players = [null, null];

    function connect(io, socket) {
        var playerNum = -1,
            player,
            p,
            playersToSend = [],
            playerToSend;

        if (!players[0]) {
            playerNum = 1;
        } else if (!players[1]) {
            playerNum = 2;
        }

        if (playerNum !== -1) {
            player = new Character(io, config, field, socket.id, playerNum);
            players[playerNum - 1] = player;

            for (p in players) {
                playerToSend = players[p];

                if (playerToSend) {
                    playerToSend = players[p].toSendable();
                }

                playersToSend.push(playerToSend);
            }

            IO.emit('user connected', playerNum, playersToSend);

            field.draw();
            console.log('user `' + socket.id + '` connected');
        }
    }

    function disconnect(id) {
        var player = getPlayerById(id),
            playerNum;

        if (player) {
            playerNum = player.getPlayerNum();

            IO.emit('user disconnected', playerNum);

            player.leaveField();
            delete players[playerNum - 1];

            field.draw();
            console.log('user `' + id + '` disconnected');
        }
    }

    function attach(io) {
        IO = io;

        io.on('connection', function (socket) {
            if (!field) {
                field = new Field(io, config, players);
            }

            connect(io, socket);

            socket.on('disconnect', function() {
                disconnect(socket.id);
            });

            socket.on('move', function(direction) {
                var player = getPlayerById(socket.id);

                if (player) {
                    player.move(direction);
                }
            });

            socket.on('buster', function() {
                var player = getPlayerById(socket.id);

                if (player) {
                    player.busterShot();
                }
            });
        });
    }

    return {
        attach : attach
    };

    function getPlayerById(id) {
        var player,
            p;

        for (p in players) {
            player = players[p];

            if (player.getId() === id) {
                return player;
            }
        }

        return null;
    }
};
