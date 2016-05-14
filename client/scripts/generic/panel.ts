/// <reference path="../../../typings/tsd.d.ts" />
'use strict';

namespace Generic {
    export class Panel extends Phaser.Sprite {
        row: number;
        col: number;
        panelType: string;
        stolen: boolean;

        constructor(state: Phaser.State, row: number, col: number, type: string, stolen: boolean) {
            super(state.game, col * 40, row * 25, 'panels', 'red/normal/top.png');

            this.row = row;
            this.col = col;
            this.panelType = type;
            this.stolen = stolen;
        }
    }
}