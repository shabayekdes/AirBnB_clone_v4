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
    fetchPlaces();
  });
  
const HOST = "0.0.0.0";

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
    data: JSON.stringify({}),
    success: function (response) {
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
