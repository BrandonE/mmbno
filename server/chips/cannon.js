'use strict';

var CannonType = require(__dirname + '/types/cannon'),
    extend = require(__dirname + '/extend');

function CannonConstructor(io, config, game, character) {
    this.properties.codes = ['A', 'B', 'C', '*'];
    this.properties.description = 'Cannon to attack 1 enemy';
    this.properties.name = 'Cannon';
    this.properties.short = 'Cannon';
    this.properties.power = 40;
}

module.exports = function Cannon(io, config, game, character) {
    return extend(CannonConstructor, CannonType, io, config, game, character);
};
