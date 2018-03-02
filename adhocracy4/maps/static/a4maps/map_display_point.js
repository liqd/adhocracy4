var init = function () {
  var $ = window.jQuery
  var L = window.L

  $('[data-map="display_point"]').each(function (i, e) {
    var polygon = JSON.parse(e.getAttribute('data-polygon'))
    var point = JSON.parse(e.getAttribute('data-point'))
    var categoryIcon = JSON.parse(e.getAttribute('data-category-icon'))
    var baseurl = e.getAttribute('data-baseurl')
    var attribution = e.getAttribute('data-attribution')

    var basemap = baseurl + '{z}/{x}/{y}.png'
    var baselayer = L.tileLayer(basemap, {attribution: attribution})
    var map = new L.Map(e, {scrollWheelZoom: false, zoomControl: false})
    baselayer.addTo(map)

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
        if (categoryIcon) {
          icon = L.icon({
            iconUrl: '/static/category_icons/pins/' + categoryIcon + '_pin.svg',
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
