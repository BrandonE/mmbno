'use strict';

var SpreaderType = require(__dirname + '/types/spreader'),
    extend = require(__dirname + '/extend');

function Spreader3Constructor(io, config, game, character) {
    this.properties.codes = ['Q', 'R', 'S', '*'];
    this.properties.description = 'Spreads damage to adjacent panels';
    this.properties.name = 'Spreader 3';
    this.properties.short = 'Spreadr3';
    this.properties.power = 90;
    this.properties.stars = 3;
}

module.exports = function Spreader3(io, config, game, character) {
    return extend(Spreader3Constructor, SpreaderType, io, config, game, character);
};
