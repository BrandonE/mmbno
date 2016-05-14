/// <reference path="../../../typings/tsd.d.ts" />
'use strict';

namespace Generic {
    export class Keyboard {
        up: Phaser.Key;
        down: Phaser.Key;
        left: Phaser.Key;
        right: Phaser.Key;
        a: Phaser.Key;
        s: Phaser.Key;

        constructor(game: Phaser.Game) {
            this.up = game.input.keyboard.addKey(Phaser.Keyboard.UP);
            this.down = game.input.keyboard.addKey(Phaser.Keyboard.DOWN);
            this.left = game.input.keyboard.addKey(Phaser.Keyboard.LEFT);
            this.right = game.input.keyboard.addKey(Phaser.Keyboard.RIGHT);
            this.a = game.input.keyboard.addKey(Phaser.Keyboard.A);
            this.s = game.input.keyboard.addKey(Phaser.Keyboard.S);
        }
    }
}
