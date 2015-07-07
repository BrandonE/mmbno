'use strict';

var VulcanType = require(__dirname + '/types/vulcan'),
    extend = require(__dirname + '/extend');

function Vulcan2Constructor(io, config, game, character) {
    this.properties.codes = ['D', 'F', 'L'];
    this.properties.description = '4-Shot to pierce one panel';
    this.properties.name = 'Vulcan 2';
    this.properties.short = 'Vulcan2';
    this.properties.bullets = 4;
    this.properties.power = 15;
    this.properties.stars = 2;
}

module.exports = function Vulcan2(io, config, game, character) {
    return extend(Vulcan2Constructor, VulcanType, io, config, game, character);
};
