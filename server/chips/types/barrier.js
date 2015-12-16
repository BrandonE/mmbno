'use strict';

var Chip = require(__dirname + '/..'),
    extend = require(__dirname + '/../extend');

function BarrierConstructor(io, config, game, character, code) {
    var self = this;

    this.use = function use() {
        character.setDamageHandler({
            name    : self.properties.name,
            handler : function(damage, element, flinch) {
                self.properties.health -= damage;

                if (self.properties.health <= 0) {
                    character.setDamageHandler(null, 3);
                }

                return 0;
            }
        }, 3);
    };
}

module.exports = function Barrier(io, config, game, character, code) {
    return extend(BarrierConstructor, Chip, io, config, game, character, code);
};
