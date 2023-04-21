const passwordInput = document.getElementById("password");
const passwordToggleIcon = document.querySelector(".password-toggle-icon");

passwordToggleIcon.addEventListener("click", () => {
  if (passwordInput.type === "password") {
    passwordInput.type = "text";
    passwordToggleIcon.style.backgroundImage =
      "url('../static/images/show-icon.jpg')";
  } else {
    passwordInput.type = "password";
    passwordToggleIcon.style.backgroundImage =
      "url('../static/images/hide-icon.jpg')";
  }
});
