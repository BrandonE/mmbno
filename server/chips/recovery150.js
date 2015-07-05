'use strict';

var RecoveryType = require(__dirname + '/types/recovery'),
    extend = require(__dirname + '/extend');

function Recovery150Constructor(io, config, game, character) {
    this.properties.codes = ['J', 'M', 'T'];
    this.properties.description = 'Recovers 150HP';
    this.properties.health = 150;
    this.properties.name = 'Recovery +150';
    this.properties.short = 'Recov150';
    this.properties.stars = 3;
}

module.exports = function Recovery150(io, config, game, character) {
    return extend(Recovery150Constructor, RecoveryType, io, config, game, character);
};
