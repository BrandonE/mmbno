'use strict';

module.exports = function extend(Child, Parent, io, config, character) {
    Child.prototype = new Parent(io, config, character);
    Child.constructor = Child;
    return new Child(io, config, character);
};
