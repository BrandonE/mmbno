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

module.exports = function Character(config, field, id, playerNum) {
    var self = this;

    this.config = config;
    this.field = field;
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

        field.placeCharacter(self, row, col);
    };

    this.leaveField = function leave() {
        field.placeCharacter(null, self.row, self.col);
    };

    this.move = function move(direction, rows, cols) {
        var playerNum = self.playerNum,
            playerElement = self.element,
            playerStatus = self.status,
            grid = self.field.getGrid(),
            currentRow,
            currentCol,
            currentPanel,
            newRow,
            newCol,
            newPanel;

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
        if (currentPanel.character != self) {
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
                    !newPanel.character &&
                    playerStatus.indexOf('paralyzed') === -1 &&
                    playerStatus.indexOf('frozen') === -1
            ) {
                currentPanel.character = null;

                newPanel.character = self;
                self.setRow(newRow);
                self.setCol(newCol);

                if (playerStatus.indexOf('floatshoes') === -1) {
                    // If the panel is cracked and the character moved, break it.
                    if (
                        currentPanel.status === 'cracked' &&
                            (currentRow !== newRow || currentCol !== newCol)
                    ) {
                        currentPanel.status = 'broken';
                    }

                    /*
                     If the character moved onto a lava panel and doesn't have the fire element, burn the character
                     and revert the panel.
                     */
                    if (newPanel.status === 'lava' && playerElement !== 'fire') {
                        self.takeDamage(10);
                        newPanel.status = 'normal';
                    }

                    // Slide if the panel is frozen and the character does not have the aqua element.
                    if (newPanel.status === 'frozen' && playerElement !== 'aqua') {
                        self.move(direction, 1, 1);
                    }

                    // Handle road panels.
                    if (['up', 'down', 'left', 'right'].indexOf(newPanel.status) > -1) {
                        self.move(newPanel.status, 1, 1);
                    }
                }

                field.draw();
            }
        }
    };

    this.shoot = function shoot(power, element) {
        var grid = self.field.getGrid(),
            row,
            col,
            panel;

        if (element === undefined) {
            element = 'none';
        }

        if (self.status.indexOf('paralyzed')) {
            row = self.row;

            if (self.playerNum === 1) {
                for (col = self.col + 1; col < self.config.cols; col++) {
                    panel = grid[row][col];

                    if (self.shootPanel(power, element, panel)) {
                        break;
                    }
                }
            } else {
                for (col = self.col - 1; col >= 0; col--) {
                    panel = grid[row][col];

                    if (self.shootPanel(power, element, panel)) {
                        break;
                    }
                }
            }
        }
    };

    this.shootPanel = function shootPanel(power, element, panel) {
        if (panel.character) {
            panel.character.takeDamage(power, element);

            if (panel.status === 'grass' && element === 'fire') {
                panel.status = 'normal';
            }

            return true;
        } else {
            return false;
        }
    };

    this.takeDamage = function takeDamage(damage, element, flinch) {
        var frozenIndex,
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
        panelStatus = self.field.getGrid()[self.row][self.col].status;

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
        field.draw();
    };

    this.toSendable = function toSendable() {
        return {
            id          : self.id,
            playerNum   : self.playerNum,
            maxHealth   : self.maxHealth,
            health      : self.maxHealth,
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
