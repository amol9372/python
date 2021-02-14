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
  if (volcano_name == null || volcano_name == "") {
    enterNameValidation();
    return
  }

  filterUsingFetch({ volcano_name: volcano_name });
}

function enterNameValidation() {
  document.getElementById("name-validation").innerHTML =
    "Please enter Volcano Name";
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
      document.getElementById("name-validation").innerHTML = ""
    });
  //}).catch;
}
