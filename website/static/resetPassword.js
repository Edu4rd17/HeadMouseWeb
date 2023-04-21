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

const confirmPasswordInput = document.getElementById("confirm_password");
const confirmPasswordToggleIcon = document.querySelector(
  ".confirm_password-toggle-icon"
);

confirmPasswordToggleIcon.addEventListener("click", () => {
  if (confirmPasswordInput.type === "password") {
    confirmPasswordInput.type = "text";
    confirmPasswordToggleIcon.style.backgroundImage =
      "url('../static/images/show-icon.jpg')";
  } else {
    confirmPasswordInput.type = "password";
    confirmPasswordToggleIcon.style.backgroundImage =
      "url('../static/images/hide-icon.jpg')";
  }
});
