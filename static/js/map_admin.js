  // Icons

  var redIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
  });
 
var blueIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
  });

var greenIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
  });

var orangeIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-orange.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
  });
 
 
var violetIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-violet.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
  });

  var yellowIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-yellow.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
  });
  
  var blackIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-black.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
  });
  
  // L.marker([51.5, -0.09], {icon: greenIcon}).addTo(map);


  // L.marker([51.5, -0.09], {icon: greenIcon}).addTo(map);


// Function to add markers

function addMarkers(markers) {
  markers.forEach(function(marker) {
    var icon;
    switch(marker.incident_type) {
      case 'Agression sexuelle':
        icon = violetIcon; 
        break;
      case 'Dégradation':
        icon = greenIcon;
        break;
      case 'Harcèlement de rue':
        icon = redIcon;
        break;
      case 'Individu suspect':
        icon = blueIcon;
        break;
      case 'Individu violent':
        icon = yellowIcon;
        break;
      case 'Vol':
        icon = blackIcon;
        break;
      default:
        icon = orangeIcon;
    }

    var newMarker = L.marker([marker.lat, marker.long], {icon: icon});
    var popup = newMarker.bindPopup(`<h2 style="text-align: center">${marker.incident_type}</h2><h3>${marker.time}</h3>`).openPopup();
    switch(marker.incident_type) {
      case 'Agression sexuelle':
        popup.addTo(agressionSexuelleGroup);
        break;
      case 'Dégradation':
        popup.addTo(dégradationGroup);
        break;
      case 'Harcèlement de rue':
        popup.addTo(harcèlementderueGroup);
        break;
      case 'Individu suspect':
        popup.addTo(suspectIndividualGroup);
        break;
      case 'Individu violent':
        popup.addTo(violentIndividualGroup);
        break;
      case 'Vol':
        popup.addTo(volGroup);
        break;
      default:
        var popup1 = newMarker.bindPopup(`<h2 style="text-align: center;">Autre</h3><h3>${marker.time}</h3>`).openPopup();
        popup1.addTo(autreGroup);
    }
  });
}



 // Map creation
 var map = L.map('map').setView([48.685, 6.18], 13);


 // Layer initialisation
var layer = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {maxZoom: 19, attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'});
layer.addTo(map);



  // LayerGroup creations

var agressionSexuelleGroup = L.layerGroup().addTo(map);
var dégradationGroup = L.layerGroup().addTo(map);
var harcèlementderueGroup = L.layerGroup().addTo(map);
var suspectIndividualGroup = L.layerGroup().addTo(map);
var violentIndividualGroup = L.layerGroup().addTo(map);
var volGroup = L.layerGroup().addTo(map);
var autreGroup = L.layerGroup().addTo(map);


// Getting all markers and sort them to the right layerGroup

document.addEventListener('DOMContentLoaded', function() {


  function fetchAndDisplayMarkers() {
    agressionSexuelleGroup.clearLayers();
    dégradationGroup.clearLayers();
    harcèlementderueGroup.clearLayers();
    suspectIndividualGroup.clearLayers();
    violentIndividualGroup.clearLayers();
    volGroup.clearLayers();
    autreGroup.clearLayers();
    fetch('/all_markers/on')
    .then(response => response.json())
    .then(markers => {
        addMarkers(markers);
    })
    .catch(error => console.error('Error:', error));
  }
  fetchAndDisplayMarkers();
});


// Overaly creation

var overlays = {
  "Agression sexuelle 🟪": agressionSexuelleGroup,
  "Dégradation 🟩": dégradationGroup,
  "Harcèlement de rue 🟥": harcèlementderueGroup,
  "Individu suspect 🟦": suspectIndividualGroup,
  "Individu violent 🟨": violentIndividualGroup,
  "Vol ⬛️": volGroup,
  "Autre 🟧": autreGroup,
};


L.control.layers(null, overlays, { position: 'bottomright', collapsed : false}).addTo(map);




var resetViewControl = L.control({position: 'topleft'});

resetViewControl.onAdd = function (map) {
    var div = L.DomUtil.create('div', 'leaflet-bar leaflet-control leaflet-control-custom');

    div.innerHTML = '<button title="Reset view" style="font-size: 30px;">&#10227;</button>';
    div.onclick = function(){
        map.setView([48.685, 6.18], 13);
    }

    return div;
};


resetViewControl.addTo(map);




// City zoom

map.doubleClickZoom.disable(); 


document.querySelectorAll('.report').forEach(item => {
    item.addEventListener('click', event => {
      const lat = item.getAttribute('lat');
      const long = item.getAttribute('long');
      map.setView([lat, long], 19);
    });
  });