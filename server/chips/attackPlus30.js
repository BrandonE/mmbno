'use strict';

var AttackPlusType = require(__dirname + '/types/attackPlus'),
    extend = require(__dirname + '/extend');

function AttackPlus10Constructor(io, config, character) {
    this.properties.codes = ['*'];
    this.properties.description = '+30 for selected attack chip';
    this.properties.name = 'Attack +30';
    this.properties.short = 'Atk+30';
    this.properties.element = 'plus';
    this.properties.powerPlus = 30;
    this.properties.stars = 4;
}

module.exports = function AttackPlus10(io, config, character) {
    return extend(AttackPlus10Constructor, AttackPlusType, io, config, character);
};
