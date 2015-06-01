'use strict';

module.exports = function Chip(io, config, game, character) {
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
        self.used();
    };

    this.used = function used() {
        io.to(game.getId()).emit('chip used', character.getPlayerNum(), self.toSendable());
    };

    this.toSendable = function toSendable() {
        return self.properties;
    };
};
