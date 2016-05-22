/// <reference path="../../../typings/tsd.d.ts" />
'use strict';

namespace Generic {
    export class Panel extends Phaser.Sprite {
        row: number;
        col: number;
        panelType: string;
        stolen: boolean;
        character: Generic.Character;
        layer: string;

        constructor(state: Phaser.State, row: number, col: number, type: string, stolen: boolean) {
            super(state.game, null, (row * 25) + 65, 'panels');

            var colPerspective = col;

            if (this.game.state.states.Game.clientPlayerNum !== 1) {
                colPerspective = this.game.state.states.Game.config.cols - col - 1;
            }

            this.x = colPerspective * 40;

            this.row = row;
            this.col = col;
            this.panelType = type;
            this.stolen = stolen;

            if (row === 0) {
                this.layer = 'top';
            } else if (row === this.game.state.states.Game.config.rows - 1) {
                this.layer = 'bottom';
            } else {
                this.layer = 'middle';
            }

            this.updateFrame();
        }

        flipStolen(): void {
            this.stolen = !this.stolen;

            this.updateFrame();
        }

        setType(type): void {
            this.panelType = type;

            this.updateFrame();
        }

        updateFrame(): void {
            var color;

            if (
                isPanelInBounds(
                    this.game.state.states.Game.config,
                    this.col,
                    this.stolen,
                    this.game.state.states.Game.clientPlayerNum
                )
            ) {
                color = 'red';
            } else {
                color = 'blue';
            }

            this.frameName = color + '/' + this.panelType + '/' + this.layer + '.png';
        }
    }
}