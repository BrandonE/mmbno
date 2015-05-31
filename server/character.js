'use strict';

var weaknesses = {
    aqua     : 'electric',
    break    : 'cursor',
    cursor   : 'wind',
    electric : 'wood',
    fire     : 'aqua',
    sword    : 'break',
    wind     : 'sword',
    wood     : 'fire'
};

module.exports = function Character(io, config, game, id, playerNum) {
    var self = this;

    this.id = id;
    this.playerNum = playerNum;
    this.maxHealth = 500;
    this.health = this.maxHealth;
    this.element = 'none';
    this.status = [];
    this.busterPower = 1;

    this.getId = function getId() {
        return self.id;
    };

    this.getPlayerNum = function getPlayerNum() {
        return self.playerNum;
    };

    this.getRow = function getRow() {
        return self.row;
    };

    this.setRow = function setRow(value) {
        self.row = value;
    };

    this.getCol = function getCol() {
        return self.col;
    };

    this.setCol = function setCol(value) {
        self.col = value;
    };

    this.getHealth = function getHealth() {
        return self.health;
    };

    this.getElement = function getElement() {
        return self.element;
    };

    this.getStatus = function getStatus() {
        return self.status;
    };

    this.getBusterPower = function getStatus() {
        return self.busterPower;
    };

    this.enterField = function enterField(row, col) {
        self.setRow(row);
        self.setCol(col);

        game.getField().placeCharacter(self, row, col);
    };

    this.leaveField = function leave() {
        game.getField().placeCharacter(null, self.row, self.col);
    };

    this.busterShot = function busterShot() {
        return self.shoot(self.busterPower);
    }

    this.move = function move(direction, rows, cols) {
        var playerNum = self.playerNum,
            playerElement = self.element,
            playerStatus = self.status,
            field = game.getField(),
            grid = field.getGrid(),
            currentRow,
            currentCol,
            currentPanel,
            newRow,
            newCol,
            newPanel,
            newPanelStatus;

        if (rows === undefined) {
            rows = 1;
        }

        if (cols === undefined) {
            cols = 1;
        }

        if (playerNum === 2) {
            cols = -cols;
        }

        currentRow = self.row;
        currentCol = self.col;
        currentPanel = grid[currentRow][currentCol];
        newRow = currentRow;
        newCol = currentCol;

        // If the panel doesn't contain the character, something went horribly wrong.
        if (currentPanel.getCharacter() != self) {
            throw new Error('Field desync.');
        }

        switch (direction) {
            case 'up':
                newRow -= rows;
                break;

            case 'down':
                newRow += rows;
                break;

            case 'left':
                newCol -= cols;
                break;

            case 'right':
                newCol += cols;
                break;
        }

        // Destination must be a real panel.
        if (
            newRow >= 0 && newRow < config.rows &&
                newCol >= 0 && newCol < config.cols
        ) {
            newPanel = grid[newRow][newCol];

            if (
                field.checkPanelInBounds(playerNum, newRow, newCol) &&
                    field.checkCanStand(playerStatus, newPanel) &&
                    !newPanel.getCharacter() &&
                    playerStatus.indexOf('paralyzed') === -1 &&
                    playerStatus.indexOf('frozen') === -1
            ) {
                currentPanel.setCharacter(null);
                newPanel.setCharacter(self);
                self.setRow(newRow);
                self.setCol(newCol);

                if (playerStatus.indexOf('floatshoes') === -1) {
                    newPanelStatus = newPanel.getStatus();

                    // If the panel is cracked and the character moved, break it.
                    if (
                        currentPanel.getStatus() === 'cracked' &&
                            (currentRow !== newRow || currentCol !== newCol)
                    ) {
                        currentPanel.setStatus('broken');
                    }

                    /*
                     If the character moved onto a lava panel and doesn't have the fire element, burn the character
                     and revert the panel.
                     */
                    if (newPanelStatus === 'lava' && playerElement !== 'fire') {
                        self.takeDamage(10);
                        newPanel.setStatus('normal');
                    }

                    // Slide if the panel is frozen and the character does not have the aqua element.
                    if (newPanelStatus === 'frozen' && playerElement !== 'aqua') {
                        self.move(direction, 1, 1);
                    }

                    // Handle road panels.
                    if (['up', 'down', 'left', 'right'].indexOf(newPanelStatus) > -1) {
                        setTimeout(
                            function() {
                                if (newPanel.getCharacter() === self) {
                                    self.move(newPanelStatus, 1, 1);
                                }
                            },
                            500
                        );
                    }
                }

                io.to(game.getId()).emit('moved', self.playerNum, self.row, self.col);
                field.draw();
            }
        }
    };

    this.shoot = function shoot(power, element) {
        var grid = game.getField().getGrid(),
            row,
            col,
            panel,
            playerNumHit;

        if (element === undefined) {
            element = 'none';
        }

        if (self.status.indexOf('paralyzed')) {
            row = self.row;

            if (self.playerNum === 1) {
                for (col = self.col + 1; col < config.cols; col++) {
                    panel = grid[row][col];
                    playerNumHit = self.shootPanel(power, element, panel);

                    if (playerNumHit) {
                        return playerNumHit;
                    }
                }
            } else {
                for (col = self.col - 1; col >= 0; col--) {
                    panel = grid[row][col];
                    playerNumHit = self.shootPanel(power, element, panel);

                    if (playerNumHit) {
                        return playerNumHit;
                    }
                }
            }
        }
    };

    this.shootPanel = function shootPanel(power, element, panel) {
        if (panel.character) {
            panel.character.takeDamage(power, element);

            if (panel.getStatus() === 'grass' && element === 'fire') {
                panel.setStatus('normal');
            }

            return panel.character.getPlayerNum();
        } else {
            return false;
        }
    };

    this.takeDamage = function takeDamage(damage, element, flinch) {
        var field = game.getField(),
            frozenIndex,
            panelStatus;

        if (element === undefined) {
            element = 'none';
        }

        // Double the damage if the attack is the character's weakness.
        if (weaknesses.hasOwnProperty(self.element) && weaknesses[self.element] === element) {
            damage *= 2;
        }

        frozenIndex = self.status.indexOf('frozen');

        // Double the damage and revert if the character is frozen and the attack is break.
        if (frozenIndex > -1 && element === 'break') {
            damage *= 2;
            delete self.status[frozenIndex];
        }

        // Double the damage if the panel is grass and the attack has the fire element.
        panelStatus = field.getGrid()[self.row][self.col].getStatus();

        if (panelStatus === 'grass' && element === 'fire') {
            damage *= 2;
        }

        // Half the damage if on a holy panel.
        if (panelStatus === 'holy') {
            damage = parseInt(Math.ceil(damage / 2));
        }

        // If an active chip exists, override the original handling.
        // TODO

        self.health -= damage;

        if (self.health < 0) {
            self.health = 0;
        }

        io.to(game.getId()).emit('health changed', self.playerNum, self.health);
        field.draw();
    };

    this.useChip = function useChip() {
        var chip = self.chips.shift(),
            nextChip,
            chained = true;

        // Handle a chip chain event.
        while (self.chips.length && chained) {
            nextChip = self.chips[0];
            chained = nextChip.chain(chip);

            // Remove the next chip if it should be used in a chain.
            if (chained) {
                self.chips.shift();
            }
        }

        chip.use();
    }

    this.toSendable = function toSendable() {
        return {
            id          : self.id,
            playerNum   : self.playerNum,
            maxHealth   : self.maxHealth,
            health      : self.health,
            element     : self.element,
            status      : self.status,
            busterPower : self.busterPower,
            row         : self.row,
            col         : self.col
        };
    };

    if (playerNum === 1) {
        this.enterField(1, 1);
    } else if (playerNum === 2) {
        this.enterField(1, 4);
    }
};
