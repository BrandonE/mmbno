/// <reference path="../../../typings/tsd.d.ts" />
'use strict';

namespace Loader {
    export class State extends Phaser.State {
        preload(): void {
            this.load.json('config', 'assets/config.json');

            this.load.atlasJSONHash('mega', 'assets/images/spritesheets/mega.png', 'assets/images/spritesheets/mega.json');
            this.load.atlasJSONHash('panels', 'assets/images/spritesheets/panels.png', 'assets/images/spritesheets/panels.json');

            this.load.audio('mmbn6boss', 'assets/music/mmbn6boss.ogg');
        }

        create(): void {
            console.log('Loading complete');
            this.game.state.start('Game');
        }
    }
}
