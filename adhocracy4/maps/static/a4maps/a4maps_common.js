import 'leaflet'
import '@maplibre/maplibre-gl-leaflet'
import { isMapboxURL, transformMapboxUrl } from 'maplibregl-mapbox-request-transformer'

export function createMap (L, e, {
  dragging = undefined,
  scrollWheelZoom = undefined,
  zoomControl = undefined,
  minZoom = undefined,
  maxZoom = undefined,
  baseUrl = '',
  useVectorMap = '0',
  attribution = '',
  mapboxToken = '',
  omtToken = ''
} = {}) {
  const map = new L.Map(e, {
    dragging,
    scrollWheelZoom,
    zoomControl,
    minZoom,
    maxZoom,
    tap: false
  })

  // Transform urls with the mapbox:// scheme as maplibre-gl dropped support
  // for it in v2.
  const transformRequest = (url, resourceType) => {
    if (isMapboxURL(url)) {
      return transformMapboxUrl(url, resourceType, mapboxToken)
    }
    return { url }
  }

  if (useVectorMap === '1') {
    if (mapboxToken !== '') {
      L.maplibreGL({
        accessToken: mapboxToken,
        style: baseUrl,
        transformRequest
      }).addTo(map)
    } else {
      if (omtToken !== '') {
        L.maplibreGL({
          style: baseUrl,
          transformRequest: function (url, resourceType) {
            if (resourceType === 'Tile' && url.indexOf('https://') === 0) {
              return {
                url: url + '?token=' + omtToken
              }
            }
          }
        }).addTo(map)
      } else {
        L.maplibreGL({
          style: baseUrl
        }).addTo(map)
      }
    }
    const attributionLayer = L.tileLayer('', { attribution })
    attributionLayer.addTo(map)
  } else {
    let basemap = baseUrl + '{z}/{x}/{y}.png'
    let accessToken = ''
    if (mapboxToken !== '') {
      basemap = baseUrl + '{z}/{x}/{y}.png?access_token={accessToken}'
      accessToken = mapboxToken
    } else if (omtToken !== '') {
      basemap = baseUrl + '{z}/{x}/{y}.png?token={accessToken}'
      accessToken = omtToken
    }
    const baselayer = L.tileLayer(basemap, { attribution, accessToken })
    baselayer.addTo(map)
  }

  return map
}
