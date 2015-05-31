'use strict';

var Chip = require(__dirname + '/..');

function CannonConstructor(io, config, character) {
    var self = this;

    this.use = function use() {
        character.shoot(self.properties.power, self.properties.element);
    };
}

module.exports = function Cannon(io, config, character) {
    CannonConstructor.prototype = new Chip(io, config, character);
    CannonConstructor.constructor = CannonConstructor;
    return new CannonConstructor(io, config, character);
};
