function createMap (L, baseurl, attribution, e) {
  var basemap = baseurl + '{z}/{x}/{y}.png'
  var baselayer = L.tileLayer(basemap, {maxZoom: 18, attribution: attribution})
  var map = new L.Map(e, {scrollWheelZoom: false, zoomControl: false})
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

function getLines (array) {
  var output = []
  if (array.length) {
    if ('lat' in array[0]) {
      for (var i = 0, j = array.length - 1; i < array.length; j = i++) {
        output.push([array[i], array[j]])
      }
    } else {
      array.forEach(function (a) {
        getLines(a).forEach(function (line) {
          output.push(line)
        })
      })
    }
  }
  return output
}

function isMarkerInsidePolygon (marker, poly) {
  var x = marker.getLatLng().lat
  var y = marker.getLatLng().lng

  // Algorithm comes from:
  // https://github.com/substack/point-in-polygon/blob/master/index.js
  var inside = false

  // FIXME: getLatLngs does not return holes. Maybe use toGetJson instead?
  getLines(poly.getLatLngs()).forEach(function (line) {
    var xi = line[0].lat
    var yi = line[0].lng
    var xj = line[1].lat
    var yj = line[1].lng

    //      *
    //     /
    // *--/----------->>
    //   *
    // Check that
    //
    // 1.  yi and yj are on opposite sites of a ray to the right
    // 2.  the intersection of the ray and the segment is right of x
    var intersect = ((yi > y) !== (yj > y)) &&
        (x < (xj - xi) * (y - yi) / (yj - yi) + xi)
    if (intersect) inside = !inside
  })
  return inside
}

var init = function () {
  var $ = window.jQuery
  var L = window.L

  $('[data-map="choose_point"]').each(function (i, e) {
    var name = e.getAttribute('data-name')
    var polygon = JSON.parse(e.getAttribute('data-polygon'))
    var point = JSON.parse(e.getAttribute('data-point'))
    var baseurl = e.getAttribute('data-baseurl')
    var attribution = e.getAttribute('data-attribution')

    var map = createMap(L, baseurl, attribution, e)

    var polygonStyle = {
      'color': '#0076ae',
      'weight': 2,
      'opacity': 1,
      'fillOpacity': 0.2
    }

    var basePolygon = L.geoJson(polygon, {style: polygonStyle}).addTo(map)
    map.fitBounds(basePolygon.getBounds())
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
}

window.jQuery(init)
window.jQuery(document).on('a4.embed.ready', init)
