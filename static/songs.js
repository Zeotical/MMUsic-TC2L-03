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

    $(document).on('click', function(e) {
        if (!$(e.target).closest('#text').length && !$(e.target).closest('#show-list').length) {
            $('#show-list').hide();
        }
    });

    $(document).on('click', '.link-class', function() {
    

        var selectedFile = $(this).data('file');
        var filePath = '/static/music.mp3/' + selectedFile;
        console.log("Selected file path: ", filePath);
        $('#audio_player').attr('src', filePath);
        var lyrics = $(this).find('small').text();
        $('#messages').append(`<li> <img src="${pfp_url}" class="chatpfp" onclick="info_popup"> ${username}: ${lyrics}</li>`);
        $('#show-list').hide();
        var audioPlayer = document.getElementById('audio_player');
        audioPlayer.play().then(() => {
            console.log('Playing the song');
        }).catch((error) => {
            console.error('Error playing the song:', error);
        });
    });
});