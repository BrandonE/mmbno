'use strict';

var BarrierType = require(__dirname + '/types/barrier'),
    extend = require(__dirname + '/extend');

function Barrier200Constructor(io, config, game, character, code) {
    this.properties.codes = ['A', 'F', 'R', '*'];
    this.properties.description = 'Nullifies 200HP of damage';
    this.properties.health = 100;
    this.properties.name = 'Barrier 200';
    this.properties.short = 'Barr200';
    this.properties.stars = 4;
}

module.exports = function Barrier200(io, config, game, character, code) {
    return extend(Barrier200Constructor, BarrierType, io, config, game, character, code);
};
