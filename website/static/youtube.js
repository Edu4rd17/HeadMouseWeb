$(document).ready(function () {

    var video = ''


    $("#form").submit(function (event) {
        event.preventDefault()

        var search = $("#search").val()
        if (search != "") {
            videoSearch(YT_API_KEY, search, 2)

        } else {
            alert("Please enter a search term")
        }
    })

    function videoSearch(key, search, maxResults) {

        $.get("https://www.googleapis.com/youtube/v3/search?key=" + key + "&type=video&part=snippet&maxResults=" + maxResults + "&q=" + search, function (data) {
            console.log(data)

            data.items.forEach(item => {
                video = `<iframe height="315" width="420" src="http://www.youtube.com/embed/${item.id.videoId}" frameborder="0" allowfullscreen></iframe> `
                $("#videos").append(video)
            });
        })
    }
})
