'use strict';

var SpreaderType = require(__dirname + '/types/spreader'),
    extend = require(__dirname + '/extend');

function Spreader2Constructor(io, config, game, character) {
    this.properties.codes = ['A', 'B', 'C', '*'];
    this.properties.description = 'Spreads damage to adjacent panels';
    this.properties.name = 'Spreader 2';
    this.properties.short = 'Spreadr2';
    this.properties.power = 60;
    this.properties.stars = 2;
}

module.exports = function Spreader2(io, config, game, character) {
    return extend(Spreader2Constructor, SpreaderType, io, config, game, character);
};
