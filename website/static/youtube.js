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
        // console.log(data);
        var id = data.items[0].id.videoId;
        mainVideo(id);
        resultsLoop(data);
      }
    );
  }

  function mainVideo(id) {
    $("#video").html(
      `<iframe height="400" width="900" src="http://www.youtube.com/embed/${id}?autoplay=0&showinfo=0&controls=0" frameborder="0" allowfullscreen></iframe>`
    );
  }

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
    mainVideo(id);
  });
  function pauseVideo() {
    console.log('stopVideo');
    player.stopVideo();
}
});

// $(document).ready(function () {
//   var YT_API_KEY = "AIzaSyAsPHFeYLAiHxFm4-tgoLoaM-Fjy_yg3ws";
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
