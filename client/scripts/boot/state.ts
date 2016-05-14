/// <reference path="../../../typings/tsd.d.ts" />
'use strict';

namespace Boot {
    export class State extends Phaser.State {
        init(): void {
            this.game.scale.scaleMode = Phaser.ScaleManager.SHOW_ALL;
            this.game.scale.pageAlignHorizontally = true;
            this.game.scale.pageAlignVertically = true;
            this.game.scale.refresh();
            this.game.stage.disableVisibilityChange = true;
        }

        create(): void {
            console.log('Boot complete');
            this.game.state.start('Loader');
        }
    }
}
