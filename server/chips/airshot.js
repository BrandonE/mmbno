'use strict';

var Chip = require(__dirname + '/'),
    extend = require(__dirname + '/extend');

function CannonConstructor(io, config, game, character) {
    var self = this;

    this.properties.codes = ['*'];
    this.properties.description = 'Knock enemy back 1 square';
    this.properties.element = 'wind';
    this.properties.name = 'Air Shot';
    this.properties.short = 'AirShot';
    this.properties.power = 20;
    this.properties.stars = 2;

    this.use = function use() {
        character.shoot(self.properties.power, self.properties.element, function(panel) {
            // Knocking "back" relative to the character's perspective means moving left.
            panel.getCharacter().move('left', 0, 1);
        });
    };
}

module.exports = function Cannon(io, config, game, character) {
    return extend(CannonConstructor, Chip, io, config, game, character);
};
