import L from 'leaflet'
import 'leaflet.markercluster'
import {
  createElementObject,
  createLayerComponent, extendContext, updateGridLayer
} from '@react-leaflet/core'

const createMarkerClusterLayer = (props, context) => {
  const instance = L.markerClusterGroup({ showCoverageOnHover: false })

  return createElementObject(instance, extendContext(context, { layerContainer: instance }))
}

const updateMarkerClusterLayer = (instance, props, prevProps) => {
  updateGridLayer(instance, props, prevProps)
}

const MarkerClusterLayer = createLayerComponent(createMarkerClusterLayer, updateMarkerClusterLayer)
export default MarkerClusterLayer
