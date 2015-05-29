var socket = io();

$(document).ready
(
    function ()
    {
        socket.on('user connected', function (id) {
        });

        socket.on('user disconnected', function () {
        });

        $(document).keydown(function(e) {
            switch(e.which) {
                case 37:
                    socket.emit('move', 'left');
                    break;

                case 38:
                    socket.emit('move', 'up');
                    break;

                case 39:
                    socket.emit('move', 'right');
                    break;

                case 40:
                    socket.emit('move', 'down');
                    break;

                default:
                    return;
            }

            e.preventDefault();
        });
    }
);
