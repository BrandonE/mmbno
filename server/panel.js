'use strict';

module.exports = function Panel(io, field, row, col) {
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
        io.sockets.emit('panel changed', self.toSendable());
        field.draw();
    };

    this.getTime = function getTime() {
        return self.time;
    };

    this.setTime = function setTime(time) {
        self.time = time;
    };

    this.toSendable = function toSendable() {
        return {
            row       : self.row,
            col       : self.col,
            stolen    : self.stolen,
            status    : self.status
        };
    };
};
