const menu = document.querySelector("#menu-btn");
const navbar = document.querySelector(".header .navbar");

menu.onclick = () => {
  menu.classList.toggle("fa-times");
  navbar.classList.toggle("active");
};

function scrollDown() {
  window.scrollBy(0, 200);
}

function scrollUp() {
  window.scrollBy(0, -200);
}

// autocliking for the website
$(document).ready(function () {
  $("#start-click").click(function () {
    $.ajax({
      type: "POST",
      url: "/start-click",
      success: function (response) {
        displayFlashMessage(response);
      },
    });
  });

  $("#stop-click").click(function () {
    $.ajax({
      type: "POST",
      url: "/stop-click",
      success: function (response) {
        displayFlashMessage(response);
      },
    });
  });

  function displayFlashMessage(response) {
    var message = response.message;
    var category = response.category;
    var alertType = "alert-success";
    if (category == "error") {
      alertType = "alert-danger";
    }
    var html =
      '<div class="alert ' +
      alertType +
      ' alert-dismissable fade show div-alert-flash" role="alert">' +
      message +
      '<button type="button" class="close" data-dismiss="alert">' +
      '<span aria-hidden="true">&times;</span></button></div>';
    $("#flash-messages").html(html);
    setTimeout(function () {
      $(".alert").alert("close");
    }, 5000);
  }
});

//5 seconds after the page loads, the alert will be closed
setTimeout(function () {
  $(".alert").alert("close");
}, 5000);
