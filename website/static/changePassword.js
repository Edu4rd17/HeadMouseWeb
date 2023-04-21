const passwordInput = document.getElementById("currentPassword");
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

const newPasswordInput = document.getElementById("newPassword");
const newPasswordToggleIcon = document.querySelector(
  ".newPassword-toggle-icon"
);

newPasswordToggleIcon.addEventListener("click", () => {
  if (newPasswordInput.type === "password") {
    newPasswordInput.type = "text";
    newPasswordToggleIcon.style.backgroundImage =
      "url('../static/images/show-icon.jpg')";
  } else {
    newPasswordInput.type = "password";
    newPasswordToggleIcon.style.backgroundImage =
      "url('../static/images/hide-icon.jpg')";
  }
});

const confirmPasswordInput = document.getElementById("confirmNewPassword");
const confirmPasswordToggleIcon = document.querySelector(
  ".confirmNewPassword-toggle-icon"
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
