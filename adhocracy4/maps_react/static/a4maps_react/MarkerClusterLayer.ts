import L from 'leaflet'
import 'leaflet.markercluster'
import {
  createElementObject,
  createLayerComponent, extendContext, updateGridLayer
} from '@react-leaflet/core'

const createMarkerClusterLayer = (props: any, context: any): any => {
  const instance = (L as any).markerClusterGroup({ showCoverageOnHover: false })

  return createElementObject(instance, extendContext(context, { layerContainer: instance }))
}

const updateMarkerClusterLayer = (instance: any, props: any, prevProps: any): void => {
  updateGridLayer(instance, props, prevProps)
}

const MarkerClusterLayer = createLayerComponent(createMarkerClusterLayer, updateMarkerClusterLayer)
export default MarkerClusterLayer
