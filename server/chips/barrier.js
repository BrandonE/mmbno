'use strict';

var BarrierType = require(__dirname + '/types/barrier'),
    extend = require(__dirname + '/extend');

function BarrierConstructor(io, config, game, character) {
    this.properties.codes = ['A', 'F', 'R', '*'];
    this.properties.description = 'Nullifies 10HP of damage';
    this.properties.health = 10;
    this.properties.name = 'Barrier';
    this.properties.short = 'Barrier';
    this.properties.stars = 2;
}

module.exports = function Barrier(io, config, game, character) {
    return extend(BarrierConstructor, BarrierType, io, config, game, character);
};
