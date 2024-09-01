// musicplay.js

const SongsList = [
    { path: 'music.mp3/Love_Story.mp3' },
    { path: 'music.mp3/Panda.mp3' },
    { path: 'music.mp3/rockstar.mp3' },
    { path: 'music.mp3/7_rings.mp3' },
    { path: 'music.mp3/11.mp3' },
    { path: 'music.mp3/50_feet.mp3' },
    { path: 'music.mp3/Alone.mp3' },
    { path: 'music.mp3/Animals.mp3' },
    { path: 'music.mp3/Baby.mp3' },
    { path: 'music.mp3/Black_In_Blask.mp3' },
    { path: 'music.mp3/Beliver.mp3' },
    { path: 'music.mp3/Billie_jean.mp3' },
    { path: 'music.mp3/Bohemian_Rhapsodty.mp3' },
    { path: 'music.mp3/Come_Around_Me.mp3' },
    { path: 'music.mp3/Cruel_Summer.mp3' },
    { path: 'music.mp3/Die_For_You.mp3' },
    { path: 'music.mp3/double_take.mp3' },
    { path: 'music.mp3/Faded.mp3' },
    { path: "music.mp3/God's_plain.mp3" },
    { path: "music.mp3/I'm_Not_Alone.mp3" },
    { path: 'music.mp3/Lean_On.mp3' },
    { path: 'music.mp3/Levitating.mp3' },
    { path: 'music.mp3/Like_That.mp3' },
    { path: "music.mp3/Livin'_On_A_Prayer.mp3" },
    { path: 'music.mp3/London_Calling.mp3' },
    { path: 'music.mp3/Look_At_Me!.mp3' },
    { path: 'music.mp3/Love_Story.mp3' },
    { path: 'music.mp3/Mr._Brightside.mp3' },
    { path: 'music.mp3/Needed_Me.mp3' },
    { path: 'music.mp3/NO_BYSTANDERS.mp3' },
    { path: 'music.mp3/Not_Like_Us.mp3' },
    { path: 'music.mp3/One_More_Time.mp3' },
    { path: 'music.mp3/Panda.mp3' },
    { path: 'music.mp3/Paris_In_The_Rain.mp3' },
    { path: 'music.mp3/Plain_Jane.mp3' },
    { path: 'music.mp3/Poker_Face.mp3' },
    { path: 'music.mp3/rockstar.mp3' },
    { path: 'music.mp3/Rolling_In_The_Deep.mp3' },
    { path: 'music.mp3/Shake_It.mp3' },
    { path: 'music.mp3/Shape_Of_You.mp3' },
    { path: 'music.mp3/Smells_Like_Teen_Spirit.mp3' },
    { path: 'music.mp3/Spectre.mp3' },
    { path: 'music.mp3/Stairway To Heaven.mp3' },
    { path: 'music.mp3/Starboy.mp3' },
    { path: "music.mp3/There's_Nothing_Holding_Me_Back.mp3" },
    { path: 'music.mp3/Titanium.mp3' },
    { path: 'music.mp3/Uprising.mp3' },
    { path: 'music.mp3/Wake_Me_Up.mp3' },
    { path: 'music.mp3/WAP.mp3' },
    { path: 'music.mp3/Wolves.mp3' },
    { path: 'music.mp3/You_Rock_My_World.mp3' }
];

let currentSongIndex = 0;

const audioPlayer = document.getElementById('audio_player');
const playPauseButton = document.getElementById('playandpause');
const prevButton = document.getElementById('previoussong');
const nextButton = document.getElementById('nextsong');

function loadSong(index) {
    if (index < 0 || index >= SongsList.length) return;
    audioPlayer.src = SongsList[index].path;
    audioPlayer.play();
    currentSongIndex = index;
}

function togglePlayPause() {
    if (audioPlayer.paused) {
        audioPlayer.play();
        playPauseButton.querySelector('ion-icon').setAttribute('name', 'pause-circle-outline');
        playPauseButton.querySelector('div').textContent = 'Pause';
    } else {
        audioPlayer.pause();
        playPauseButton.querySelector('ion-icon').setAttribute('name', 'play-circle-outline');
        playPauseButton.querySelector('div').textContent = 'Play';
    }
}

function playPreviousSong() {
    if (currentSongIndex > 0) {
        loadSong(currentSongIndex - 1);
    }
}

function playNextSong() {
    if (currentSongIndex < SongsList.length - 1) {
        loadSong(currentSongIndex + 1);
    }
}

playPauseButton.addEventListener('click', togglePlayPause);
prevButton.addEventListener('click', playPreviousSong);
nextButton.addEventListener('click', playNextSong);

// Automatically load the song if the page has a song path set
document.addEventListener('DOMContentLoaded', () => {
    if (audioPlayer.src) {
        loadSong(currentSongIndex);
    }
});
