$(function(){
    var socket = io.connect('http://' + location.hostname + ':' + location.port);

    socket.on('connect', function() {
        socket.emit('joined', {}); //This notifies the server that a new user has joined the chat
    });

    socket.on('message', function(data) {
        $('#messages').append('<li>' + data.username + ': ' + data.text + '</li>');
    });

    $('#send').click(function() {
        var message = $('#text').val();
        socket.emit('text', {text: message}); //Emits a 'text' event to the server with the message
        $('#text').val('');
    });

    $('#text').on('keypress', function(e) {
        if(e.which === 13) {
            $('#send').click();
        }
    });
});