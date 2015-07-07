'use strict';

var SpreaderType = require(__dirname + '/types/spreader'),
    extend = require(__dirname + '/extend');

function Spreader1Constructor(io, config, game, character) {
    this.properties.codes = ['L', 'M', 'N', '*'];
    this.properties.description = 'Spreads damage to adjacent panels';
    this.properties.name = 'Spreader 1';
    this.properties.short = 'Spreadr1';
    this.properties.power = 30;
}

module.exports = function Spreader1(io, config, game, character) {
    return extend(Spreader1Constructor, SpreaderType, io, config, game, character);
};
