$(document).ready(function(){
    $('#text').keyup(function(){
        var searchQuery = $(this).val();
        if (searchQuery !== '') {
            $.ajax({
                url: '/livesearch',
                method: 'POST',
                data: { query: searchQuery },
                success: function(data) {
                    let suggestions = '';
                    if (data.length > 0) { 
                        data.forEach(function(item) {
                            suggestions += `<li class="list-group-item link-class" data-file="${item[2]}">${item[0]} - ${item[1]}</li>`;
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
        if (!$(e.target).closest('#text').length) {
            $('#show-list').hide();
        }
    });

    $(document).on('click', '.link-class', function(){
        var selectedFile = $(this).data('file');
        var filePath = '/static/music.mp3/' + selectedFile;
        $('#audio_player').attr('src', filePath);
        $('#text').val($(this).text()); 
        $('#show-list').hide();
        playPauseButton.querySelector('ion-icon').setAttribute('name', 'pause-circle-outline'); 
    });
});
