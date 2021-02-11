import 'leaflet'
import 'mapbox-gl-leaflet'

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
    dragging: dragging,
    scrollWheelZoom: scrollWheelZoom,
    zoomControl: zoomControl,
    minZoom: minZoom,
    maxZoom: maxZoom
  })

  if (useVectorMap === '1') {
    if (mapboxToken !== '') {
      L.mapboxGL({
        accessToken: mapboxToken,
        style: baseUrl
      }).addTo(map)
    } else {
      if (omtToken !== '') {
        L.mapboxGL({
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
        L.mapboxGL({
          style: baseUrl
        }).addTo(map)
      }
    }
    const attributionLayer = L.tileLayer('', { attribution: attribution })
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
    const baselayer = L.tileLayer(basemap, { attribution: attribution, accessToken: accessToken })
    baselayer.addTo(map)
  }

  return map
}
