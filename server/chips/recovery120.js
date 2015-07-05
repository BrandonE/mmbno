'use strict';

var RecoveryType = require(__dirname + '/types/recovery'),
    extend = require(__dirname + '/extend');

function Recovery120Constructor(io, config, game, character) {
    this.properties.codes = ['F', 'P', 'S'];
    this.properties.description = 'Recovers 120HP';
    this.properties.health = 120;
    this.properties.name = 'Recovery +120';
    this.properties.short = 'Recov120';
    this.properties.stars = 2;
}

module.exports = function Recovery120(io, config, game, character) {
    return extend(Recovery120Constructor, RecoveryType, io, config, game, character);
};
