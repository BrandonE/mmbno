'use strict';

var fs = require('fs'),
    chipClasses = {},
    defaultChips = JSON.parse(fs.readFileSync(__dirname + '/chips/folders/default.json')),
    weaknesses = {
    aqua     : 'electric',
    break    : 'cursor',
    cursor   : 'wind',
    electric : 'wood',
    fire     : 'aqua',
    sword    : 'break',
    wind     : 'sword',
    wood     : 'fire'
};

fs.readdirSync(__dirname + '/chips')
    .filter(function(file) {
        return (file.indexOf('.') !== 0 && ['index.js', 'folders', 'types'].indexOf(file) <= -1);
    })
    .forEach(function(file) {
        var ChipClass = require(__dirname + '/chips/' + file),
            chipName = file.replace('.js', '');

        chipClasses[chipName] = ChipClass;
    });

module.exports = function Character(io, config, game, socket, playerNum) {
    var self = this;

    this.id = socket.id;
    this.playerNum = playerNum;
    this.maxHealth = 500;
    this.health = this.maxHealth;
    this.damageHandlers = [];
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

    this.getDamageHandler = function getDamageHandler(priority) {
        return self.damageHandlers[priority];
    };

    this.getDamageHandlerWithTopPriority = function getDamageHandlerWithTopPriority() {
        var damageHandler,
            d;

        for (d in self.damageHandlers) {
            damageHandler = self.damageHandlers[d];

            if (damageHandler) {
                return damageHandler;
            }
        }

        return null;
    };

    this.setDamageHandler = function setDamageHandler(damageHandler, priority) {
        self.damageHandlers[priority] = damageHandler;

        io.to(game.getId()).emit(
            'player damage handler changed', self.playerNum,
            (damageHandler) ? damageHandler.name : null,
            priority
        );

        game.getField().draw();
    };

    this.hasStatus = function hasStatus(status) {
        return (self.statuses.indexOf(status) > -1);
    };

    this.addStatus = function addStatus(status) {
        var index = self.statuses.indexOf(status);

        if (index === -1) {
            self.statuses.push(status);
        }

        io.to(game.getId()).emit('player status added', self.playerNum, status);
        game.getField().draw();
    };

    this.removeStatus = function removeStatus(status) {
        var index = self.statuses.indexOf(status);

        if (index > -1) {
            self.statuses.splice(index, 1);
        }

        io.to(game.getId()).emit('player status removed', self.playerNum, status);
        game.getField().draw();
    };

    this.boostBusterPower = function boostBusterPower(plus) {
        self.busterPower += plus;
    };

    this.createChipFolder = function createChipFolder() {
        var chips = [],
            chipRecord,
            ChipClass,
            chip,
            c;

        for (c in defaultChips) {
            chipRecord = defaultChips[c];
            ChipClass = chipClasses[chipRecord.name];
            chip = new ChipClass(io, config, game, self, chipRecord.code);
            chip.validate();
            chips.push(chip);
        }

        return chips;
    };

    this.getRandomChips = function getRandomChips(num) {
        var chips = [],
            chipNum,
            chip,
            c;

        for (chipNum = 0; chipNum < num; chipNum++) {
            if (this.chipFolder.length) {
                c = Math.floor(Math.random() * this.chipFolder.length);
                chip = this.chipFolder[c];

                // Remove the chip from the folder.
                this.chipFolder.splice(c, 1);

                chips.push(chip);
            }
        }

        return chips;
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
        self.shoot(self.busterPower, self.element);
    };

    this.canStandOn = function canStandOn(panel) {
        return (
            ['blank', 'broken'].indexOf(panel.getType()) === -1 ||
                self.hasStatus('airshoes')
        );
    };

    this.heal = function heal(health) {
        self.health += health;

        if (self.health > self.maxHealth) {
            self.health = self.maxHealth;
        }

        io.to(game.getId()).emit('player health changed', self.playerNum, self.health);
        game.getField().draw();
    };

    this.move = function move(direction, distance) {
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

        if (distance === undefined) {
            distance = 1;
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
                newRow -= distance;
                break;

            case 'down':
                newRow += distance;
                break;

            case 'left':
                if (playerNum === 1) {
                    newCol -= distance;
                } else {
                    newCol += distance;
                }

                break;

            case 'right':
                if (playerNum === 1) {
                    newCol += distance;
                } else {
                    newCol -= distance;
                }

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
                    !self.hasStatus('attacking') &&
                    !self.hasStatus('flinching') &&
                    !self.hasStatus('frozen') &&
                    !self.hasStatus('paralyzed')
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
                        currentPanel.break();
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
                        self.move(direction, 1);
                    }

                    newPanel.handleRoad();
                }

                io.to(game.getId()).emit('player moved', self.playerNum, self.row, self.col);
                field.draw();
            }
        }
    };

    this.selectChips = function selectChips() {
        self.chips = self.getRandomChips(5);
        socket.emit('chips', self.chipsToSendable());
    };

    this.shoot = function shoot(power, element, flinch, recoveryTime, onHit, onMiss) {
        var hit = false,
            grid = game.getField().getGrid(),
            row,
            col,
            panel;

        if (recoveryTime === undefined) {
            recoveryTime = 250;
        }

        if (element === undefined) {
            element = 'none';
        }

        if (
            !self.hasStatus('attacking') && !self.hasStatus('flinching') && !self.hasStatus('frozen') &&
                !self.hasStatus('paralyzed')
        ) {
            row = self.row;

            if (self.playerNum === 1) {
                for (col = self.col + 1; col < config.cols; col++) {
                    panel = grid[row][col];

                    if (panel.hit(power, element, flinch, onHit)) {
                        hit = true;
                        break;
                    }
                }
            } else {
                for (col = self.col - 1; col >= 0; col--) {
                    panel = grid[row][col];

                    if (panel.hit(power, element, flinch, onHit)) {
                        hit = true;
                        break;
                    }
                }
            }

            if (!hit && onMiss) {
                onMiss();
            }

            if (recoveryTime) {
                self.addStatus('attacking');

                setTimeout(function() {
                    self.removeStatus('attacking');
                }, recoveryTime);
            }
        }
    };

    this.takeDamage = function takeDamage(damage, element, flinch) {
        var field = game.getField(),
            damageHandler = self.getDamageHandlerWithTopPriority(),
            panelType;

        if (element === undefined) {
            element = 'none';
        }

        if (!self.hasStatus('invincible')) {
            if (damageHandler) {
                damageHandler.handler(damage, element, flinch);
            } else {
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

                if (
                    ((panelType === 'frozen' || panelType === 'metal') && element === 'electric') ||
                        (panelType === 'grass' && (element === 'fire' || element === 'wind')) ||
                        (panelType === 'sand' && element === 'wind')
                ) {
                    damage *= 2;
                }

                // Halve the damage if on a holy panel.
                if (panelType === 'holy') {
                    damage = parseInt(Math.floor(damage / 2));
                }

                self.health -= damage;

                if (self.health < 0) {
                    self.health = 0;
                }

                if (flinch) {
                    self.addStatus('flinching');
                    self.addStatus('invincible');

                    setTimeout(function() {
                        self.removeStatus('flinching');
                    }, 250);

                    setTimeout(function() {
                        self.removeStatus('invincible');
                    }, 1000);
                }
            }

            io.to(game.getId()).emit('player health changed', self.playerNum, self.health);
            field.draw();
        }
    };

    this.useChip = function useChip() {
        var chip,
            nextChip,
            chained = true;

        if (
            self.chips[0] &&
                !self.hasStatus('attacking') && !self.hasStatus('flinching') && !self.hasStatus('frozen') &&
                !self.hasStatus('paralyzed')
        ) {
            chip = self.chips.shift();

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
        var damageHandlersToSendable = [],
            damageHandler,
            d;

        for (d in self.damageHandlers) {
            damageHandler = self.damageHandlers[d];

            if (damageHandler) {
                damageHandlersToSendable.push(damageHandler.name);
            } else {
                damageHandlersToSendable.push(undefined);
            }
        }

        return {
            id             : self.id,
            playerNum      : self.playerNum,
            maxHealth      : self.maxHealth,
            health         : self.health,
            damageHandlers : damageHandlersToSendable,
            element        : self.element,
            statuses       : self.statuses,
            busterPower    : self.busterPower,
            row            : self.row,
            col            : self.col
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

    this.chipFolder = this.createChipFolder();
    this.selectChips();
    setInterval(this.selectChips, config.chipSelectionInterval);
};
