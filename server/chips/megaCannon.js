'use strict';

var CannonType = require(__dirname + '/types/cannon'),
    extend = require(__dirname + '/extend');

function MegaCannonConstructor(io, config, game, character) {
    this.properties.codes = ['R', 'S', 'T', '*'];
    this.properties.description = 'Cannon to attack 1 enemy';
    this.properties.name = 'Mega Cannon';
    this.properties.short = 'M-Cannon';
    this.properties.power = 180;
    this.properties.stars = 3;
}

module.exports = function MegaCannon(io, config, game, character) {
    return extend(MegaCannonConstructor, CannonType, io, config, game, character);
};
