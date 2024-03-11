import L from 'leaflet'
import '@maplibre/maplibre-gl-leaflet'
import {
  createElementObject,
  createTileLayerComponent, updateGridLayer
} from '@react-leaflet/core'

const createMaplibreGlLayer = (props, context) => {
  const instance = L.maplibreGL({
    attribution: props.attribution,
    style: props.baseUrl,
    transformRequest: function (url, resourceType) {
      if (resourceType === 'Tile' && url.indexOf('https://') === 0) {
        return {
          url: url + '?token=' + props.omtToken
        }
      }
    }
  })

  return createElementObject(instance, context)
}

const updateMaplibreGlLayer = (instance, props, prevProps) => {
  updateGridLayer(instance, props, prevProps)

  const { baseUrl, attribution } = props
  if (baseUrl != null && baseUrl !== prevProps.baseUrl) {
    instance.getMaplibreMap().setStyle(baseUrl)
  }

  if (attribution != null && attribution !== prevProps.attribution) {
    instance.options.attribution = attribution
  }
}

const MaplibreGlLayer = createTileLayerComponent(createMaplibreGlLayer, updateMaplibreGlLayer)
export default MaplibreGlLayer
