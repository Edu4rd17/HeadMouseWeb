$(document).ready(function () {
  var YT_API_KEY = "";
  var URL = "https://www.googleapis.com/youtube/v3/search?key=";
  var maxNumResults = 20;

  // $("#form")[0].reset();
  $("#form").submit(function (event) {
    // Prevent the form from submitting via the browser.
    event.preventDefault();
    // Get the search term
    var search = $("#search").val();
    if (document.getElementById("search").value.trim().length > 0) {
      videoSearch(YT_API_KEY, search, maxNumResults);
    } else {
      alert("Please enter a search term");
    }
  });

  function videoSearch(key, search, maxResults) {
    $.get(
      URL +
        key +
        "&type=video&part=snippet&maxResults=" +
        maxResults +
        "&q=" +
        search,
      function (data) {
        console.log(data);
        var id = data.items[0].id.videoId;
        mainVideo(id);
        resultsLoop(data);
      }
    );
  }

  // function mainVideo(id) {
  //   $("#video").html(
  //     `<iframe height="400" width="900" src="http://www.youtube.com/embed/${id}?autoplay=0&showinfo=0&controls=0" frameborder="0" allowfullscreen></iframe>`
  //   );
  // }

  function resultsLoop(data) {
    $.each(data.items, function (i, item) {
      var thumb = item.snippet.thumbnails.medium.url;
      var title = item.snippet.title;
      var description = item.snippet.description.substring(0, 100);
      var vid = item.id.videoId;

      $("main").append(`
      <article class="item" data-key="${vid}">
        <img src="${thumb}" alt="" class="thumb" />
        <div class="details">
          <h4 class="video-title">${title}</h4>
          <p class="video-description">${description}</p>
        </div>
      </article>
    `);
    });
  }

  $("main").on("click", "article", function () {
    var id = $(this).attr("data-key");
    console.log(id);
    videoDuration(id);
    playSelectedVideo(id);
  });
});

