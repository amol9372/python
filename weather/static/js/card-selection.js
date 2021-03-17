$(document).ready(function () {
  // ------------
  $(".radio-group .radio:first").addClass("selected");
  // classList[0].className.concat(" selected");

  $(".radio-group .radio").click(function () {
    $(".selected .fa").removeClass("fa-check");
    $(".radio").removeClass("selected");
    $(this).addClass("selected");
  });

  $("#user-location").on("keydown", function (event) {
    if (event.keyCode === 13) {
      $("#search-button").trigger("click");
      event.preventDefault();
    }
  });
});
