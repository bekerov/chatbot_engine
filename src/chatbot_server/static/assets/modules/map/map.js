function Map() {
    
    var that = this;
    var map;
    var makers;

    this.setMarkers = function(markers){

      map = new google.maps.Map(document.getElementById('map'), {
        center: {'lat': lat, 'lng':lng},
        zoom: 13
      });
      getLocation();

      $.ajax({
          url:'./time.php',
          success:function(data){
              $('#time').append(data);
          }
      })


      //marker_info 
      // marker 
      ehwa_latlng = {lat: 37.558612, lng:126.945669};
      md_latlng = {lat:37.565668, lng:126.983142};
      
      generateMarker('ehwa_spot', ehwa_latlng) 
      generateMarker('md_spot', md_latlng)

    }

    this.generateMarker = function(spot_name, latlng){

      var marker = new google.maps.Marker({
        position: latlng,
        title: spot_name
      });
      markers.push(marker)

      marker.setMap(map); 
      marker.addListener('click', function() {
        selected_spot = this.title
        var infowindow = new google.maps.InfoWindow({
          content: 'Selected Spot!'
        });
        infowindow.open(map, this); 

        updateCarrySpot(selected_spot)

      });
    }
}
