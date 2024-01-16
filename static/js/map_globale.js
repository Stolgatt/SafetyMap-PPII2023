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
      case 'Autres':
        icon = orangeIcon;
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
        var popup1 = newMarker.bindPopup(`<h2 style="text-align: center;">Autres</h3><h3>${marker.time}</h3>`).openPopup();
        popup1.addTo(autresGroup);
    }
  });
}

var map = L.map('map').setView([48.685, 6.18], 13);

function initMap(latitude, longitude) {
  map.setView([latitude, longitude], 13);
}

_lat = null;
_long = null;

function getLocation(){
  if ("geolocation" in navigator) {
    navigator.geolocation.getCurrentPosition(function(position) {
      _lat = position.coords.latitude;
      _long = position.coords.longitude;
      localStorage.setItem('geoPermission', 'granted');
      localStorage.setItem('latitude', _lat);
      localStorage.setItem('longitude', _long);
      initMap(_lat, _long);
    }, function() {
      localStorage.setItem('geoPermission', 'denied');
      initMap(48.685, 6.18);
    });
  } else {
    initMap(48.685, 6.18);
  }
}

window.onload = function() {
  var geoPermission = localStorage.getItem('geoPermission');
  _lat = parseFloat(localStorage.getItem('latitude'));
  _long = parseFloat(localStorage.getItem('longitude'));
  if (geoPermission === 'granted' && _lat && _long) {
    initMap(_lat, _long);
  } else if ( geoPermission === 'denied') {
    initMap(48.685, 6.18);
  } else {
    getLocation();
  }
}


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
var autresGroup = L.layerGroup().addTo(map);


// Getting all markers and sort them to the right layerGroup

document.addEventListener('DOMContentLoaded', function() {
  var toggleState = 'on';

  function fetchAndDisplayMarkers(state) {
    agressionSexuelleGroup.clearLayers();
    dégradationGroup.clearLayers();
    harcèlementderueGroup.clearLayers();
    suspectIndividualGroup.clearLayers();
    violentIndividualGroup.clearLayers();
    volGroup.clearLayers();
    autresGroup.clearLayers();
    fetch(`/all_markers/${state}`)
    .then(response => response.json())
    .then(markers => {
        addMarkers(markers);
    })
    .catch(error => console.error('Error:', error));
  }

  document.getElementById('toggleButton').addEventListener('click', function() {
    toggleState = toggleState === 'off' ? 'on' : 'off';
    fetchAndDisplayMarkers(toggleState);
  });

  fetchAndDisplayMarkers(toggleState);
});


// Overaly creation

var overlays = {
  "Agression sexuelle 🟪": agressionSexuelleGroup,
  "Dégradation 🟩": dégradationGroup,
  "Harcèlement de rue 🟥": harcèlementderueGroup,
  "Individu suspect 🟦": suspectIndividualGroup,
  "Individu violent 🟨": violentIndividualGroup,
  "Vol ⬛️": volGroup,
  "Autres 🟧": autresGroup,
};


L.control.layers(null, overlays, { position: 'bottomright', collapsed : false}).addTo(map);



//adding a custom control to reset the view

var resetViewControl = L.control({position: 'topleft'});

resetViewControl.onAdd = function (map) {
    var div = L.DomUtil.create('div', 'leaflet-bar leaflet-control leaflet-control-custom');

    div.innerHTML = '<button title="Reset view" style="font-size: 30px;">&#10227;</button>';
    div.onclick = function(){
      if (_lat && _long) {
        map.setView([_lat, _long], 13);
      } else {
        map.setView([48.685, 6.18], 13);
      }
    }

    return div;
};

// Ajoutez le contrôle personnalisé à la carte

resetViewControl.addTo(map);



var toggleButton = L.control({position: 'topleft'});

