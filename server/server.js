'use strict';

var express = require('express'),
    app = express(),
    http = require('http').Server(app),
    io = require('socket.io')(http),
    socket_routes = require(__dirname + '/socket'),
    fs = require('fs'),
    server;

app.set('config', JSON.parse(fs.readFileSync(__dirname + '/config.json')));
app.set('views', __dirname, '../views');

app.use(express.static(__dirname + '/../public'));

app.get('/', function(req, res) {
    res.sendFile('index.html', {root : __dirname + '/../views'});
});

socket_routes.attach(io);

server = http.listen(app.get('config').port, function() {
    console.log('Express server listening on port ' + server.address().port);
});
