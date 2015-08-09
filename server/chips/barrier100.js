'use strict';

var BarrierType = require(__dirname + '/types/barrier'),
    extend = require(__dirname + '/extend');

function Barrier100Constructor(io, config, game, character, code) {
    this.properties.codes = ['A', 'F', 'R', '*'];
    this.properties.description = 'Nullifies 100HP of damage';
    this.properties.health = 100;
    this.properties.name = 'Barrier 100';
    this.properties.short = 'Barr100';
    this.properties.stars = 3;
}

module.exports = function Barrier100(io, config, game, character, code) {
    return extend(Barrier100Constructor, BarrierType, io, config, game, character, code);
};
