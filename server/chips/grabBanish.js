'use strict';

var BanishType = require(__dirname + '/types/banish'),
    extend = require(__dirname + '/extend');

function GrabBanishConstructor(io, config, game, character, code) {
    this.properties.codes = ['B', 'M', 'S'];
    this.properties.damage = 20;
    this.properties.description = '20 damage for every stolen square';
    this.properties.name = 'Grab Banish';
    this.properties.short = 'GrabBnsh';
    this.properties.stars = 3;
}

module.exports = function GrabBanish(io, config, game, character, code) {
    return extend(GrabBanishConstructor, BanishType, io, config, game, character, code);
};
