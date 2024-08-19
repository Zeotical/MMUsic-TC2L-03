$(function(){
    var socket = io.connect('http://' + location.hostname + ':' + location.port);

    socket.on('connect', function() {
        socket.emit('joined', {});
    });

    socket.on('message', function(data) {
        $('#messages').append('<li>' + data.username + ': ' + data.text + '</li>');
    });

    $('#send').click(function() {
        var message = $('#txt').val();
        socket.emit('text', {text: message});
        $('#txt').val('');
    });

    $('#txt').on('keypress', function(e) {
        if(e.which === 13) {
            $('#send').click();
        }
    });
});