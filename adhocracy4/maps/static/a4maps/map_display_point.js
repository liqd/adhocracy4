var init = function () {
  var $ = window.jQuery
  var L = window.L

  $('[data-map="display_point"]').each(function (i, e) {
    var polygon = JSON.parse(e.getAttribute('data-polygon'))
    var point = JSON.parse(e.getAttribute('data-point'))
    var pinSrc = JSON.parse(e.getAttribute('data-pin-src'))
    var baseurl = e.getAttribute('data-baseurl')
    var usevectormap = e.getAttribute('data-usevectormap')
    var token = e.getAttribute('data-token')
    var attribution = e.getAttribute('data-attribution')

    var map = new L.Map(e, {scrollWheelZoom: false, zoomControl: false})

    if (usevectormap === '1') {
      var newToken = (this.props.token === '') ? 'no-token' : token
      L.mapboxGL.accessToken = newToken
      L.mapboxGL({
        accessToken: L.mapboxGL.accessToken,
        style: baseurl
      }).addTo(map)
    } else {
      var basemap = baseurl + '{z}/{x}/{y}.png?access_token={accessToken}'
      var baselayer = L.tileLayer(basemap, { attribution: attribution, accessToken: token })
      baselayer.addTo(map)
    }

    var polygonStyle = {
      'color': '#0076ae',
      'weight': 2,
      'opacity': 1,
      'fillOpacity': 0.2
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

    var basePolygon = L.geoJson(polygon, {style: polygonStyle}).addTo(map)
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

        var marker = L.marker(latlng, {icon: icon}).addTo(map)
        return marker
      }
    })
  })
}

window.jQuery(init)
window.jQuery(document).on('a4.embed.ready', init)