var tag = document.createElement("script");

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName("script")[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var player;
function mainVideo(id) {
  player = new YT.Player("video", {
    height: "500",
    width: "1200",
    videoId: id,
    autoplay: 1,
    playerVars: {
      controls: 0,
      showinfo: 0,
      rel: 0,
      modestbranding: 1,
      order: "date",
      // enablejsapi: 1
    },
    events: {
      onReady: onPlayerReady,
      onStateChange: onPlayerStateChange,
    },
  });
}

function playSelectedVideo(id) {
  player.loadVideoById(id);
  // player.playVideo();
}

function onPlayerReady(event) {
  event.target.playVideo();
  videoDuration();
  // liveVideoTime();
}

// function playNextVideo() {
//   var seconds;
//   if (seconds == player.getDuration()) {
//     player.nextVideo();
//     player.playVideo();
//   }
// }

function liveVideoTime() {
  var liveVideoTime;
  liveVideoTime += formatTime(player.getCurrentTime());
  $("#liveVideoTime").html(`<p>Current Time: ${liveVideoTime}</p>`);
}

function videoDuration(id) {
  var videoDuration = 0;
  videoDuration = formatTime(player.getDuration(id));
  $("#videoDuration").html(`<p>Video Duration: ${videoDuration}</p>`);
  // console.log(videoDuration);
}

function formatTime(time) {
  time = Math.round(time);

  var minutes = Math.floor(time / 60),
    seconds = time - minutes * 60;

  seconds = seconds < 10 ? "0" + seconds : seconds;

  return minutes + ":" + seconds;
}

function onPlayerStateChange(event) {
  if (player.getPlayerState() === 1 || player.getPlayerState() === 2) {
    //forward the video by 10 seconds
    $("#fwrd").prop("disabled", false);
    $("#fwrd").click(function () {
      forwardTenSec();
    });

    //rewind the video by 10 seconds
    $("#rwnd").prop("disabled", false);
    $("#rwnd").click(function () {
      rewindTenSec();
    });

    //stop the video
    $("#pause").prop("disabled", false);
    $("#pause").click(function () {
      pauseVideo();
    });

    //play the video
    $("#play").prop("disabled", false);
    $("#play").click(function () {
      playVideo();
    });

    //play the next video
    // $("#playNext").click(function () {
    //   playNextVideo();
    // });

    //mute the video
    $("#mute").prop("disabled", false);
    $("#mute").click(function () {
      muteVideo();
    });

    //unmute the video
    $("#unMute").prop("disabled", false);
    $("#unMute").click(function () {
      unMuteVideo();
    });

    //volume up
    $("#volumeUp").prop("disabled", false);
    $("#volumeUp").click(function () {
      volumeUp();
    });

    //volume down
    $("#volumeDown").prop("disabled", false);
    $("#volumeDown").click(function () {
      volumeDown();
    });

    //slow down the video
    $("#slowerVideo").prop("disabled", false);
    $("#slowerVideo").click(function () {
      slowDownVideo();
    });

    //speed up the video
    $("#fasterVideo").prop("disabled", false);
    $("#fasterVideo").click(function () {
      speedUpVideo();
    });

    //normal speed
    $("#normalSpeed").prop("disabled", false);
    $("#normalSpeed").click(function () {
      normalSpeedVideo();
    });
  } else {
    //disable the buttons
    $("#rwnd").prop("disabled", true);
    $("#fwrd").prop("disabled", true);
    $("#pause").prop("disabled", true);
    $("#play").prop("disabled", true);
    $("#mute").prop("disabled", true);
    $("#unMute").prop("disabled", true);
    $("#volumeUp").prop("disabled", true);
    $("#volumeDown").prop("disabled", true);
    $("#slowerVideo").prop("disabled", true);
    $("#fasterVideo").prop("disabled", true);
    $("#normalSpeed").prop("disabled", true);
  }
}

function rewindTenSec() {
  var currentTime = player.getCurrentTime();
  player.seekTo(currentTime - 10, true);
  player.playVideo();
}

function forwardTenSec() {
  var currentTime = player.getCurrentTime();
  player.seekTo(currentTime + 10, true);
  player.playVideo();
}

function pauseVideo() {
  player.pauseVideo();
}

function playVideo() {
  player.playVideo();
}

// function playNextVideo() {
//   player.nextVideo();
// }

function muteVideo() {
  player.mute();
}

function unMuteVideo() {
  player.unMute();
}

function volumeUp() {
  var currVolume = player.getVolume();
  player.setVolume(currVolume + 10);
}

function volumeDown() {
  var currVolume = player.getVolume();
  player.setVolume(currVolume - 10);
}

function slowDownVideo() {
  var currSpeed = player.getPlaybackRate();
  player.setPlaybackRate(currSpeed - 0.5);
}

function speedUpVideo() {
  var currSpeed = player.getPlaybackRate();
  player.setPlaybackRate(currSpeed + 0.5);
}

function normalSpeedVideo() {
  var currSpeed = player.getPlaybackRate();
  player.setPlaybackRate((currSpeed = 1));
}

// $(document).ready(function () {
//   var YT_API_KEY = "";
//   var video = "";

//   $("#form").submit(function (event) {
//     // Prevent the form from submitting via the browser.
//     event.preventDefault();

//     // Get the search term
//     var search = $("#search").val();
//     if (search != "") {
//       videoSearch(YT_API_KEY, search, 17);
//     } else {
//       alert("Please enter a search term");
//     }
//   });

//   function videoSearch(key, search, maxResults) {
//     $.get(
//       "https://www.googleapis.com/youtube/v3/search?key=" +
//         key +
//         "&type=video&part=snippet&maxResults=" +
//         maxResults +
//         "&q=" +
//         search,
//       function (data) {
//         console.log(data);

//         data.items.forEach((item) => {
//           video = `<iframe height="315" width="420" src="http://www.youtube.com/embed/${item.id.videoId}" frameborder="0" allowfullscreen></iframe> `;
//           $("#videos").append(video);
//         });
//       }
//     );
//   }
// });
