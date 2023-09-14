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
    let maplibreMap
    if (mapboxToken !== '') {
      maplibreMap = L.maplibreGL({
        accessToken: mapboxToken,
        style: baseUrl,
        transformRequest
      }).addTo(map)
    } else {
      if (omtToken !== '') {
        maplibreMap = L.maplibreGL({
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
    if (!attribution) {
      // for some reason getMaplibreMap returns null if executed immediately.
      // setTimeout is kinda hacky.
      setTimeout(() => {
        const mm = maplibreMap.getMaplibreMap()
        if (mm == null) {
          console.warn("a4: couldn't load maplibreMap to set attribution")
          return
        }
        const loadAttribution = () => {
          const sources = mm.getStyle().sources
          const keys = Object.keys(sources)
          const noAttribution = keys.every((key, index) => {
            if ('attribution' in sources[key]) {
              map.attributionControl.addAttribution(sources[key].attribution)
              return false
            }
            return true
          })
          if (noAttribution) {
            console.warn("couldn't find map attribution in style")
          }
        }
        if (mm.isStyleLoaded()) {
          loadAttribution()
        } else {
          mm.once('styledata', function () {
            loadAttribution()
          })
        }
      }, 100)
    }
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
    const baselayer = L.tileLayer(basemap, { accessToken })
    baselayer.addTo(map)
  }
  if (attribution) {
    map.attributionControl.addAttribution(attribution)
  }
  return map
}
