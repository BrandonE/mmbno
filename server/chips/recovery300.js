'use strict';

var RecoveryType = require(__dirname + '/types/recovery'),
    extend = require(__dirname + '/extend');

function Recovery300Constructor(io, config, game, character) {
    this.properties.codes = ['J', 'O', 'Y'];
    this.properties.description = 'Recovers 300HP';
    this.properties.health = 300;
    this.properties.name = 'Recovery +300';
    this.properties.short = 'Recov300';
    this.properties.stars = 4;
}

module.exports = function Recovery300(io, config, game, character) {
    return extend(Recovery300Constructor, RecoveryType, io, config, game, character);
};
