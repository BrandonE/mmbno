'use strict';

var uuid = require('uuid'),
    Character = require(__dirname + '/character'),
    Field = require(__dirname + '/field');

module.exports = function Game(io, config) {
    var self = this;

    this.id = uuid.v4();
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
            console.log('player `' + socket.id + '` connected to ' + self.id);
        } else {
            console.log('spectator `' + socket.id + '` connected to ' + self.id);
        }

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
            console.log('player `' + id + '` disconnected from ' + self.id);
        } else {
            console.log('spectator `' + id + '` disconnected from ' + self.id);
        }
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
