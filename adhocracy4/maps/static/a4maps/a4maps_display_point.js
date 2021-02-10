import { createMap } from './a4maps_common'

function init () {
  var L = window.L

  $('[data-map="display_point"]').each(function (i, e) {
    const polygon = JSON.parse(e.getAttribute('data-polygon'))
    const point = JSON.parse(e.getAttribute('data-point'))
    const pinSrc = JSON.parse(e.getAttribute('data-pin-src'))

    const map = createMap(L, e, {
      baseUrl: e.getAttribute('data-baseurl'),
      useVectorMap: e.getAttribute('data-usevectormap'),
      attribution: e.getAttribute('data-attribution'),
      mapboxToken: e.getAttribute('data-mapbox-token'),
      omtToken: e.getAttribute('data-omt-token'),
      dragging: true,
      scrollWheelZoom: false,
      zoomControl: false
    })

    const polygonStyle = {
      color: '#0076ae',
      weight: 2,
      opacity: 1,
      fillOpacity: 0.2
    }

    var defaultIcon = L.icon({
      iconUrl: '/static/images/map_pin_default.svg',
      shadowUrl: '/static/images/map_shadow_01.svg',
      iconSize: [30, 36],
      iconAnchor: [15, 36],
      shadowSize: [40, 54],
      shadowAnchor: [20, 54],
      popupAnchor: [0, -45]
    })

    var basePolygon = L.geoJson(polygon, { style: polygonStyle }).addTo(map)
    map.fitBounds(basePolygon.getBounds())
    map.options.minZoom = map.getZoom()
    L.control.zoom({
      position: 'topleft'
    }).addTo(map)

    L.geoJson(point, {
      pointToLayer: function (feature, latlng) {
        var icon = defaultIcon
        if (pinSrc) {
          icon = L.icon({
            iconUrl: pinSrc,
            shadowUrl: '/static/images/map_shadow_01.svg',
            iconSize: [30, 36],
            iconAnchor: [15, 36],
            popupAnchor: [0, 5]
          })
        }

        var marker = L.marker(latlng, { icon: icon }).addTo(map)
        return marker
      }
    })
  })
}

document.addEventListener('DOMContentLoaded', init, false)
document.addEventListener('a4.embed.ready', init, false)
