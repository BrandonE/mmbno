/// <reference path="../../../typings/tsd.d.ts" />
'use strict';

namespace Game {
    export class State extends Phaser.State {
        socket: SocketIOClient.Socket;
        keyboard: Generic.Keyboard;
        music: Phaser.Sound;
        field: Generic.Panel[][];
        players;
        observers;
        chips: [{}];
        config: {port: number, rows: number, cols: number, chipSelectionInterval: number};
        chipSelectionTime: number = 0;
        clientPlayerNum: number;

        create(): void {
            var self = this;

            if (!this.music) {
                this.music = this.sound.play('mmbn6boss', 0.5);
            }

            this.config = this.cache.getJSON('config');

            this.socket = io.connect();

            this.keyboard = new Generic.Keyboard(this.game);

            this.keyboard.left.onDown.add(function() {
                self.socket.emit('move', 'left');
            });

            this.keyboard.right.onDown.add(function() {
                self.socket.emit('move', 'right');
            });

            this.keyboard.up.onDown.add(function() {
                self.socket.emit('move', 'up');
            });

            this.keyboard.down.onDown.add(function() {
                self.socket.emit('move', 'down');
            });

            this.keyboard.a.onDown.add(function() {
                self.socket.emit('use chip');
            });

            this.keyboard.s.onDown.add(function() {
                self.socket.emit('buster');
            });

            this.socket.on(
                'user connected', function(playerNum: number, game: {field: {type: string, stolen: boolean}[][]}) {
                    var row: number,
                        col: number,
                        panels: Generic.Panel[],
                        panel: Generic.Panel,
                        player: number,
                        playerIndex: number,
                        p: number;

                    if (self.field) {
                    } else {
                        if (game.field.length === self.config.rows) {
                            self.field = [];

                            for (row = 0; row < game.field.length; row++) {
                                if (game.field[row].length === self.config.cols) {
                                    panels = [];

                                    for (col = 0; col < game.field[row].length; col++) {
                                        panel = new Generic.Panel(
                                            self,
                                            row,
                                            col,
                                            game.field[row][col].type,
                                            game.field[row][col].stolen
                                        );

                                        panels.push(panel);
                                        self.game.add.existing(panel);
                                    }

                                    self.field.push(panels);
                                } else {
                                    throw new Error('Mismatch of number of columns between sent field and config.');
                                }
                            }
                        } else {
                            throw new Error('Mismatch of number of rows between sent field and config.');
                        }
                    }
                }
            );
        }
    }
}
