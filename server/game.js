'use strict';

var uuid = require('uuid'),
    Character = require(__dirname + '/character'),
    Field = require(__dirname + '/field');

module.exports = function Game(io, config, num) {
    var self = this;

    this.id = uuid.v4();
    this.num = num;
    this.players = [null, null];
    this.field = new Field(io, config, self);

    this.getId = function getId() {
        return self.id;
    };

    this.getField = function getField() {
        return self.field;
    };

    this.getPlayers = function getPlayers() {
        return self.players;
    };

    this.getPlayerById = function getPlayerById(id) {
        var player,
            p;

        for (p in self.players) {
            player = self.players[p];

            if (player.getId() === id) {
                return player;
            }
        }

        return null;
    };

    this.isAvailable = function isAvailable() {
        return (!this.players[0] || !this.players[1]);
    };

    this.connect = function connect(socket) {
        var playerNum = 0,
            player;

        if (!self.players[0]) {
            playerNum = 1;
        } else if (!self.players[1]) {
            playerNum = 2;
        }

        if (playerNum) {
            player = new Character(io, config, self, socket.id, playerNum);
            self.players[playerNum - 1] = player;

            self.field.draw();
        }

        console.log(self.connectionMessage(playerNum, socket.id));
        io.to(self.id).emit('user connected', playerNum, self.toSendable());
    };

    this.disconnect = function disconnect(id) {
        var player = self.getPlayerById(id),
            playerNum;

        if (player) {
            playerNum = player.getPlayerNum();

            io.to(self.id).emit('user disconnected', playerNum);

            player.leaveField();
            delete self.players[playerNum - 1];

            self.field.draw();
        }

        console.log(self.connectionMessage(playerNum, id, true));
    };

    this.connectionMessage = function connectionMessage(playerNum, id, disconnected) {
        var message;

        if (playerNum) {
            message = 'Player #' + playerNum + ' (' + id + ')';
        } else {
            message = 'Spectator (' + socket.id + ')';
        }

        if (disconnected) {
            message += ' disconnected from';
        } else {
            message += ' connected to';
        }

        message += ' Game #' + self.num + ' (' + self.id + ')';

        return message;
    };

    this.toSendable = function toSendable() {
        var playersToSend = [],
            playerToSend,
            p;

        for (p in self.players) {
            playerToSend = self.players[p];

            if (playerToSend) {
                playerToSend = self.players[p].toSendable();
            }

            playersToSend.push(playerToSend);
        }

        return {
            field   : self.field.toSendable(),
            players : playersToSend
        };
    };
};
