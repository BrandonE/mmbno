'use strict';

var CannonType = require(__dirname + '/types/cannon');

function CannonConstructor(io, config, character) {
    this.properties.codes = ['A', 'B', 'C', '*'];
    this.properties.description = 'Cannon to attack 1 enemy';
    this.properties.name = 'Cannon';
    this.properties.short = 'Cannon';
    this.properties.power = 40;
}

module.exports = function Cannon(io, config, character) {
    CannonConstructor.prototype = new CannonType(io, config, character);
    CannonConstructor.constructor = CannonConstructor;
    return new CannonConstructor(io, config, character);
};
