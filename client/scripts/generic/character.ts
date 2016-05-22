/// <reference path="../../../typings/tsd.d.ts" />
'use strict';

namespace Generic {
    export class Character extends Phaser.Sprite {
        playerNum: number;
        row: number;
        col: number;
        maxHealth: number;
        health: number;
        busterPower: number;
        element: string;
        damageHandlers: string[];
        statuses: string[];

        constructor(
            state: Phaser.State, playerNum: number, row: number, col: number, maxHealth: number, health: number,
            busterPower: number, element: string, damageHandlers: string[], statuses: string[]
        ) {
            super(state.game, null, null, 'mega', 'normal/0.png');

            this.row = row;
            this.col = col;
            this.maxHealth = maxHealth;
            this.health = health;
            this.busterPower = busterPower;
            this.element = element;
            this.damageHandlers = damageHandlers;
            this.statuses = statuses;

            this.updatePosition();
        }

        updatePosition(): void {
            var colPerspective = this.col;

            if (this.game.state.states.Game.clientPlayerNum !== 1) {
                colPerspective = this.game.state.states.Game.config.cols - this.col - 1;
            }

            this.x = (colPerspective * 40) - 24;
            this.y = ((this.row - 1) * 25) + 65 - 23;
        }
    }
}