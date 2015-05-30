var EOL = require('os').EOL,
    common = require(__dirname + '/common');

module.exports = function Field(config, players) {
    var self = this;

    this.config = config;
    this.players = players;
    this.grid = [];

    this.getGrid = function getGrid() {
        return self.grid;
    };

    this.checkCanStand = function checkCanStand(playerStatus, newPanel) {
        return (
            ['blank', 'broken'].indexOf(newPanel.status) === -1 ||
                playerStatus.indexOf('airshoes') > -1
        );
    };

    this.checkPanelInBounds = function checkPanelInBounds(playerNum, newRow, newCol) {
        return common.checkPanelInBounds(self.config, self.grid, playerNum, newRow, newCol);
    };

    this.draw = function draw() {
        console.log('\033[2J');
        console.log(common.gridToString(self.config, self.grid, this.players));
    };

    this.placeCharacter = function place(character, row, col) {
        self.grid[row][col].character = character;
    };

    this.grid = common.createGrid(config);
};
