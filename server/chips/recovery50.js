'use strict';

var RecoveryType = require(__dirname + '/types/recovery'),
    extend = require(__dirname + '/extend');

function Recovery50Constructor(io, config, game, character) {
    this.properties.codes = ['C', 'M', 'P', '*'];
    this.properties.description = 'Recovers 50HP';
    this.properties.health = 50;
    this.properties.name = 'Recovery +50';
    this.properties.short = 'Recov50';
}

module.exports = function Recovery50(io, config, game, character) {
    return extend(Recovery50Constructor, RecoveryType, io, config, game, character);
};
