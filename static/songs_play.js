const SongsList = [
    { path: 'static/music.mp3/baby_lyric1.mp3' },
    { path: 'static/music.mp3/baby_lyric2.mp3' },
    { path: 'static/music.mp3/baby_lyric3.mp3' },
    { path: 'static/music.mp3/baby_lyric4.mp3' },
    { path: 'static/music.mp3/back_lyric1.mp3' },
    { path: 'static/music.mp3/back_lyric2.mp3' },
    { path: 'static/music.mp3/back_lyric3.mp3' },
    { path: 'static/music.mp3/believer_lyric1.mp3' },
    { path: 'static/music.mp3/believer_lyric2.mp3' },
    { path: 'static/music.mp3/die_lyric1.mp3' },
    { path: 'static/music.mp3/faded_lyric1.mp3' },
    { path: 'static/music.mp3/faded_lyric2.mp3' },
    { path: 'static/music.mp3/faded_lyric3.mp3' },
    { path: 'static/music.mp3/gods_plan_lyric1.mp3' },
    { path: 'static/music.mp3/lean_on_lyric1.mp3' },
    { path: 'static/music.mp3/lean_on_lyric2.mp3' },
    { path: 'static/music.mp3/love_story_lyric1.mp3' },
    { path: 'static/music.mp3/love_story_lyric2.mp3' },
    { path: "static/music.mp3/love_story_lyric3.mp3" },
    { path: "static/music.mp3/love_story_lyric4.mp3" },
    { path: 'static/music.mp3/love_story_lyric5.mp3' },
    { path: 'static/music.mp3/mean_lyric1.mp3' },
    { path: 'static/music.mp3/mean_lyric2.mp3' },
    { path: "static/music.mp3/rockstar_lyric1.mp3" },
    { path: 'static/music.mp3/wake_lyric1.mp3' },
    { path: 'static/music.mp3/wolves_lyric1.mp3' },
];

let currentSongIndex = 0;

const audioPlayer = document.getElementById('audio_player');
const songListContainer = document.getElementById('song-list');

function populateSongList(data) {
    let suggestions = '';
    data.forEach(function(song, index) {
        suggestions += `<li class="list-group-item link-class" data-index="${index}">${song.path.split('/').pop().replace('.mp3', '').replace(/_/g, ' ')}</li>`;
    });
    songListContainer.innerHTML = suggestions;
}

populateSongList(SongsList);

function loadSong(index) {
    if (index < 0 || index >= SongsList.length) return;
    if (currentSongIndex !== index) { 
        audioPlayer.src = SongsList[index].path;
        currentSongIndex = index;
        audioPlayer.play();
    }
}

songListContainer.addEventListener('click', function(e) {
    if (e.target && e.target.nodeName === 'LI') {
        const selectedSongIndex = parseInt(e.target.getAttribute('data-index'));
        loadSong(selectedSongIndex);
    }
});