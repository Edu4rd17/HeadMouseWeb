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
