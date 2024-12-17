import { createMap } from './a4maps_common'
import django from 'django'

function loadMarkerCluster () {
  require('leaflet.markercluster')
}

function init () {
  loadMarkerCluster()
  const L = window.L

  const escapeHtml = function (unsafe) {
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
    const hideSupport = e.getAttribute('data-hide-support')
    const hideVoteCount = e.getAttribute('data-hide-vote-count')
    let initial = 0

    const map = createMap(L, e, {
      baseUrl: e.getAttribute('data-baseurl'),
      useVectorMap: e.getAttribute('data-usevectormap'),
      attribution: e.getAttribute('data-attribution'),
      mapboxToken: e.getAttribute('data-mapbox-token'),
      omtToken: e.getAttribute('data-omt-token'),
      dragging: true,
      scrollWheelZoom: false,
      zoomControl: false,
      maxZoom: 18,
      tap: false
    })

    map.on('zoomend', function () {
      const currentZoom = map.getZoom()
      const minZoom = map.getMinZoom()

      if (currentZoom > minZoom) {
        if (initial === 1) {
          $('#zoom-out').removeClass('leaflet-disabled')
        }
      }
      if (currentZoom === minZoom) {
        $('#zoom-out').addClass('leaflet-disabled')
      }
    })

    const polygonStyle = {
      color: '#0076ae',
      weight: 2,
      opacity: 1,
      fillOpacity: 0.2
    }

    const basePolygon = L.geoJson(polygon, { style: polygonStyle }).addTo(map)
    basePolygon.on('dblclick', function (event) {
      map.zoomIn()
    })
    basePolygon.on('click', function (event) {
      map.closePopup()
    })

    map.fitBounds(basePolygon.getBounds())
    map.options.minZoom = map.getZoom()
    initial = 1

    const customOptions =
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
      return '<span class="map-popup-upvotes">' +
               feature.properties.positive_rating_count + ' <i class="fa fa-thumbs-up" aria-hidden="true"></i>' +
             '</span>' +
             '<span class="map-popup-downvotes">' +
               feature.properties.negative_rating_count + ' <i class="fa fa-thumbs-down" aria-hidden="true"></i>' +
             '</span>'
    }

    function getSupport (feature) {
      return '<span class="map-popup-upvotes">' +
               feature.properties.positive_rating_count + ' <i class="fa fa-thumbs-up" aria-hidden="true"></i>' +
               '<span class="visually-hidden">' +
                  django.ngettext(
                    'person supports this proposal.',
                    'persons support this proposal.',
                    feature.properties.positive_rating_count
                  ) +
               '</span>' +
             '</span>'
    }

    function getVoteCount (feature) {
      return '<span class="map-popup-vote-count">' +
               feature.properties.vote_count + ' <i class="fa-regular fa-square-check" aria-hidden="true"></i>' +
               '<span class="visually-hidden">' +
                  django.ngettext(
                    'person voted for this proposal.',
                    'persons voted for this proposal.',
                    feature.properties.vote_count
                  ) +
                '</span>' +
             '</span>'
    }

    function getCommentCount (feature) {
      return '<span class="map-popup-comments-count">' +
               feature.properties.comments_count + ' <i class="far fa-comment" aria-hidden="true"></i>' +
               '<span class="visually-hidden">' +
                  django.ngettext(
                    'person commented on this proposal.',
                    'persons commented on this proposal.',
                    feature.properties.comments_count
                  ) +
                '</span>' +
             '</span>'
    }

    function getPopUpContent (feature) {
      let popupContent = getImage(feature) +
                         '<div class="maps-popups-popup-text-content">' +
                         '<div class="maps-popups-popup-meta">'
      if (hideRatings === 'false' || hideRatings === null) {
        popupContent += getRatings(feature)
      } else if (hideSupport === 'false') {
        popupContent += getSupport(feature)
      }
      if (hideVoteCount === 'false' || hideVoteCount === null) {
        popupContent += getVoteCount(feature)
      }
      popupContent += getCommentCount(feature) +
                      '</div>' +
                      '<div class="maps-popups-popup-name">' +
                          '<a href="' + feature.properties.url + '">' + escapeHtml(feature.properties.name) + '</a>' +
                      '</div>' +
                      '</div>'
      return popupContent
    }

    const defaultIcon = L.icon({
      iconUrl: '/static/images/map_pin_default.svg',
      shadowUrl: '/static/images/map_shadow_01.svg',
      iconSize: [30, 36],
      iconAnchor: [15, 36],
      shadowSize: [40, 54],
      shadowAnchor: [20, 54],
      popupAnchor: [0, -10]
    })

    const cluster = L.markerClusterGroup({
      showCoverageOnHover: false
    })

    L.geoJson(points, {
      pointToLayer: function (feature, latlng) {
        let icon = defaultIcon
        if (feature.properties.category_icon) {
          icon = L.icon({
            iconUrl: feature.properties.category_icon,
            shadowUrl: '/static/images/map_shadow_01.svg',
            iconSize: [30, 36],
            iconAnchor: [15, 36],
            popupAnchor: [0, -10]
          })
        }

        const marker = L.marker(latlng, { icon })
        cluster.addLayer(marker)
        marker.bindPopup(getPopUpContent(feature), customOptions)
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
