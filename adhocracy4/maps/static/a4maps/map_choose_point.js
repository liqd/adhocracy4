function createMap (L, baseurl, name) {
  var basemap = baseurl + '{z}/{x}/{y}.png'
  var osmAttrib = '&copy; <a href="http://openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  var baselayer = L.tileLayer(basemap, {maxZoom: 18, attribution: osmAttrib})
  var map = new L.Map('map_' + name, {scrollWheelZoom: false, zoomControl: false})
  baselayer.addTo(map)
  return map
}

function createMarker ($, L, newlatln, oldlatln, basePolygon, map, name) {
  var icon = L.icon({
    iconUrl: '/static/images/map_pin_01_2x.png',
    shadowUrl: '/static/images/map_shadow_01_2x.png',
    iconSize: [30, 45],
    iconAnchor: [15, 45],
    shadowSize: [40, 54],
    shadowAnchor: [20, 54],
    popupAnchor: [0, -45]
  })

  var marker = L.marker(newlatln, { draggable: true, icon: icon }).addTo(map)
  marker.on('dragend', function () {
    var markerInsidePolygon = false
    basePolygon.getLayers().forEach(function (each) {
      if (isMarkerInsidePolygon(marker, each)) {
        markerInsidePolygon = true
        oldlatln = marker.getLatLng()
        var shape = marker.toGeoJSON()
        $('#id_' + name).val(JSON.stringify(shape))
      }
    })
    if (!markerInsidePolygon) {
      marker.setLatLng(oldlatln)
    }
  })
  return marker
}

function isMarkerInsidePolygon (marker, poly) {
  var polyPoints = poly.getLatLngs()
  var x = marker.getLatLng().lat
  var y = marker.getLatLng().lng

  var inside = false
  for (var i = 0, j = polyPoints.length - 1; i < polyPoints.length; j = i++) {
    var xi = polyPoints[i].lat
    var yi = polyPoints[i].lng
    var xj = polyPoints[j].lat
    var yj = polyPoints[j].lng

    var intersect = ((yi > y) !== (yj > y)) &&
        (x < (xj - xi) * (y - yi) / (yj - yi) + xi)
    if (intersect) inside = !inside
  }
  return inside
}

window.jQuery(document).ready(function () {
  var $ = window.jQuery
  var L = window.L
  var name = window.name
  var polygon = window.polygon
  var point = window.point
  var baseurl = window.baseurl
  var map = createMap(L, baseurl, name)

  var polygonStyle = {
    'color': '#0076ae',
    'weight': 2,
    'opacity': 1,
    'fillOpacity': 0.2
  }

  var basePolygon = L.geoJson(polygon, {style: polygonStyle}).addTo(map)
  map.fitBounds(basePolygon)
  map.options.minZoom = map.getZoom()
  L.control.zoom({
    position: 'topleft'
  }).addTo(map)

  var marker

  if (point) {
    L.geoJson(point, {
      pointToLayer: function (feature, newlatlng) {
        var oldlatlng = newlatlng
        marker = createMarker($, L, newlatlng, oldlatlng, basePolygon, map, name)
        return marker
      }
    })
  }

  basePolygon.on('click', function (event) {
    if (typeof marker === 'undefined') {
      var oldlatlng = event.latlng
      marker = createMarker($, L, event.latlng, oldlatlng, basePolygon, map, name)
      var shape = marker.toGeoJSON()
      $('#id_' + name).val(JSON.stringify(shape))
    }
  })
})
