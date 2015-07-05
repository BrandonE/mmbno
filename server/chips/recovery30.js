'use strict';

var RecoveryType = require(__dirname + '/types/recovery'),
    extend = require(__dirname + '/extend');

function Recovery30Constructor(io, config, game, character) {
    this.properties.codes = ['E', 'L', 'Q', '*'];
    this.properties.description = 'Recovers 30HP';
    this.properties.health = 30;
    this.properties.name = 'Recovery +30';
    this.properties.short = 'Recov30';
}

module.exports = function Recovery30(io, config, game, character) {
    return extend(Recovery30Constructor, RecoveryType, io, config, game, character);
};
