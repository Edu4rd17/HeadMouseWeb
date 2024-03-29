//list of countries in the world

document.addEventListener("DOMContentLoaded", () => {
  const selectDropCountry = document.querySelector("#country");

  fetch("https://restcountries.com/v2/all")
    .then((res) => {
      return res.json();
    })
    .then((data) => {
      let output = `<option value="">-Select Country-</option>`;
      output += `<option value="Ireland">Ireland</option>`;
      data.forEach((country) => {
        output += `<option value="${country.name}">${country.name}</option>`;
      });
      selectDropCountry.innerHTML = output;
    })
    .catch((err) => {
      console.log(err);
    });
});

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

const confirmPasswordInput = document.getElementById("password2");
const confirmPasswordToggleIcon = document.querySelector(
  ".password2-toggle-icon"
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
