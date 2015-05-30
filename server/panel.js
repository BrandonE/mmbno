'use strict';

module.exports = function Panel(io, field) {
    var self = this;

    this.character = null;
    this.stolen = false;
    this.status = 'normal';
    this.time = 0;

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
    };

    this.getTime = function getTime() {
        return self.time;
    };

    this.setTime = function setTime(time) {
        self.time = time;
    };

    this.toSendable = function toSendable() {
        return {
            stolen    : self.stolen,
            status    : self.status,
            time      : self.time
        };
    };
};
