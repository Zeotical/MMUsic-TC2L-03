$(function(){
    var socket = io.connect('http://' + location.hostname + ':' + location.port);
    var chatroomID = '{{ chatroomID }}';

    socket.on('connect', function() {
        socket.emit('joined', {chatroomID: chatroomID}); //This notifies the server that a new user has joined the chat
    });

    
    socket.on('message', function(data) {
        if (data.username==='System'){
            $('#messages').append('<li>' + data.username + ': ' + data.text + '</li>');
        }
        else {
        $('#messages').append('<li><img src=" '+ pfp_url + '" class="chatpfp"> <span class="open">' + data.username +' </span> : ' + data.text + '</li>');
    };

    $('#send').click(function(event) {
        event.preventDefault();
        var message = $('#text').val();
        if (message.trim() !== "") {
            socket.emit('text', {text: message, chatroomID: chatroomID}); //Emits a 'text' event to the server with the message
            $('#text').val('');
        }
    });

    $('#text').on('keypress', function(e) {
        if(e.which === 13) {
            $('#send').click();
        }
    });
});

$(document).on('click', '.open', function() {
    $('#modal_container').addClass('show');
});

$('#close').click(function() {
    $('#modal_container').removeClass('show');
});})
