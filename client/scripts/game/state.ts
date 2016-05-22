/// <reference path="../../../typings/tsd.d.ts" />
'use strict';

namespace Game {
    export class State extends Phaser.State {
        socket: SocketIOClient.Socket;
        keyboard: Generic.Keyboard;
        music: Phaser.Sound;
        field: Generic.Panel[][] = [];
        players: Generic.Character[] = [];
        observers: number = 0;
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
                'user connected', function(
                    playerNum: number,
                    game: {
                        field: {type: string, stolen: boolean}[][],
                        players: {
                            playerNum: number, row: number, col: number, maxHealth: number, health: number,
                            busterPower: number, element: string, damageHandlers: string[], statuses: string[]
                        }[]
                    }
                ) {
                    var row: number,
                        col: number,
                        panels: Generic.Panel[],
                        panel: Generic.Panel,
                        playerData: {
                            playerNum: number, row: number, col: number, maxHealth: number, health: number,
                            busterPower: number, element: string, damageHandlers: string[], statuses: string[]
                        },
                        p: number;

                    if (self.clientPlayerNum) {
                        if (playerNum) {
                            playerData = game.players[playerNum - 1];

                            self.addPlayer(playerData, playerNum);
                        } else {
                            self.observers++;
                        }
                    } else {
                        self.clientPlayerNum = playerNum;
                        
                        if (game.field.length === self.config.rows) {
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

                        for (p = 0; p < game.players.length; p++) {
                            playerData = game.players[p];

                            if (playerData) {
                                self.addPlayer(playerData, p + 1);
                            }
                        }
                    }
                }
            );

            this.socket.on('user disconnected', function(playerNum: number) {
                var player: Generic.Character,
                    playerIndex: number = playerNum - 1;

                if (playerNum) {
                    player = self.players[playerIndex];

                    if (player) {
                        self.players[playerIndex] = null;
                        self.field[player.row][player.col].character = null;
                        player.kill();
                    }
                } else {
                    self.observers--;
                }
            });

            this.socket.on('active connections', function(activeConnections) {
                // TODO
            });

            this.socket.on('chips', function(chipsSent) {
                // TODO
            });

            this.socket.on('chip used', function(playerNum, chip) {
                // TODO
            });

            this.socket.on('panel type changed', function(panelRow, panelCol, type) {
                self.field[panelRow][panelCol].setType(type);
            });

            this.socket.on('panel flip stolen', function(panelRow, panelCol) {
                self.field[panelRow][panelCol].flipStolen();
            });

            this.socket.on('player damage handler changed', function(playerNum, damageHandler, priority) {
                // TODO
            });

            this.socket.on('player health changed', function(playerNum, health) {
                // TODO
            });

            this.socket.on('player moved', function(playerNum: number, row: number, col: number) {
                var player: Generic.Character;

                if (playerNum) {
                    player = self.players[playerNum - 1];

                    if (player) {
                        self.field[player.row][player.col].character = null;

                        player.row = row;
                        player.col = col;

                        player.updatePosition();

                        self.field[row][col].character = player;
                    }
                }
            });

            this.socket.on('player status added', function(playerNum, status) {
                // TODO
            });

            this.socket.on('player status removed', function(playerNum, status) {
                // TODO
            });
        }

        addPlayer(
            playerData: {
                playerNum: number, row: number, col: number, maxHealth: number, health: number,
                busterPower: number, element: string, damageHandlers: string[], statuses: string[]
            },
            playerNum
        ): void {
            var player: Generic.Character = new Generic.Character(
                this,
                playerNum,
                playerData.row,
                playerData.col,
                playerData.maxHealth,
                playerData.health,
                playerData.busterPower,
                playerData.element,
                playerData.damageHandlers,
                playerData.statuses
            );

            this.game.add.existing(player);

            this.players[playerNum - 1] = player;
            this.field[player.row][player.col].character = player;
        }
    }
}
