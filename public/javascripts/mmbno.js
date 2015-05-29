var socket = io();

$(document).ready
(
    function ()
    {
        socket.on('user connected', function () {
            alert('User connected');
        });

        socket.on('user disconnected', function () {
            alert('User disconnected');
        });
    }
);