toggleButton.onAdd = function () {
    var div = L.DomUtil.create('div', 'leaflet-bar leaflet-control leaflet-control-custom');
    div.innerHTML = "<button title='Toggle Marker' id='toggleButton' style='font-size: 15px;font-family: 'Mukta';'>Changer d'affichage</button>";
    return div;
};

// Ajoutez le contrôle personnalisé à la carte

toggleButton.addTo(map);


// DB fetch + Chart creation (titre ne fonctionne pas)


const colors = {
  "Agression sexuelle": { backgroundColor: 'rgba(128, 0, 128, 0.4)', borderColor: 'rgba(128, 0, 128, 1)' },
  "Dégradation": { backgroundColor: 'rgba(0, 128, 0, 0.4)', borderColor: 'rgba(0, 128, 0, 1)' },
  "Harcèlement de rue": { backgroundColor: 'rgba(255, 0, 0, 0.4)', borderColor: 'rgba(255, 0, 0, 1)' },
  "Individu suspect": { backgroundColor: 'rgba(0, 0, 255, 0.4)', borderColor: 'rgba(0, 0, 255, 1)' },
  "Individu violent": { backgroundColor: 'rgba(255, 255, 0, 0.4)', borderColor: 'rgba(255, 255, 0, 1)' },
  "Vol": { backgroundColor: 'rgba(0, 0, 0, 0.4)', borderColor: 'rgba(0, 0, 0, 1)' },
  "Autres": { backgroundColor: 'rgba(255, 165, 0, 0.4)', borderColor: 'rgba(255, 165, 0, 1)' },
};


// Chart creation

document.addEventListener('DOMContentLoaded', function() {
  fetch('/get_pourcentage_from_database')
    .then(response => response.json())
    .then(data => {
      var backgroundColors = [];
      var borderColors = [];

      for (var i = 0; i < data.incident_type.length; i++) {
        var type = data.incident_type[i];
        var colorInfo = colors[type] || { backgroundColor: 'gray', borderColor: 'darkgray' };
        backgroundColors.push(colorInfo.backgroundColor);
        borderColors.push(colorInfo.borderColor);
      }

      var ctx = document.getElementById('myChart').getContext('2d');
      var myChart = new Chart(ctx, {
        type: 'pie',
        data: {
          labels: data.incident_type,
          datasets: [{
            data: data.pourcentage,
            backgroundColor: backgroundColors,
            borderColor: borderColors,
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            title: {
              display: true,
              text: "Répartition des incidents (en %)",
              color: "black",
              position: "top",
              font: {
                size: 20,
                family: "Mukta, sans serif",
                lineHeight: 1.2,
              },
            },
            legend: {
              display: true,
              position: "bottom",
              labels: {
                color: "black",
                font: {
                  size: 13,
                  family: "Mukta, sans serif",
                  lineHeight: 1.2,
                }
              }
            }
          }
        }
      });
    });
});




// City zoom

map.doubleClickZoom.disable(); 

var inputContainer = document.createElement('div');
inputContainer.className = 'input-container';

var input = document.createElement('input');
input.type = 'text';
input.id = 'cityName';
input.placeholder = 'Entrez le nom d\'une ville';

var button = document.createElement('button');
button.innerText = 'Zoom';
button.onclick = zoomToCity;

inputContainer.appendChild(input);
inputContainer.appendChild(button);

input.addEventListener('keyup', function(event) {
  if (event.key === 'Enter') {
    button.click();
  }
});

document.getElementById('map').appendChild(inputContainer);



function zoomToCity() {
  var cityName = document.getElementById('cityName').value;

  fetch('https://nominatim.openstreetmap.org/search?format=json&q=' + cityName)
    .then(response => response.json())
    .then(data => {
      if (data.length > 0) {
        var lat = data[0].lat;
        var lon = data[0].lon;
        map.setView([lat, lon], 13);
      } else {
        alert('Ville non trouvée');
      }
    })
    .catch(error => {
      console.error('Erreur:', error);
    });
}