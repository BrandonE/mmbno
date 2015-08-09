'use strict';

var VulcanType = require(__dirname + '/types/vulcan'),
    extend = require(__dirname + '/extend');

function SuperVulcanConstructor(io, config, game, character, code) {
    this.properties.codes = ['V'];
    this.properties.description = '10-shot vulcan cannon';
    this.properties.name = 'Super Vulcan';
    this.properties.short = 'SuprVulc';
    this.properties.bullets = 10;
    this.properties.power = 20;
    this.properties.stars = 4;
}

module.exports = function SuperVulcan(io, config, game, character, code) {
    return extend(SuperVulcanConstructor, VulcanType, io, config, game, character, code);
};
