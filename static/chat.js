$(document).ready(function() {
    var socket = io.connect('http://' + location.hostname + ':' + location.port);
    var chatroomID = document.getElementById('hiddenChatroomID').value;

    // Join the chatroom on connect
    socket.on('connect', function() {
        socket.emit('joined', { chatroomID: chatroomID });
    });

    $('#text').keyup(function() {
        var searchQuery = $(this).val();
        if (searchQuery !== '') {
            $.ajax({
                url: '/livesearch',
                method: 'POST',
                data: { query: searchQuery },
                success: function(data) {
                    let suggestions = '';
                    if (data.length > 0) {
                        data.reverse().forEach(function(item) {
                            suggestions += `<li class="list-group-item link-class" data-file="${item[3]}">
                                <strong>${item[0]} - ${item[1]}</strong><br>
                                <small>${item[2]}</small>
                            </li>`;
                        });
                        $('#show-list').show();
                    } else {
                        suggestions = '<li class="list-group-item link-class">No results found</li>';
                        $('#show-list').show();
                    }
                    $('#show-list').html(suggestions);
                }
            });
        } else {
            $('#show-list').hide();
        }
    });

    // Handle click on search result
    $(document).on('click', '.link-class', function() {
        var selectedFile = $(this).data('file');
        var filePath = '/static/music.mp3/' + selectedFile;
        var lyrics = $(this).find('small').text();

        // Set audio player source and play the selected song
        $('#audio_player').attr('src', filePath);
        var audioPlayer = document.getElementById('audio_player');
        audioPlayer.play().then(() => {
            console.log('Playing the song');
        }).catch((error) => {
            console.error('Error playing the song:', error);
        });

        // Emit selected lyrics to server
        console.log("Emitting to chatroomID:", chatroomID);

        socket.emit('selected-lyrics', { lyric: lyrics, file: selectedFile ,chatroomID:chatroomID});

        // Clear the search box after selecting the lyric
        $('#text').val('');
        $('#show-list').hide();
    });

    // Listen for messages and lyrics from the server
socket.on('message', function(data) {
    var username = data.username;
    var lyrics = data.lyric;
    var selectedFile = data.file;

    // If the message is from the system, display the message only
    if (data.username === 'System') {
        $('#messages').append('<li>' + data.username + ': ' + data.text + '</li>');
    } else {
        // Display the received lyrics with a play icon
        $('#messages').append(`
            <li class="chat-message">
                <img src="${pfp_url}" class="chatpfp"> <span class="open">${username}</span> : ${lyrics}
                <ion-icon name="play-circle-outline" class="play-icon" style="cursor:pointer;" data-file="${selectedFile}"></ion-icon>
            </li>
        `);
        
        // Automatically play the song associated with the received lyrics
        var filePath = '/static/music.mp3/' + selectedFile;
        $('#audio_player').attr('src', filePath);
        var audioPlayer = document.getElementById('audio_player');
        audioPlayer.play().then(() => {
            console.log('Auto-playing the song');
        }).catch((error) => {
            console.error('Error playing the song:', error);
        });

        //Get chat id
        // Get the current URL path
        var path = window.location.pathname; 
        // Split the path into segments
        var segments = path.split('/'); 
        // Get the last segment, which is the chatroom number
        var chatroomID = segments[segments.length - 1]; 
        console.log(chatroomID); 

        //Get date
        const now = new Date();
        const year = now.getFullYear();
        const month = String(now.getMonth() + 1).padStart(2, '0'); // Months are zero-indexed
        const day = String(now.getDate()).padStart(2, '0');
        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        const seconds = String(now.getSeconds()).padStart(2, '0');
    
        var createdDate =  `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`; 

        $.ajax({
            url: '/save',            
            type: 'POST',            
            contentType: 'application/json',  
            data: JSON.stringify({    
                message: lyrics,
                chatroom: chatroomID,
                musicfile: selectedFile,
                username: username
            }),
            success: function(response) {
                console.log('Success Post:', response);  
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);  
            }
        });
    }
});


    // Play song when play icon is clicked
    $(document).on('click', '.play-icon', function() {
        var selectedFile = $(this).data('file');
        var filePath = '/static/music.mp3/' + selectedFile;

        // Update the audio player source and play the selected song
        $('#audio_player').attr('src', filePath);
        var audioPlayer = document.getElementById('audio_player');
        audioPlayer.play().then(() => {
            console.log('Playing the song');
        }).catch((error) => {
            console.error('Error playing the song:', error);
        });
    });

    $(document).on('click', '.open', function() {
        $('#modal_container').addClass('show');
    });

    $('#close').click(function() {
        $('#modal_container').removeClass('show');
    });

    // Handle sending text messages
    $('#send').click(function(event) {
        event.preventDefault();
        var message = $('#text').val();
        if (message.trim() !== "") {
            socket.emit('text', { text: message, chatroomID: chatroomID });
            $('#text').val('');
        }
    });

    // Send message on enter key
    $('#text').on('keypress', function(e) {
        if(e.which === 13) {
            $('#send').click();
        }
    });
});

