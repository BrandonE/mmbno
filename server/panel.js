'use strict';

var common = require(__dirname + '/common');

module.exports = function Panel(io, config, game, field, row, col) {
    var self = this;

    this.row = row;
    this.col = col;
    this.character = null;
    this.stolen = false;
    this.type = 'normal';

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

    this.crackOrBreak = function crackOrBreak() {
        if (self.type === 'cracked') {
            self.setType('broken');
        } else if (['blank', 'broken', 'metal'].indexOf(self.type) === -1) {
            self.setType('cracked');
        }
    };

    this.handleRoad = function handleRoad() {
        var character = self.character,
            type = self.type;

        if (character && ['up', 'down', 'left', 'right'].indexOf(type) > -1) {
            self.roadPanelTimeout = setTimeout(
                function() {
                    // Confirm that the character and panel type remained the same.
                    if (self.character === character && self.type === type) {
                        if (character.getPlayerNum() === 2) {
                            if (type === 'left') {
                                type = 'right';
                            } else if (type === 'right') {
                                type = 'left';
                            }
                        }

                        self.character.move(type, 1);
                    }
                },
                500
            );
        }
    };

    this.hit = function hit(power, element, hitHook) {
        if (self.character) {
            self.character.takeDamage(power, element);

            if (self.type === 'grass' && element === 'fire') {
                self.setType('normal');
            }

            if (['up', 'down', 'left', 'right'].indexOf(self.type) > -1 && element === 'wood') {
                self.setType('normal');
            }

            if (hitHook) {
                hitHook(self);
            }

            return true;
        } else {
            return false;
        }
    };

    this.isInBounds = function isInBounds(player) {
        return common.isPanelInBounds(config, field.getGrid(), player.getPlayerNum(), self.row, self.col);
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
