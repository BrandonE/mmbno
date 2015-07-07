'use strict';

var VulcanType = require(__dirname + '/types/vulcan'),
    extend = require(__dirname + '/extend');

function Vulcan3Constructor(io, config, game, character) {
    this.properties.codes = ['A', 'G', 'R'];
    this.properties.description = '5-Shot to pierce one panel';
    this.properties.name = 'Vulcan 3';
    this.properties.short = 'Vulcan3';
    this.properties.bullets = 5;
    this.properties.power = 20;
    this.properties.stars = 3;
}

module.exports = function Vulcan3(io, config, game, character) {
    return extend(Vulcan3Constructor, VulcanType, io, config, game, character);
};
