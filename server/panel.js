'use strict';

module.exports = function Panel(io, game, field, row, col) {
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

    this.getStolen = function getStolen() {
        return self.stolen;
    };

    this.setStolen = function setStolen(stolen) {
        self.stolen = stolen;
    };

    this.getType = function getType() {
        return self.type;
    };

    this.setType = function setType(type) {
        self.type = type;
        io.to(game.getId()).emit('panel type changed', type);
        field.draw();
    };

    this.getTime = function getTime() {
        return self.time;
    };

    this.setTime = function setTime(time) {
        self.time = time;
    };

    this.shot = function shot(power, element) {
        if (self.character) {
            self.character.takeDamage(power, element);

            if (self.getType() === 'grass' && element === 'fire') {
                self.setType('normal');
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
