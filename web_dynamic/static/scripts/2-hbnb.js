$(document).ready(function () {
  const show_amenity = {};
  $(".amenities .popover input").change(function () {
    if ($(this).is(":checked")) {
      show_amenity[$(this).attr("data-name")] = $(this).attr("data-id");
    } else if ($(this).is(":not(:checked)")) {
      delete show_amenity[$(this).attr("data-name")];
    }
    const names = Object.keys(show_amenity);
    $(".amenities h4").text(names.sort().join(", "));
  });

  apiStatus();
});


function apiStatus() {
  const API_URL = `http://0.0.0.0:5001/api/v1/status/`;
  $.get(API_URL, (data, textStatus) => {
    if (textStatus === "success" && data.status === "OK") {
      $("#api_status").addClass("available");
    } else {
      $("#api_status").removeClass("available");
    }
  });
}
