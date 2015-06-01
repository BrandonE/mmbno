'use strict';

module.exports = function Panel(io, game, field, row, col) {
    var self = this;

    this.row = row;
    this.col = col;
    this.character = null;
    this.stolen = false;
    this.status = 'normal';
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

    this.getStatus = function getStatus() {
        return self.status;
    };

    this.setStatus = function setStatus(status) {
        self.status = status;
        io.to(game.getId()).emit('panel changed', self.toSendable());
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

            if (self.getStatus() === 'grass' && element === 'fire') {
                self.setStatus('normal');
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
            status    : self.status
        };
    };
};
