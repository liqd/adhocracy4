window.jQuery(document).ready(function () {
  var L = window.L
  var polygon = window.polygon
  var point = window.point
  var baseurl = window.baseurl

  var basemap = baseurl + '{z}/{x}/{y}.png'
  var osmAttrib = '&copy; <a href="http://openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  var baselayer = L.tileLayer(basemap, {attribution: osmAttrib})
  var map = new L.Map('map', {scrollWheelZoom: false, zoomControl: false})
  baselayer.addTo(map)

  var polygonStyle = {
    'color': '#0076ae',
    'weight': 2,
    'opacity': 1,
    'fillOpacity': 0.2
  }

  var icon = L.icon({
    iconUrl: '/static/images/map_pin_01_2x.png',
    shadowUrl: '/static/images/map_shadow_01_2x.png',
    iconSize: [30, 45],
    iconAnchor: [15, 45],
    shadowSize: [40, 54],
    shadowAnchor: [20, 54],
    popupAnchor: [0, -45]
  })

  var basePolygon = L.geoJson(polygon, {style: polygonStyle}).addTo(map)
  map.fitBounds(basePolygon)
  map.options.minZoom = map.getZoom()
  L.control.zoom({
    position: 'topleft'
  }).addTo(map)

  L.geoJson(point, {
    pointToLayer: function (feature, latlng) {
      var marker = L.marker(latlng, {icon: icon}).addTo(map)
      return marker
    }
  })
})
