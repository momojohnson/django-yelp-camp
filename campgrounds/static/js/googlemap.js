function initMap() {
    var lat = Number($('#lat').text());
    var lng = Number($('#lng').text());
    console.log(lng)
    console.log(lat)
    var center = {lat: lat, lng: lng };
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 8,
        center: center,
        scrollwheel: false
    });
    var campgroundName = $('.campground-name').text(),
        campgroundLocation = $('#loc').text(),
        campgroundDescription = $('.campground-description').text();
        console.log("Location"+campgroundLocation)
    var contentString = "<strong>"+ campgroundName +"<br />"
        + campgroundLocation + "</strong>" +
      "<p>"+ campgroundDescription + "</p>";
    var infowindow = new google.maps.InfoWindow({
      content: contentString
    });
    var marker = new google.maps.Marker({
        position: center,
        map: map
    });
    marker.addListener('click', function() {
      infowindow.open(map, marker);
    });
  }