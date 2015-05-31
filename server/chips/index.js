'use strict';

module.exports = function Chip(io, config, character) {
    this.properties = {
        codes          : [],
        description    : '',
        name           : '',
        short          : '',
        power          : 0,
        element        : 'none',
        classification : 'standard',
        priority       : 0,
        stars          : 1
    };

    this.use = function use() {
    };
};
