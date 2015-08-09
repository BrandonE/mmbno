'use strict';

module.exports = function extend(Child, Parent, io, config, game, character, code) {
    Child.prototype = new Parent(io, config, game, character, code);
    Child.constructor = Child;
    return new Child(io, config, game, character, code);
};
