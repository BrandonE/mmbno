'use strict';

var Chip = require(__dirname + '/'),
    extend = require(__dirname + '/extend');

function InvisibleConstructor(io, config, game, character, code) {
    var self = this;

    this.properties.codes = ['*'];
    this.properties.description = 'Invisible for a while';
    this.properties.name = 'Invisible';
    this.properties.short = 'Invisibl';
    this.properties.stars = 3;

    this.use = function use() {
        character.setDamageHandler({
            name    : self.properties.name,
            handler : function(damage, element, flinch) {
                // Ignore damage while invisible.
                return 0;
            }
        }, 2);

        clearTimeout(character.invisibleTimeout);
        character.invisibleTimeout = setTimeout(function() {
            if (character.getDamageHandler(2).name === self.properties.name) {
                character.setDamageHandler(null, 2);
            }
        }, 10000);
    };
}

module.exports = function Invisible(io, config, game, character, code) {
    return extend(InvisibleConstructor, Chip, io, config, game, character, code);
};
