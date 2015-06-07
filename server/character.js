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
    this.statuses = [];
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

    this.hasStatus = function hasStatus(status) {
        return (self.statuses.indexOf(status) > -1);
    };

    this.addStatus = function addStatus(status) {
        self.statuses.push(status);
    };

    this.removeStatus = function removeStatus(status) {
        var index = self.statuses.indexOf(status);

        if (index > -1) {
            delete self.statuses[index];
        }
    };

    this.getBusterPower = function getBusterPower() {
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
        self.shoot(self.busterPower);
    };

    this.canStandOn = function canStandOn(panel) {
        return (
            ['blank', 'broken'].indexOf(panel.getType()) === -1 ||
                self.hasStatus('airshoes')
        );
    };

    this.move = function move(direction, rows, cols) {
        var playerNum = self.playerNum,
            playerElement = self.element,
            field = game.getField(),
            grid = field.getGrid(),
            currentRow,
            currentCol,
            currentPanel,
            newRow,
            newCol,
            newPanel,
            newPanelType;

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
                newPanel.isInBounds(self) &&
                    self.canStandOn(newPanel) &&
                    !newPanel.getCharacter() &&
                    !self.hasStatus('paralyzed') &&
                    !self.hasStatus('frozen')
            ) {
                currentPanel.setCharacter(null);
                newPanel.setCharacter(self);
                self.setRow(newRow);
                self.setCol(newCol);

                clearTimeout(self.roadPanelTimeout);

                if (!self.hasStatus('floatshoes')) {
                    newPanelType = newPanel.getType();

                    field.updateStolenPanels();

                    // If the panel is cracked and the character moved, break it.
                    if (
                        currentPanel.getType() === 'cracked' &&
                            (currentRow !== newRow || currentCol !== newCol)
                    ) {
                        currentPanel.setType('broken');
                    }

                    /*
                     If the character moved onto a lava panel and doesn't have the fire element, burn the character
                     and revert the panel.
                     */
                    if (newPanelType === 'lava' && playerElement !== 'fire') {
                        self.takeDamage(10);
                        newPanel.setType('normal');
                    }

                    // Slide if the panel is frozen and the character does not have the aqua element.
                    if (newPanelType === 'frozen' && playerElement !== 'aqua') {
                        self.move(direction, 1, 1);
                    }

                    newPanel.handleRoad();
                }

                io.to(game.getId()).emit('player moved', self.playerNum, self.row, self.col);
                field.draw();
            }
        }
    };

    this.shoot = function shoot(power, element) {
        var grid = game.getField().getGrid(),
            row,
            col,
            panel;

        if (element === undefined) {
            element = 'none';
        }

        if (self.hasStatus('paralyzed')) {
            row = self.row;

            if (self.playerNum === 1) {
                for (col = self.col + 1; col < config.cols; col++) {
                    panel = grid[row][col];

                    if (panel.shot(power, element)) {
                        break;
                    }
                }
            } else {
                for (col = self.col - 1; col >= 0; col--) {
                    panel = grid[row][col];

                    if (panel.shot(power, element)) {
                        break;
                    }
                }
            }
        }
    };

    this.takeDamage = function takeDamage(damage, element, flinch) {
        var field = game.getField(),
            panelType;

        if (element === undefined) {
            element = 'none';
        }

        // Double the damage if the attack is the character's weakness.
        if (weaknesses.hasOwnProperty(self.element) && weaknesses[self.element] === element) {
            damage *= 2;
        }

        // Double the damage and revert if the character is frozen and the attack is break.
        if (self.hasStatus('frozen') && element === 'break') {
            damage *= 2;
            self.removeStatus('frozen');
        }

        // Double the damage if the panel is grass and the attack has the fire element.
        panelType = field.getGrid()[self.row][self.col].getType();

        if (panelType === 'grass' && element === 'fire') {
            damage *= 2;
        }

        // Half the damage if on a holy panel.
        if (panelType === 'holy') {
            damage = parseInt(Math.ceil(damage / 2));
        }

        // If an active chip exists, override the original handling.
        // TODO

        self.health -= damage;

        if (self.health < 0) {
            self.health = 0;
        }

        io.to(game.getId()).emit('player health changed', self.playerNum, self.health);
        field.draw();
    };

    this.useChip = function useChip() {
        var chip = self.chips.shift(),
            nextChip,
            chained = true;

        if (chip) {
            // Handle a chip chain event.
            while (self.chips.length && chained) {
                nextChip = self.chips[0];
                chained = nextChip.chain(chip);

                // Remove the next chip if it should be used in a chain.
                if (chained) {
                    self.chips.shift();
                    nextChip.used();
                }
            }

            chip.use();
            chip.used();
        }
    };

    this.toSendable = function toSendable() {
        return {
            id          : self.id,
            playerNum   : self.playerNum,
            maxHealth   : self.maxHealth,
            health      : self.health,
            element     : self.element,
            statuses    : self.statuses,
            busterPower : self.busterPower,
            row         : self.row,
            col         : self.col
        };
    };

    this.chipsToSendable = function chipsToSendable() {
        var chipsToSend = [],
            chipToSend,
            c;

        for (c in self.chips) {
            if (self.chips.hasOwnProperty(c)) {
                chipToSend = self.chips[c].toSendable();

                chipsToSend.push(chipToSend);
            }
        }

        return chipsToSend;
    };

    if (playerNum === 1) {
        this.enterField(1, 1);
    } else if (playerNum === 2) {
        this.enterField(1, 4);
    }
};
