'use strict';

module.exports = function Chip(io, config, character) {
    var self = this;

    this.properties = {
        codes          : [],
        description    : '',
        name           : '',
        short          : '',
        power          : null,
        powerPlus      : null,
        element        : 'none',
        classification : 'standard',
        priority       : 0,
        stars          : 1
    };

    this.getPower = function getPower() {
        return self.properties.power;
    };

    this.addPower = function addPower(powerPlus) {
        self.properties.power += powerPlus;
    }

    this.chain = function chain() {
        // Handle a chip chain event.
    };

    this.use = function use() {
        // Use the chip.
    };
};
