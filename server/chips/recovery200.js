'use strict';

var RecoveryType = require(__dirname + '/types/recovery'),
    extend = require(__dirname + '/extend');

function Recovery200Constructor(io, config, game, character) {
    this.properties.codes = ['I', 'Q', 'Z'];
    this.properties.description = 'Recovers 200HP';
    this.properties.health = 200;
    this.properties.name = 'Recovery +200';
    this.properties.short = 'Recov200';
    this.properties.stars = 3;
}

module.exports = function Recovery200(io, config, game, character) {
    return extend(Recovery200Constructor, RecoveryType, io, config, game, character);
};
