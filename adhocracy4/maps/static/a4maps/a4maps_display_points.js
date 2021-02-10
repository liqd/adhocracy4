import { createMap } from './a4maps_common'
import 'leaflet.markercluster'

function init () {
  var L = window.L

  var escapeHtml = function (unsafe) {
    // jQuery.text() escapes special chars as is documented at http://api.jquery.com/text/#text-function
    // Alternatively a custom unsafe.replace(/&/g, '&amp;')... solution as described
    // at https://stackoverflow.com/a/6234804 may be used. for example underscore.js uses a regexp based unescape.
    // FIXME: this method should be moved to a global scope or made importable if used more then once
    return $('<div>').text(unsafe).html()
  }

  $('[data-map="display_points"]').each(function (i, e) {
    const polygon = JSON.parse(e.getAttribute('data-polygon'))
    const points = JSON.parse(e.getAttribute('data-points'))
    const hideRatings = e.getAttribute('data-hide-ratings')
    var initial = 0

    const map = createMap(L, e, {
      baseUrl: e.getAttribute('data-baseurl'),
      useVectorMap: e.getAttribute('data-usevectormap'),
      attribution: e.getAttribute('data-attribution'),
      mapboxToken: e.getAttribute('data-mapbox-token'),
      omtToken: e.getAttribute('data-omt-token'),
      dragging: true,
      scrollWheelZoom: false,
      zoomControl: false,
      maxZoom: 18
    })

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
      color: '#0076ae',
      weight: 2,
      opacity: 1,
      fillOpacity: 0.2
    }

    var basePolygon = L.geoJson(polygon, { style: polygonStyle }).addTo(map)
    basePolygon.on('dblclick', function (event) {
      map.zoomIn()
    })
    basePolygon.on('click', function (event) {
      map.closePopup()
    })

    map.fitBounds(basePolygon.getBounds())
    map.options.minZoom = map.getZoom()
    initial = 1

    var customOptions =
      {
        className: 'maps-popups',
        closeButton: false
      }

    function getImage (feature) {
      if (feature.properties.image) {
        return '<div class="maps-popups-popup-image" style="background-image:url(' + feature.properties.image + ');"></div>'
      }
      return '<div class="maps-popups-popup-image maps-popups-popup-no-image"></div>'
    }

    function getRatings (feature) {
      if (hideRatings === 'false' || hideRatings === null) {
        return '<div class="maps-popups-popup-meta">' +
            '<span class="map-popup-upvotes">' +
            feature.properties.positive_rating_count + ' <i class="fa fa-chevron-up" aria-hidden="true"></i>' +
            '</span>' +
            '<span class="map-popup-downvotes">' +
            feature.properties.negative_rating_count + ' <i class="fa fa-chevron-down" aria-hidden="true"></i>' +
            '</span>' +
            '<span class="map-popup-comments-count">' +
            feature.properties.comments_count + ' <i class="far fa-comment" aria-hidden="true"></i>' +
            '</span>' +
        '</div>'
      } else if (hideRatings === 'true') {
        return '<div class="maps-popups-popup-meta">' +
            '<span class="map-popup-comments-count">' +
            feature.properties.comments_count + ' <i class="far fa-comment" aria-hidden="true"></i>' +
            '</span>' +
        '</div>'
      }
    }

    var defaultIcon = L.icon({
      iconUrl: '/static/images/map_pin_default.svg',
      shadowUrl: '/static/images/map_shadow_01.svg',
      iconSize: [30, 36],
      iconAnchor: [15, 36],
      shadowSize: [40, 54],
      shadowAnchor: [20, 54],
      popupAnchor: [0, -10]
    })

    var cluster = L.markerClusterGroup({
      showCoverageOnHover: false
    })

    L.geoJson(points, {
      pointToLayer: function (feature, latlng) {
        var icon = defaultIcon
        if (feature.properties.category_icon) {
          icon = L.icon({
            iconUrl: feature.properties.category_icon,
            shadowUrl: '/static/images/map_shadow_01.svg',
            iconSize: [30, 36],
            iconAnchor: [15, 36],
            popupAnchor: [0, -10]
          })
        }

        var marker = L.marker(latlng, { icon: icon })
        cluster.addLayer(marker)
        var popupContent = getImage(feature) +
                          '<div class="maps-popups-popup-text-content">' +
                          getRatings(feature) +
                            '<div class="maps-popups-popup-name">' +
                                '<a href="' + feature.properties.url + '">' + escapeHtml(feature.properties.name) + '</a>' +
                            '</div>' +
                          '</div>'
        marker.bindPopup(popupContent, customOptions)
        return marker
      }
    })

    map.addLayer(cluster)

    $('#zoom-in').click(function () {
      map.setZoom(map.getZoom() + 1)
      return false
    })

    $('#zoom-out').click(function () {
      map.setZoom(map.getZoom() - 1)
      return false
    })
  })
}

document.addEventListener('DOMContentLoaded', init, false)
document.addEventListener('a4.embed.ready', init, false)
