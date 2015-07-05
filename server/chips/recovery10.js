'use strict';

var RecoveryType = require(__dirname + '/types/recovery'),
    extend = require(__dirname + '/extend');

function Recovery10Constructor(io, config, game, character) {
    this.properties.codes = ['A', 'D', 'L', '*'];
    this.properties.description = 'Recovers 10HP';
    this.properties.health = 10;
    this.properties.name = 'Recovery +10';
    this.properties.short = 'Recov10';
}

module.exports = function Recovery10(io, config, game, character) {
    return extend(Recovery10Constructor, RecoveryType, io, config, game, character);
};
