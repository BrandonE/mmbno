'use strict';

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

    this.enterField = function enterField(row, col) {
        self.setRow(row);
        self.setCol(col);

        field.placeCharacter(self, row, col);
    };

    this.leaveField = function leave() {
        field.placeCharacter(null, self.getRow(), self.getCol());
    };

    this.move = function move(direction, rows, cols) {
        var playerNum = self.getPlayerNum(),
            playerElement = self.getElement(),
            playerStatus = self.getStatus(),
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

        currentRow = self.getRow();
        currentCol = self.getCol();
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

    this.takeDamage = function takeDamage(damage) {
        self.health -= damage;
    };

    if (playerNum === 1) {
        this.enterField(1, 1);
    } else if (playerNum === 2) {
        this.enterField(1, 4);
    }
};
