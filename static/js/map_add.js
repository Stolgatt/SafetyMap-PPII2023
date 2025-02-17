/// PARTIE FORMULAIRE ///

// Set date to today's date

const dateControl = document.querySelector('#date');

const date = new Date();
let day = date.getDate();
let month = date.getMonth() + 1;
let year = date.getFullYear();
if (day < 10) {
    day = `0${day}`;
  }
if (month < 10) {
    month = `0${month}`;
  }
let currentDate = `${year}-${month}-${day}`;

dateControl.value = currentDate;


// Set hour to current hour

const hourControl = document.querySelector('input[type="time"]');
const hour = new Date();
let hourNow = hour.getHours();
let minutesNow = hour.getMinutes();
if (hourNow < 10) {
    hourNow = `0${hourNow}`;
  }
if (minutesNow < 10) {
    minutesNow = `0${minutesNow}`;
  }
let currentHour = `${hourNow}:${minutesNow}`;
hourControl.value = currentHour;



/// PARTIE MAP ///

  // Map creation

var map = L.map('map').setView([48.685, 6.18], 12);

  // Truc initialisation
var layer = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {maxZoom: 19, attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'});
  layer.addTo(map);



  // Reset view button (ne fonctionne pas)

  var resetViewControl = L.control({position: 'topleft'});

  resetViewControl.onAdd = function (map) {
      var div = L.DomUtil.create('div', 'leaflet-bar leaflet-control leaflet-control-custom');
  
      div.innerHTML = '<button title="Reset view" style="font-size: 25px;">&#10227;</button>';
      div.onclick = function(){
          map.setView([48.685, 6.18], 12);
      }
  
      return div;
  };
resetViewControl.addTo(map);

  
// Function to add marker on double click

init_marker = null;
function onMapDoubleClick(e) {
    if (init_marker) {
        map.removeLayer(init_marker);
    }

    init_marker = L.marker(e.latlng).addTo(map);
    // init_marker.bindPopup("Marqueur placé à : " + e.latlng.toString()).openPopup();
}

map.on('dblclick', (e) => {
  onMapDoubleClick(e);
  var position = init_marker.getLatLng();
    let long = position.lng;
    let lat = position.lat;
  
    const longControl = document.querySelector('#long');
    longControl.value = long.toFixed(5);
    const latControl = document.querySelector('#lat');
    latControl.value = lat.toFixed(5);
}); 



  // Get coordinates from marker

var long = 6.18;
var lat = 48.685;

const longControl = document.querySelector('#long');
longControl.value = long.toFixed(5);
const latControl = document.querySelector('#lat');
latControl.value = lat.toFixed(5);


map.doubleClickZoom.disable();