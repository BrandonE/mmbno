'use strict';

var BanishType = require(__dirname + '/types/banish'),
    extend = require(__dirname + '/extend');

function GrabRevengeConstructor(io, config, game, character) {
    this.properties.codes = ['I', 'Q', 'Z'];
    this.properties.damage = 40;
    this.properties.description = '40 damage for every stolen square';
    this.properties.name = 'Grab Revenge';
    this.properties.short = 'GrabRvng';
    this.properties.stars = 4;
}

module.exports = function GrabRevenge(io, config, game, character) {
    return extend(GrabRevengeConstructor, BanishType, io, config, game, character);
};
