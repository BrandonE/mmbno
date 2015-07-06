'use strict';

var common = require(__dirname + '/common');

module.exports = function Panel(io, config, game, field, row, col) {
    var self = this;

    this.row = row;
    this.col = col;
    this.character = null;
    this.stolen = false;
    this.type = 'normal';
    this.time = 0;

    this.getRow = function getRow() {
        return self.row;
    };

    this.getCol = function getCol() {
        return self.col;
    };

    this.getCharacter = function getCharacter() {
        return self.character;
    };

    this.setCharacter = function setCharacter(character) {
        self.character = character;
    };

    this.isStolen = function isStolen() {
        return self.stolen;
    };

    this.flipStolen = function flipStolen() {
        self.stolen = !self.stolen;
        io.to(game.getId()).emit('panel flip stolen', self.row, self.col);
        field.draw();
    };

    this.getType = function getType() {
        return self.type;
    };

    this.setType = function setType(type) {
        self.type = type;
        io.to(game.getId()).emit('panel type changed', self.row, self.col, type);
        field.draw();
    };

    this.getTime = function getTime() {
        return self.time;
    };

    this.setTime = function setTime(time) {
        self.time = time;
    };

    this.handleRoad = function handleRoad() {
        var character = self.character,
            type = self.type;

        if (character && ['up', 'down', 'left', 'right'].indexOf(self.type) > -1) {
            self.roadPanelTimeout = setTimeout(
                function() {
                    // Confirm that the character remained on this panel.
                    if (self.character === character) {
                        if (character.getPlayerNum() === 2) {
                            if (type === 'left') {
                                type = 'right';
                            } else if (type === 'right') {
                                type = 'left';
                            }
                        }

                        self.character.move(type, 1, 1);
                    }
                },
                500
            );
        }
    };

    this.isInBounds = function isInBounds(player) {
        return common.isPanelInBounds(config, field.getGrid(), player.getPlayerNum(), self.row, self.col);
    };

    this.shot = function shot(power, element, shotHook) {
        if (self.character) {
            self.character.takeDamage(power, element);

            if (self.getType() === 'grass' && element === 'fire') {
                self.setType('normal');
            }

            if (shotHook) {
                shotHook(self);
            }

            return true;
        } else {
            return false;
        }
    };

    this.toSendable = function toSendable() {
        var character = self.character;

        if (character) {
            character = character.toSendable();
        }

        return {
            row       : self.row,
            col       : self.col,
            character : character,
            stolen    : self.stolen,
            type      : self.type
        };
    };
};
