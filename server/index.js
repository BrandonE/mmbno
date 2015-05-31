'use strict';

var fs = require('fs'),
    express = require('express'),
    app = express(),
    config = JSON.parse(fs.readFileSync(__dirname + '/../public/config.json')),
    http = require('http').Server(app),
    io = require('socket.io')(http),
    socket = require(__dirname + '/socket')(config),
    server;

if (process.env.PORT) {
    config.port = process.env.PORT;
}

app.set('views', __dirname, '../views');

app.use(express.static(__dirname + '/../public'));

app.get('/', function(req, res) {
    res.sendFile('index.html', {root : __dirname + '/../views'});
});

socket.attach(io);

server = http.listen(config.port, function() {
    console.log('Express server listening on port ' + server.address().port);
});
