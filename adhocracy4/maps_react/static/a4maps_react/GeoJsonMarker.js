import L from 'leaflet'
import {
  createElementObject,
  createLayerComponent, extendContext
} from '@react-leaflet/core'
import django from 'django'

export const makeIcon = (iconUrl) =>
  L.icon({
    iconUrl: iconUrl || '/static/images/map_pin_default.svg',
    shadowUrl: '/static/images/map_shadow_01.svg',
    iconSize: [30, 36],
    iconAnchor: [15, 36],
    shadowSize: [40, 54],
    shadowAnchor: [20, 54],
    popupAnchor: [0, -10]
  })

/**
 * Creates a Leaflet marker from a GeoJSON. This is needed to
 * be able to add any Tooltip or Popup to the Markers using JSX.
 */
const createGeoJsonMarker = ({ feature, ...props }, context) => {
  const coords = [...feature.geometry.coordinates].reverse()
  const propsWithIcon = { icon: makeIcon(feature.properties.category_icon), ...props }
  const instance = L.marker(coords, propsWithIcon)

  const a11yTag = django.gettext('Project pin')
  const originalOnAdd = instance.onAdd
  instance.onAdd = function (map) {
    originalOnAdd.call(this, map)
    const element = this.getElement()
    if (element) {
      // eslint-disable-next-line no-restricted-syntax
      element.setAttribute('aria-label', `${a11yTag}: ${feature.properties.title}`)
      element.setAttribute('role', 'button')
    }
    return this
  }

  return createElementObject(instance, extendContext(context, { overlayContainer: instance }))
}

const updateGeoJsonMarker = (instance, { feature, ...props }, prevProps) => {
  const coords = [...feature.geometry.coordinates].reverse()
  if (props.icon !== prevProps.icon) {
    instance.setIcon(props.icon)
  }
  instance.setLatLng(coords)
}

const GeoJsonMarker = createLayerComponent(createGeoJsonMarker, updateGeoJsonMarker)
export default GeoJsonMarker
