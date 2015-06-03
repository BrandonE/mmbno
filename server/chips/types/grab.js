'use strict';

var Chip = require(__dirname + '/..'),
    extend = require(__dirname + '/../extend');

function GrabConstructor(io, config, game, character) {
    var self = this;

    this.damage = 10;
}

module.exports = function Grab(io, config, game, character) {
    return extend(GrabConstructor, Chip, io, config, game, character);
};
