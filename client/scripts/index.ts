/// <reference path="../../typings/tsd.d.ts" />
'use strict';

class MonkeyWizard extends Phaser.Game {
    constructor() {
        super(240, 160, Phaser.AUTO, '');

        this.state.add('Boot', Boot.State);
        this.state.add('Game', Game.State);
        this.state.add('Loader', Loader.State);

        this.state.start('Boot');
    }
}

new MonkeyWizard();
