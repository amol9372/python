let autocomplete;

function filterByCountry() {
  var country = document.getElementById("country").value;
  filterUsingFetch({ country: country });
}

function filterByType() {
  var type = document.getElementById("volcano-type").value;
  filterUsingFetch({ primary_volcano_type: type });
}

function filterByElevation() {
  var elevation = document.getElementById("elevation").value;
  filterUsingFetch({ elevation: elevation });
}

function searchByName() {
  var volcano_name = document.getElementById("volcano-name").value;
  var userLocation = document.getElementById("user-location").value;
  var advancedFilter = document.getElementById("flexSwitchCheckDefault");
  var radiusInKm = document.getElementById("search-radius").value;

  if (advancedFilter.checked) {
    if (isNullOrEmpty(userLocation)) {
      runValidation("user-location-validation");
    }
    findNearestVolcanoes({
      location: autocomplete.getPlace().geometry.location,
      radius: radiusInKm,
    });
  } else if (isNullOrEmpty(volcano_name)) {
    runValidation("name-validation");
  } else {
    filterUsingFetch({ volcano_name: volcano_name });
  }
}

function runValidation(element) {
  document.getElementById(element).innerHTML = "Field cannot be blank";
}

function filterUsingFetch(request_body) {
  fetch("/filter", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    //make sure to serialize your JSON body
    body: JSON.stringify(request_body),
  })
    .then((response) => {
      var iframe = document.getElementById("map");
      console.log(response);
      iframe.contentWindow.location.reload(true);
    })
    .then((r) => {
      document.getElementById("filter-form").reset();
      document.getElementsByClassName("advanced-search")[0].style.display =
        "none";
      document.getElementById("name-validation").innerHTML = "";
    });
  //}).catch;
}

function autoCompleteUserSearch() {
  const userInput = document.getElementById("user-location");

  const options = {
    //bounds: defaultBounds,
    componentRestrictions: { country: "us" },
    fields: ["address_components", "geometry", "icon", "name"],
    // origin: center,
    strictBounds: false,
    types: ["establishment"],
  };

  autocomplete = new google.maps.places.Autocomplete(userInput, options);
  autocomplete.addListener("place_changed", onPlaceChanged);
}

function onPlaceChanged() {
  var location = autocomplete.getPlace().geometry.location;
  console.log(location);

  // search nearest volcanoes to the location
  //findNearestVolcanoes({"location": location, "radius": radiusInKm})
}

function toggleAdvanceSearch() {
  var advancedSearch = document.getElementsByClassName("advanced-search")[0];
  if (advancedSearch.style.display == "none") {
    advancedSearch.style.display = "block";
  } else {
    advancedSearch.style.display = "none";
  }
}

function findNearestVolcanoes(request_body) {
  fetch("/search-nearest-volcanoes", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    //make sure to serialize your JSON body
    body: JSON.stringify(request_body),
  })
    .then((response) => {
      var iframe = document.getElementById("map");
      console.log(response);
      iframe.contentWindow.location.reload(true);
    })
    .then((r) => {
      //document.getElementById("filter-form").reset();
      // document.getElementById("name-validation").innerHTML = "";
    });
}

function isNullOrEmpty(value) {
  if (value == null || value.trim() == "") {
    return true;
  }

  return false;
}
