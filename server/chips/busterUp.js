'use strict';

var Chip = require(__dirname + '/'),
    extend = require(__dirname + '/extend');

function BusterUpConstructor(io, config, game, character) {
    var self = this;

    this.properties.codes = ['*'];
    this.properties.description = 'Power goes up by 1';
    this.properties.element = 'plus';
    this.properties.name = 'Buster Up';
    this.properties.short = 'BusterUp';
    this.properties.plus = 1;
    this.properties.stars = 2;

    this.use = function use() {
        character.boostBusterPower(self.properties.plus);
    };
}

module.exports = function BusterUp(io, config, game, character) {
    return extend(BusterUpConstructor, Chip, io, config, game, character);
};
