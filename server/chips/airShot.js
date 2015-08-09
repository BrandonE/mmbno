'use strict';

var Chip = require(__dirname + '/'),
    extend = require(__dirname + '/extend');

function AirShotConstructor(io, config, game, character, code) {
    var self = this;

    this.properties.codes = ['*'];
    this.properties.description = 'Knock enemy back 1 square';
    this.properties.element = 'wind';
    this.properties.name = 'Air Shot';
    this.properties.short = 'AirShot';
    this.properties.power = 20;
    this.properties.stars = 2;

    this.use = function use() {
        character.shoot(self.properties.power, self.properties.element, true, null, function onHit(panel) {
            var panelCharacter = panel.getCharacter();

            // Knocking "back" relative to the character's perspective means moving left.
            panelCharacter.removeStatus('flinching');
            panelCharacter.move('left', 1);
            panelCharacter.addStatus('flinching');
        });
    };
}

module.exports = function AirShot(io, config, game, character, code) {
    return extend(AirShotConstructor, Chip, io, config, game, character, code);
};
