'use strict';

var RecoveryType = require(__dirname + '/types/recovery'),
    extend = require(__dirname + '/extend');

function Recovery80Constructor(io, config, game, character) {
    this.properties.codes = ['H', 'K', 'V', '*'];
    this.properties.description = 'Recovers 80HP';
    this.properties.health = 80;
    this.properties.name = 'Recovery +80';
    this.properties.short = 'Recov80';
    this.properties.stars = 2;
}

module.exports = function Recovery80(io, config, game, character) {
    return extend(Recovery80Constructor, RecoveryType, io, config, game, character);
};
