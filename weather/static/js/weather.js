let autocomplete;

const addressComponentTypes = [
  "sublocality_level_1", // area, sector, street
  "administrative_area_level_2", // city
  "administrative_area_level_1", // state
  "country",
  "postal_code",
];

function autoCompleteUserSearch() {
  const userInput = document.getElementById("user-location");

  const options = {
    //bounds: defaultBounds,
    componentRestrictions: { country: ["us", "in", "ca", "ru", "br"] },
    fields: [
      "address_components",
      "geometry",
      "icon",
      "name",
      "formatted_address",
    ],
    // origin: center,
    strictBounds: false,
    types: ["establishment"],
  };

  autocomplete = new google.maps.places.Autocomplete(userInput, options);
  //autocomplete.addListener("place_changed", onPlaceChanged);
}

function prepareLocationRequestBody() {
  var address = autocomplete.getPlace().address_components;
  var location = autocomplete.getPlace().geometry.location;
  var formattedAddress = autocomplete.getPlace().formatted_address;
  var filteredAddress = new Map();

  addressComponentTypes.forEach((validElement) => {
    address.forEach((addressElement) => {
      if (addressElement.types.includes(validElement)) {
        filteredAddress.set(validElement, addressElement.long_name);
      }
    });
  });

  filteredAddressJson = Object.fromEntries(filteredAddress);

  requestBody = {
    address: filteredAddressJson,
    location: location,
    formatted_address: formattedAddress,
  };

  return requestBody;
}

function changeDay(currentDay) {
  document.getElementById("wind").innerHTML =
    "Wind : " + currentDay.wind_speed + " Miles/hr";
  document.getElementById("humidity").innerHTML =
    "Humidity : " + currentDay.humidity + " %";

  document.getElementById("current-temp").innerHTML =
    "<h1>" + currentDay.temp.day + "°C" + "</h1>";
  document.getElementById("weather-icon").src = currentDay.weather[0].icon;
  document.getElementsByClassName("selected-day-of-week")[0].innerHTML =
    currentDay.dt;
}

function showWeatherForSelectedLocation() {
  var validation = document.getElementById("search-validation");
  if (autocomplete.getPlace() == null) {
    validation.style.display = "block";
    validation.innerHTML = "Please Select a Location which appears in search";
    return;
  }

  validation.style.display = "none";
  document.getElementById("search-label").innerHTML = "";
  document.getElementById("search-spinner").style.display = "block";
  requestBody = prepareLocationRequestBody();

  fetch("/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    //make sure to serialize your JSON body
    body: JSON.stringify(requestBody),
  })
    .then((data) => data.text())
    .then((value) => {
      //console.log(value)
      document.getElementById("search-spinner").style.display = "none";
      document.getElementById("search-label").innerHTML = "Search";
      document.getElementById("something").innerHTML = value;
    })
    .catch((er) => {
      console.log(er);
      document.getElementById("search-label").innerHTML = "Search";
      document.getElementById("search-spinner").style.display = "none";
    });
}

function isNullOrEmpty(value) {
  if (value == null || value.trim() == "") {
    return true;
  }

  return false;
}

function clear() {
  document.getElementById("abc").value = "";
}
