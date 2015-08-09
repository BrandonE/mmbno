'use strict';

var VulcanType = require(__dirname + '/types/vulcan'),
    extend = require(__dirname + '/extend');

function Vulcan1Constructor(io, config, game, character, code) {
    this.properties.codes = ['B', 'D', 'S', '*'];
    this.properties.description = '3-Shot to pierce one panel';
    this.properties.name = 'Vulcan 1';
    this.properties.short = 'Vulcan1';
    this.properties.bullets = 3;
    this.properties.power = 10;
}

module.exports = function Vulcan1(io, config, game, character, code) {
    return extend(Vulcan1Constructor, VulcanType, io, config, game, character, code);
};
