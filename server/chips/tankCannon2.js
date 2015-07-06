'use strict';

var TankCannonType = require(__dirname + '/types/tankCannon'),
    extend = require(__dirname + '/extend');

function TankCannon2Constructor(io, config, game, character) {
    this.properties.codes = ['L', 'S', 'V'];
    this.properties.description = '3-square blast if hits end row';
    this.properties.name = 'Tank Cannon 2';
    this.properties.short = 'TankCan2';
    this.properties.power = 160;
}

module.exports = function TankCannon2(io, config, game, character) {
    return extend(TankCannon2Constructor, TankCannonType, io, config, game, character);
};
