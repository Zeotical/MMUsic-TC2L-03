
$(document).ready(function() {
    $('#text').keyup(function() {
        var searchQuery = $(this).val();
        if (searchQuery !== '') {
            $.ajax({
                url: '/livesearch',
                method: 'POST',
                data: { query: searchQuery },
                success: function(data) {
                    console.log(data);
                    let suggestions = '';
                    if (data.length > 0) {
                        data.forEach(function(item) {  // No need to reverse if Flask already sorts
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
                },
                error: function() {
                    $('#show-list').html('<li class="list-group-item link-class">Error retrieving data</li>');
                    $('#show-list').show();
                }
            });
        } else {
            $('#show-list').hide();  // Hide the suggestions if search query is empty
        }
    });
});


  // Hide the search result when clicking outside
$(document).on('click', function(e) {
    if (!$(e.target).closest('#text').length && !$(e.target).closest('#show-list').length) {
        $('#show-list').hide();
    }
});




    // Handle click on search result
    $(document).on('click', '.link-class', function() {
    
        var selectedFile = $(this).data('file');
        var filePath = '/static/music.mp3/' + selectedFile;
        console.log("Selected file path: ", filePath);

        // Set audio player source and play the selected song
        console.log("Selected file path: ", filePath);

        // Set audio player source and play the selected song
        $('#audio_player').attr('src', filePath);
        var audioPlayer = document.getElementById('audio_player');
        audioPlayer.play().then(() => {
            console.log('Playing the song');
        }).catch((error) => {
            console.error('Error playing the song:', error);
        });

        // Get the lyrics from the selected song
        var lyrics = $(this).find('small').text();

        // Append the profile picture, username, lyrics, and play icon to the chat
        $('#messages').append(`
            <li class="chat-message">
                <img src="${pfp_url}" class="chatpfp"> <span class="open">${username}</span> : ${lyrics} 
                <ion-icon name="play-circle-outline" class="play-icon" style="cursor:pointer;" data-file="${selectedFile}"></ion-icon>
            </li>
        `);

        // Clear the search box after selecting the lyric
        $('#text').val('');
        $('#show-list').hide();
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
