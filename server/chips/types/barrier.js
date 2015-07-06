'use strict';

var Chip = require(__dirname + '/..'),
    extend = require(__dirname + '/../extend');

function BarrierConstructor(io, config, game, character) {
    var self = this;

    this.use = function use() {
        character.setDamageHandler(function(damage, element, flinch) {
            self.properties.health -= damage;

            if (self.properties.health <= 0) {
                character.setDamageHandler(null);
            }
        })
    };
}

module.exports = function Barrier(io, config, game, character) {
    return extend(BarrierConstructor, Chip, io, config, game, character);
};