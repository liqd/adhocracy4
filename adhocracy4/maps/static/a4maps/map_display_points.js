window.jQuery(document).ready(function () {
  var $ = window.jQuery
  var L = window.L
  var polygon = window.polygon
  var point = window.point
  var baseurl = window.baseurl
  var initial = 0

  var basemap = baseurl + '{z}/{x}/{y}.png'
  var osmAttrib = '&copy; <a href="http://openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  var baselayer = L.tileLayer(basemap, { attribution: osmAttrib })
  var map = new L.Map('map', { scrollWheelZoom: false, zoomControl: false })
  baselayer.addTo(map)

  map.on('zoomend', function () {
    var currentZoom = map.getZoom()
    var minZoom = map.getMinZoom()

    if (currentZoom > minZoom) {
      if (initial === 1) {
        $('#zoom-out').removeClass('leaflet-disabled')
      }
    }
    if (currentZoom === minZoom) {
      $('#zoom-out').addClass('leaflet-disabled')
    }
  })

  var polygonStyle = {
    'color': '#0076ae',
    'weight': 2,
    'opacity': 1,
    'fillOpacity': 0.2
  }

  var basePolygon = L.geoJson(polygon, {style: polygonStyle}).addTo(map)
  basePolygon.on('dblclick', function (event) {
    map.zoomIn()
  })
  basePolygon.on('click', function (event) {
    map.closePopup()
  })

  map.fitBounds(basePolygon)
  map.options.minZoom = map.getZoom()
  initial = 1

  var customOptions =
    {
      'className': 'maps-popups',
      closeButton: false
    }

  function getImage (feature) {
    if (feature.properties.image) {
      return '<div class="maps-popups-popup-image" style="background-image:url(' + feature.properties.image + ');"></div>'
    }
    return '<div class="maps-popups-popup-image"></div>'
  }

  var icon = L.icon({
    iconUrl: '/static/images/map_pin_01_2x.png',
    shadowUrl: '/static/images/map_shadow_01_2x.png',
    iconSize: [30, 45],
    iconAnchor: [15, 45],
    shadowSize: [40, 54],
    shadowAnchor: [20, 54],
    popupAnchor: [0, 5]
  })

  L.geoJson(point, {
    pointToLayer: function (feature, latlng) {
      var marker = L.marker(latlng, {icon: icon}).addTo(map)
      var popupContent = getImage(feature) +
                        '<div class="maps-popups-popup-meta">' +
                            '<span class="idea-upvotes idea-meta-item">' +
                            feature.properties.positive_rating_count + ' <i class="fa fa-chevron-up" aria-hidden="true"></i>' +
                            '</span>' +
                            '<span class="idea-downvotes idea-meta-item">' +
                            feature.properties.negative_rating_count + ' <i class="fa fa-chevron-down" aria-hidden="true"></i>' +
                            '</span>' +
                            '<span class="idea-comments-count idea-meta-item">' +
                            feature.properties.comments_count + ' <i class="fa fa-comment-o" aria-hidden="true"></i>' +
                            '</span>' +
                            '</div>' +
                        '<div class="maps-popups-popup-name"><a href="' + feature.properties.url + '">' + feature.properties.name + '</a></div>'
      marker.bindPopup(popupContent, customOptions)
      return marker
    }
  })

  $('#zoom-in').click(function () {
    map.setZoom(map.getZoom() + 1)
    return false
  })

  $('#zoom-out').click(function () {
    map.setZoom(map.getZoom() - 1)
    return false
  })
})
