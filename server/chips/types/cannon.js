'use strict';

var Chip = require(__dirname + '/..'),
    extend = require(__dirname + '/../extend');

function CannonConstructor(io, config, character) {
    var self = this;

    this.use = function use() {
        character.shoot(self.properties.power, self.properties.element);
    };
}

module.exports = function Cannon(io, config, character) {
    return extend(CannonConstructor, Chip, io, config, character);
};
