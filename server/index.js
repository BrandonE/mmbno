'use strict';

var fs = require('fs'),
    express = require('express'),
    app = express(),
    config = JSON.parse(fs.readFileSync(__dirname + '/../client/assets/config.json')),
    http = require('http').Server(app),
    io = require('socket.io')(http),
    socket = require(__dirname + '/socket')(config),
    server;

if (process.env.PORT) {
    config.port = process.env.PORT;
}

app.use(express.static(__dirname + '/../client/build'));

socket.attach(io);

server = http.listen(config.port, function() {
    console.log('Express server listening on port ' + server.address().port);
});
