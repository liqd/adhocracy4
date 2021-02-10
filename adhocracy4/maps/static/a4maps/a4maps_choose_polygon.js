import { createMap } from './a4maps_common'
import 'leaflet-draw'

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

function init () {
  var L = window.L

  $('[data-map="choose_polygon"]').each(function (i, e) {
    const name = e.getAttribute('data-name')
    const polygon = JSON.parse(e.getAttribute('data-polygon'))
    const bbox = JSON.parse(e.getAttribute('data-bbox'))

    const map = createMap(L, e, {
      baseUrl: e.getAttribute('data-baseurl'),
      useVectorMap: e.getAttribute('data-usevectormap'),
      attribution: e.getAttribute('data-attribution'),
      mapboxToken: e.getAttribute('data-mapbox-token'),
      omtToken: e.getAttribute('data-omt-token'),
      dragging: true,
      scrollWheelZoom: false,
      zoomControl: true,
      minZoom: 2
    })

    const polygonStyle = {
      color: '#0076ae',
      weight: 2,
      opacity: 1,
      fillOpacity: 0.2
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

document.addEventListener('DOMContentLoaded', init, false)
document.addEventListener('a4.embed.ready', init, false)
