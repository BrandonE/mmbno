'use strict';

var CannonType = require(__dirname + '/types/cannon'),
    extend = require(__dirname + '/extend');

function HighCannonConstructor(io, config, game, character) {
    this.properties.codes = ['L', 'M', 'N', '*'];
    this.properties.description = 'Cannon to attack 1 enemy';
    this.properties.name = 'High Cannon';
    this.properties.short = 'HiCannon';
    this.properties.power = 100;
    this.properties.stars = 2;
}

module.exports = function HighCannon(io, config, game, character) {
    return extend(HighCannonConstructor, CannonType, io, config, game, character);
};
