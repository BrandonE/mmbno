'use strict';

var TankCannonType = require(__dirname + '/types/tankCannon'),
    extend = require(__dirname + '/extend');

function TankCannon1Constructor(io, config, game, character, code) {
    this.properties.codes = ['A', 'G', 'R'];
    this.properties.description = '3-square blast if hits end row';
    this.properties.name = 'Tank Cannon 1';
    this.properties.short = 'TankCan1';
    this.properties.power = 120;
}

module.exports = function TankCannon1(io, config, game, character, code) {
    return extend(TankCannon1Constructor, TankCannonType, io, config, game, character, code);
};
