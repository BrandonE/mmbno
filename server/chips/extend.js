'use strict';

module.exports = function extend(Child, Parent, io, game, config, character) {
    Child.prototype = new Parent(io, config, game, character);
    Child.constructor = Child;
    return new Child(io, config, game, character);
};
