var tag = document.createElement("script");

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName("script")[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var player;
function onYouTubeIframeAPIReady() {
  player = new YT.Player("existing-iframe", {
    height: "550",
    width: "1300",
    events: {
      onReady: onPlayerReady,
      onStateChange: onPlayerStateChange,
    },
  });
}

function onPlayerReady(event) {
  event.target.playVideo();
  videoDuration();
  liveVideoTime();
  var videoTitle = player.getVideoData().title;
  getCurrentVideoTitle(videoTitle);
  if (event.target && event.target.postMessage) {
    event.target.postMessage("Hello", "https://www.youtube.com");
  } else {
    // console.log("event.target does not have postMessage method");
  }
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

//get the live video time
function liveVideoTime(id) {
  //set a timer to update the video time every second
  if (player.getCurrentTime(id) != player.getDuration(id)) {
    setInterval(function () {
      var liveVideoTime = 0;
      liveVideoTime += formatTime(player.getCurrentTime(id));
      $("#liveVideoTime").html(`<p>Current Time: ${liveVideoTime}</p>`);
      // console.log(liveVideoTime);
    }, 1000);
  }
}

function getCurrentVideoTitle(videoTitle) {
  $("#current-video").html(
    `<h1 class="current-playing-video-title">Currently playing: ${videoTitle}</h1>`
  );
  // console.log(videoTitle);
}

function getCurrentVideoChannel(videoChannel) {
  $("#current-video-channel").html(
    `<h1 class="current-playing-video-channel">Channel: ${videoChannel}</h1>`
  );
}

//get the video duration
function videoDuration(id) {
  var videoDuration;
  videoDuration = formatTime(player.getDuration(id));
  $("#videoDuration").html(`<p>Video Duration: ${videoDuration}</p>`);
}

//rewind the video by 10 seconds
function rewindTenSec() {
  var currentTime = player.getCurrentTime();
  player.seekTo(currentTime - 10, true);
  player.playVideo();
}

//forward the video by 10 seconds
function forwardTenSec() {
  var currentTime = player.getCurrentTime();
  player.seekTo(currentTime + 10, true);
  player.playVideo();
}

//stop the video
function pauseVideo() {
  player.pauseVideo();
}

//play the video
function playVideo() {
  player.playVideo();
}

//mute the video
function muteVideo() {
  player.mute();
}

//unmute the video
function unMuteVideo() {
  player.unMute();
}

//volume up
function volumeUp() {
  var currVolume = player.getVolume();
  player.setVolume(currVolume + 10);
}

//volume down
function volumeDown() {
  var currVolume = player.getVolume();
  player.setVolume(currVolume - 10);
}

//slow down the video
function slowDownVideo() {
  var currSpeed = player.getPlaybackRate();
  player.setPlaybackRate(currSpeed - 0.25);
}

//speed up the video
function speedUpVideo() {
  var currSpeed = player.getPlaybackRate();
  player.setPlaybackRate(currSpeed + 0.25);
}

//normal speed
function normalSpeedVideo() {
  var currSpeed = player.getPlaybackRate();
  player.setPlaybackRate((currSpeed = 1));
}

//format the time
function formatTime(time) {
  time = Math.round(time);
  var minutes = Math.floor(time / 60),
    seconds = time - minutes * 60;
  seconds = seconds < 10 ? "0" + seconds : seconds;

  return minutes + ":" + seconds;
}

//send the src of the video to the iframe
function mainVideo(id) {
  document.getElementById(
    "existing-iframe"
  ).src = `https://www.youtube.com/embed/${id}?autoplay=1&showinfo=0&controls=0&enablejsapi=1&origin:www.youtube.com`;
}

$(document).ready(function () {
  //vars
  var YT_API_KEY = "AIzaSyCRUR04csuNXtP0lxrJAcQ0inxXtmxZSKw";
  var URL = "https://www.googleapis.com/youtube/v3/search?key=";
  var maxNumResults = 30;

  $(".clear-btn").click(function () {
    // Set search input field value to empty string
    $("#search").val("");
  });
  //check if form is submitted
  $("#form").submit(function (event) {
    // Prevent the form from submitting via the browser.
    event.preventDefault();
    // Add click event listener to clear button
    $(".clear-btn").click(function () {
      // Set search input field value to empty string
      $("#search").val("");
    });
    // Get the search term
    var search = $("#search").val();
    //check if search term is empty
    if (document.getElementById("search").value.trim().length > 0) {
      //call the videoSearch function
      videoSearch(YT_API_KEY, search, maxNumResults);
    } else {
      var flashMessage = `
      <div class="alert alert-danger alter-dismissable fade show div-alert-flash" role="alert">
        Please enter a search term
        <button type="button" class="close" data-dismiss="alert">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <script>
        setTimeout(function () {
          $(".alert").alert("close");
        }, 5000);
      </script>
    `;
      $("#flash-messages").html(flashMessage);
    }
  });

  //search for videos function takes in the api key, search term and max number of results
  function videoSearch(key, search, maxResults) {
    $.get(
      URL +
        key +
        "&part=snippet&maxResults=" +
        maxResults +
        "&type=video&q=" +
        search,
      function (data) {
        console.log(data);
        if (data.items.length == 0) {
          var flashMessage = `
          <div class="alert alert-danger alter-dismissable fade show div-alert-flash" role="alert">
            No videos found. Please try again.
            <button type="button" class="close" data-dismiss="alert">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <script>
            setTimeout(function () {
              $(".alert").alert("close");
            }, 5000);
          </script>
        `;
          $("#flash-messages").html(flashMessage);
        } else {
          $("#videos-title").html(
            `<h1 class="videos-title-text">If you wish to play another video simply select one from the list below!</h1>`
          );
          var id = data.items[0].id.videoId;
          var title = data.items[0].snippet.title;
          var channel = data.items[0].snippet.channelTitle;
          mainVideo(id);
          getCurrentVideoTitle(title);
          getCurrentVideoChannel(channel);
          // bring the user to the top of the page when a video is selected
          $("html, body").animate({ scrollTop: 211 }, "slow");
          //empty the main div before appending the results
          $("main").empty();
          resultsLoop(data);
          videoDuration(id);
          liveVideoTime(id);
        }
      }
    );
  }

  function resultsLoop(data) {
    $.each(data.items, function (i, item) {
      var thumb = item.snippet.thumbnails.medium.url;
      var title = item.snippet.title;
      var description = item.snippet.description.substring(0, 100);
      var vid = item.id.videoId;
      var channel = item.snippet.channelTitle;

      //append the results to the main div
      $("main").append(`
      <article class="item" data-key="${vid}">
        <img src="${thumb}" alt="" class="thumb" />
        <div class="details">
          <h4 class="video-title">${title}</h4>
          <p class="video-channel">${channel}</p>
          <p class="video-description">${description}</p>
        </div>
      </article>
      <hr />
    `);
    });
  }

  //click event for the playlist videos to play the selected video
  $("main").on("click", "article", function () {
    var id = $(this).attr("data-key");
    var title = $(this).find(".video-title").text(); // get the title from the clicked video
    var channel = $(this).find(".video-channel").text(); // get the channel from the clicked video
    mainVideo(id);
    getCurrentVideoTitle(title);
    getCurrentVideoChannel(channel);
    // bring the user to the top of the page when a video is selected
    window.scrollTo({
      top: 211,
      behavior: "smooth",
    });
  });
});

// This is the "Offline page" service worker
//fixes the service worker navigation preload reques
self.addEventListener("fetch", (event) => {
  // Respond to navigation preload requests
  if (event.request.mode === "navigate" && event.preloadResponse) {
    event.respondWith(
      // Wait for the preload response promise to settle
      event
        .waitUntil(event.preloadResponse)
        .then((response) => response || fetch(event.request))
    );
  }
});

document.getElementById("return-video").addEventListener("click", function () {
  window.scrollTo({
    top: 211,
    behavior: "smooth",
  });
});
