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
        currentAnimation;

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

            this.updatePosition(false);
        }

        updatePosition(warping: boolean): void {
            var self = this,
                colPerspective = this.col;

            if (this.game.state.states.Game.clientPlayerNum !== 1) {
                colPerspective = this.game.state.states.Game.config.cols - this.col - 1;
            }

            this.x = (colPerspective * 40) - 24;
            this.y = ((this.row - 1) * 25) + 65 - 23;

            if (warping) {
                this.visible = false;

                setTimeout(function () {
                    self.visible = true;
                    self.animate(['move/2.png', 'move/1.png', 'move/0.png', 'normal/0.png'], 16);
                }, 16);
            }
        }

        animate(frames: string[], speed: number, frameIndex: number = 0): void {
            var self = this;

            this.frameName = frames[frameIndex];
            frameIndex++;

            if (frameIndex < frames.length) {
                if (this.currentAnimation) {
                    clearTimeout(this.currentAnimation);
                }
                
                this.currentAnimation = setTimeout(function() {
                    self.animate(frames, speed, frameIndex);
                }, speed);
            }
        }
    }
}