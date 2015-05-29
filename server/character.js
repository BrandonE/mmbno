'use strict';

module.exports = function Character() {
    var self = this;

    this.maxHealth = 500;
    this.health = this.maxHealth;
    this.status = [];
    this.busterPower = 1;

    this.getRow = function getRow() {
        return self.row;
    }

    this.setRow = function setRow(value) {
        self.row = value;
    }

    this.getCol = function getCol() {
        return self.col;
    }

    this.setCol = function setCol(value) {
        self.col = value;
    }

    this.getHealth = function getHealth() {
        return self.health;
    }
}
