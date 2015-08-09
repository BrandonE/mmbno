'use strict';

var TankCannonType = require(__dirname + '/types/tankCannon'),
    extend = require(__dirname + '/extend');

function TankCannon3Constructor(io, config, game, character, code) {
    this.properties.codes = ['B', 'M', 'P'];
    this.properties.description = '3-square blast if hits end row';
    this.properties.name = 'Tank Cannon 3';
    this.properties.short = 'TankCan3';
    this.properties.power = 200;
}

module.exports = function TankCannon3(io, config, game, character, code) {
    return extend(TankCannon3Constructor, TankCannonType, io, config, game, character, code);
};
