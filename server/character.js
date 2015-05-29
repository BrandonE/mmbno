'use strict';

module.exports = function Character(id, playerNum) {
    var self = this;

    this.id = id;
    this.playerNum = playerNum;
    this.maxHealth = 500;
    this.health = this.maxHealth;
    this.status = [];
    this.busterPower = 1;

    this.getId = function getId() {
        return self.id;
    }

    this.getPlayerNum = function getPlayerNum() {
        return self.playerNum;
    }

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
