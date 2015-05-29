var IO = null;

var connect = function (socket) {
    IO.emit('user connected');
    console.log('user connected');
}

var disconnect = function () {
    IO.emit('user disconnected');
    console.log('user disconnected');
}

exports.attach = function(io) {
    IO = io;

    io.on('connection', function (socket) {
        connect(socket);
        socket.on('disconnect', disconnect);
    });
};
