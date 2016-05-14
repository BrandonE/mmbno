/// <reference path="../../../typings/tsd.d.ts" />
'use strict';

namespace Game {
    export class State extends Phaser.State {
        socket: SocketIOClient.Socket;
        music: Phaser.Sound;

        create(): void {
            var self = this;

            if (!this.music) {
                this.music = this.sound.play('mmbn6boss', 0.5);
            }

            this.socket = io.connect();
        }
    }
}
