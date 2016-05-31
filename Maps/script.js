var map;

var type = getParameterByName("type");
var dataName = getParameterByName("dataName");
var centreLat = getParameterByName("centreLat");
var centreLat = getParameterByName("centreLon");

// If not Lat and Lon specified in URL then set to Sydney
centreLat = -33.8544439;
centreLon = 151.1839216;

if(type == null){
  alert("No type specified, try markers or heatmap");
}

if(dataName == null){
  alert("No dataName specified");
}

function initMap() {
  if(type == "markers") {
    map = new google.maps.Map(document.getElementById('map'), {
      center: {lat: centreLat, lng: centreLon},
      zoom: 8
    });
    doMarkers();
  } else {
    // Show the controls
    $('#floating-panel').show();
   map = new google.maps.Map(document.getElementById('map'), {
    zoom: 13,
    center: {lat: centreLat, lng: centreLon},
    mapTypeId: google.maps.MapTypeId.SATELLITE
  });

   heatmap = new google.maps.visualization.HeatmapLayer({
    data: getHMPoints(),
    map: map
  });

   function getHMPoints() {
    var points = [];

    d3.csv(dataName, function(csv){
      for(i = 0; i < csv.length; i++){
        console.log(csv[i].latitude, csv[i].longitude);
        var point = new google.maps.LatLng(csv[i].latitude, csv[i].longitude);
        points.push(point);
      }
      console.log(points);


    });

    return points;

  }
}
}

function getParameterByName(name, url) {
  if (!url) url = window.location.href;
  name = name.replace(/[\[\]]/g, "\\$&");
  var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
  results = regex.exec(url);
  if (!results) return null;
  if (!results[2]) return '';
  return decodeURIComponent(results[2].replace(/\+/g, " "));
}

function doMarkers() {
  var points = [];
  d3.csv(dataName, function(csv){
    for(i = 0; i < csv.length; i++){
      console.log(csv[i].latitude, csv[i].longitude);
      var icon = {
              url: csv[i].thumbURL, // url
              scaledSize: new google.maps.Size(50, 50), // scaled size
              origin: new google.maps.Point(0,0), // origin
              anchor: new google.maps.Point(0, 0), // anchor
            };

            var content = csv[i].caption + "<br><img src='" + csv[i].mainURL + "' class='mainImage'>"

            var infowindow = new google.maps.InfoWindow({
              content: "holding"
            }
            );
            
            var point = new google.maps.LatLng(csv[i].latitude, csv[i].longitude);
            
            // N.B. You have to add the infowindow content to the marker and then refrerence it later
            var marker = new google.maps.Marker({
              position: point,
              map: map,
              icon: icon,
              labelClass: "label",
              optimized:false,
              html: content
            });

            marker.addListener('click', function() {
              infowindow.setContent(this.html);
              infowindow.open(map, this);
            });
          }
        });

  var myoverlay = new google.maps.OverlayView();
  myoverlay.draw = function () {
    this.getPanes().markerLayer.id='markerLayer';
  };

  myoverlay.setMap(map);

}
function toggleHeatmap() {
  heatmap.setMap(heatmap.getMap() ? null : map);
}

function changeGradient() {
  var gradient = [
  'rgba(0, 255, 255, 0)',
  'rgba(0, 255, 255, 1)',
  'rgba(0, 191, 255, 1)',
  'rgba(0, 127, 255, 1)',
  'rgba(0, 63, 255, 1)',
  'rgba(0, 0, 255, 1)',
  'rgba(0, 0, 223, 1)',
  'rgba(0, 0, 191, 1)',
  'rgba(0, 0, 159, 1)',
  'rgba(0, 0, 127, 1)',
  'rgba(63, 0, 91, 1)',
  'rgba(127, 0, 63, 1)',
  'rgba(191, 0, 31, 1)',
  'rgba(255, 0, 0, 1)'
  ]
  heatmap.set('gradient', heatmap.get('gradient') ? null : gradient);
}

function changeRadius() {
  heatmap.set('radius', heatmap.get('radius') ? null : 5);
}

function changeOpacity() {
  heatmap.set('opacity', heatmap.get('opacity') ? null : 0.2);
}