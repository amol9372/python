$(document).ready(function () {
  var options = {
    url : "static/names.json",

    //getValue: "name",

    list: {
      match: {
        enabled: true,
      }
    }

  };

  $("#volcano-name").easyAutocomplete(options);
});
