function createMap (L, baseurl, usevectormap, attribution, e) {
  var map = new L.Map(e, {scrollWheelZoom: false, zoomControl: true, minZoom: 2})

  if (usevectormap === '1') {
    L.mapboxGL({
      accessToken: 'no-token',
      style: baseurl
    }).addTo(map)
  } else {
    var basemap = baseurl + '{z}/{x}/{y}.png'
    var baselayer = L.tileLayer(basemap, { attribution: attribution })
    baselayer.addTo(map)
  }

  return map
}

function getBaseBounds (L, polygon, bbox) {
  if (polygon) {
    if (polygon.type === 'FeatureCollection' && polygon.features.length === 0) {
      return bbox
    }
    return L.geoJson(polygon).getBounds()
  } else {
    return bbox
  }
}

var init = function () {
  var $ = window.jQuery
  var L = window.L

  $('[data-map="choose_polygon"]').each(function (i, e) {
    var name = e.getAttribute('data-name')
    var polygon = JSON.parse(e.getAttribute('data-polygon'))
    var bbox = JSON.parse(e.getAttribute('data-bbox'))
    var baseurl = e.getAttribute('data-baseurl')
    var usevectormap = e.getAttribute('data-usevectormap')
    var attribution = e.getAttribute('data-attribution')

    var map = createMap(L, baseurl, usevectormap, attribution, e)

    var polygonStyle = {
      'color': '#0076ae',
      'weight': 2,
      'opacity': 1,
      'fillOpacity': 0.2
    }

    var drawnItems
    if (polygon) {
      drawnItems = L.geoJson(polygon, {
        style: polygonStyle
      })
      if (drawnItems.getLayers().length > 0) {
        map.fitBounds(drawnItems.getBounds())
      } else {
        map.fitBounds(getBaseBounds(L, polygon, bbox))
      }
    } else {
      drawnItems = L.featureGroup()
      map.fitBounds(getBaseBounds(L, polygon, bbox))
    }
    drawnItems.addTo(map)

    map.addControl(new L.Control.Draw({
      edit: {
        featureGroup: drawnItems,
        edit: {
          selectedPathOptions: {
            maintainColor: true
          }
        }
      },
      draw: {
        polygon: {
          shapeOptions: polygonStyle
        },
        rectangle: {
          shapeOptions: polygonStyle
        },
        marker: false,
        circlemarker: false,
        polyline: false,
        circle: false
      }
    }))

    map.on(L.Draw.Event.CREATED, function (event) {
      var layer = event.layer
      drawnItems.addLayer(layer)
      var shape = drawnItems.toGeoJSON()
      $('#id_' + name).val(JSON.stringify(shape))
      $('#id_' + name).trigger('change')
    })

    map.on(L.Draw.Event.EDITED, function (event) {
      var shape = drawnItems.toGeoJSON()
      $('#id_' + name).val(JSON.stringify(shape))
      $('#id_' + name).trigger('change')
    })

    map.on(L.Draw.Event.DELETED, function (event) {
      var shape = drawnItems.toGeoJSON()
      $('#id_' + name).val(JSON.stringify(shape))
      $('#id_' + name).trigger('change')
    })

    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
      map.invalidateSize().fitBounds(getBaseBounds(L, polygon, bbox))
    })
  })
}

window.jQuery(init)
window.jQuery(document).on('a4.embed.ready', init)
