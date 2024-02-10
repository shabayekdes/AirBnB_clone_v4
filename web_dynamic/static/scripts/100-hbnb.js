const HOST = "0.0.0.0";
const show_amenity = {};
const show_state = {};
const show_city = {};
let obj = {};

$(document).ready(function init() {
  $(".amenities .popover input").change(function () {
    obj = show_amenity;
    checkedObjects.call(this, 1);
  });
  $(".state_input").change(function () {
    obj = show_state;
    checkedObjects.call(this, 2);
  });
  $(".city_input").change(function () {
    obj = show_city;
    checkedObjects.call(this, 3);
  });
  apiStatus();
  fetchPlaces();
});

function checkedObjects(nObject) {
  if ($(this).is(":checked")) {
    obj[$(this).attr("data-name")] = $(this).attr("data-id");
  } else if ($(this).is(":not(:checked)")) {
    delete obj[$(this).attr("data-name")];
  }
  const names = Object.keys(obj);
  if (nObject === 1) {
    $(".amenities h4").text(names.sort().join(", "));
  } else if (nObject === 2) {
    $(".locations h4").text(names.sort().join(", "));
  }
}

function apiStatus() {
  const API_URL = `http://${HOST}:5001/api/v1/status/`;
  $.get(API_URL, (data, textStatus) => {
    if (textStatus === "success" && data.status === "OK") {
      $("#api_status").addClass("available");
    } else {
      $("#api_status").removeClass("available");
    }
  });
}

function fetchPlaces() {
  $.ajax({
    url: `http://${HOST}:5001/api/v1/places_search/`,
    type: "POST",
    headers: { "Content-Type": "application/json" },
    data: JSON.stringify({
      amenities: Object.values(show_amenity),
      states: Object.values(show_state),
      cities: Object.values(show_city),
    }),
    success: function (response) {
      $("SECTION.places").empty();
      for (const res of response) {
        const article = [
          "<article>",
          '<div class="title_box">',
          `<h2>${res.name}</h2>`,
          `<div class="price_by_night">$${res.price_by_night}</div>`,
          "</div>",
          '<div class="information">',
          `<div class="max_guest">${res.max_guest} Guest(s)</div>`,
          `<div class="number_rooms">${res.number_rooms} Bedroom(s)</div>`,
          `<div class="number_bathrooms">${res.number_bathrooms} Bathroom(s)</div>`,
          "</div>",
          '<div class="description">',
          `${res.description}`,
          "</div>",
          "</article>",
        ];
        $("SECTION.places").append(article.join(""));
      }
    },
    error: function (error) {
      console.log(error);
    },
  });
}
