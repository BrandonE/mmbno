var socket = io(),
    clientPlayerNum = -1;

$(document).ready
(
    function ()
    {
        socket.on('user connected', function (playerNum) {
            if (clientPlayerNum === -1) {
                clientPlayerNum = playerNum;
                $('#playerNum').text(clientPlayerNum);
            }
        });

        socket.on('user disconnected', function (playerNum) {
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
