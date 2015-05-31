'use strict';

var AttackPlusType = require(__dirname + '/types/attackPlus'),
    extend = require(__dirname + '/extend');

function AttackPlus10Constructor(io, config, character) {
    this.properties.codes = ['*'];
    this.properties.description = '+10 for selected attack chip';
    this.properties.name = 'Attack +10';
    this.properties.short = 'Atk+10';
    this.properties.element = 'plus';
    this.properties.powerPlus = 10;
}

module.exports = function AttackPlus10(io, config, character) {
    return extend(AttackPlus10Constructor, AttackPlusType, io, config, character);
};
