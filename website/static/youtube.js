$(document).ready(function () {
  var YT_API_KEY = "";
  var URL = "https://www.googleapis.com/youtube/v3/search?key=";
  var maxNumResults = 20;

  $("#form").submit(function (event) {
    // Prevent the form from submitting via the browser.
    event.preventDefault();

    // Get the search term
    var search = $("#search").val();
    if (search != " ") {
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
    // alert(id);
    console.log(mainVideo(id));
    mainVideo(id);
  });
});

var tag = document.createElement("script");

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName("script")[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var player;
function mainVideo(id) {
  player = new YT.Player("video", {
    height: "400",
    width: "900",
    videoId: id,
    autoplay: 1,
    playerVars: {
      controls: 0,
    },
    events: {
      onReady: onPlayerReady,
      onStateChange: onPlayerStateChange,
    },
  });
}

function onPlayerReady(event) {
  event.target.playVideo();
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
    // $("#stop").prop("disabled", false);
    $("#pause").click(function () {
      pauseVideo();
    });

    //play the video
    // $("#play").prop("disabled", false);
    $("#play").click(function () {
      playVideo();
    });

    //play the next video
    // $("#playNext").click(function () {
    //   playNextVideo();
    // });

    //mute the video
    $("#mute").click(function () {
      muteVideo();
    });

    //unmute the video
    $("#unMute").click(function () {
      unMuteVideo();
    });

    //volume up
    $("#volumeUp").click(function () {
      volumeUp();
    });

    //volume down
    $("#volumeDown").click(function () {
      volumeDown();
    });
  } else {
    //disable the buttons
    $("#rwnd").prop("disabled", true);
    $("#fwrd").prop("disabled", true);
    // $("#stop").prop("disabled", true);
    // $("#play").prop("disabled", true);
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
