'use strict';

var Chip = require(__dirname + '/..'),
    extend = require(__dirname + '/../extend');

function CannonConstructor(io, config, game, character) {
    var self = this;

    this.use = function use() {
        character.shoot(self.properties.power, self.properties.element, true);
    };
}

module.exports = function Cannon(io, config, game, character) {
    return extend(CannonConstructor, Chip, io, config, game, character);
};
