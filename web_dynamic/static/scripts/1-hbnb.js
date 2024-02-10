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
});
