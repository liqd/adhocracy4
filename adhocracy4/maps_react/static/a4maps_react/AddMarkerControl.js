import L from 'leaflet'
import { createControlComponent } from '@react-leaflet/core'
import { point, booleanPointInPolygon } from '@turf/turf'
import { makeIcon } from './GeoJsonMarker'

export function checkPointInsidePolygon (marker, polygons) {
  const pointGeoJSON = point([marker.lng, marker.lat])
  let isInPolygon = false

  polygons.eachLayer((layer) => {
    const polygonGeoJSON = layer.toGeoJSON()
    if (booleanPointInPolygon(pointGeoJSON, polygonGeoJSON)) {
      isInPolygon = true
    }
  })

  return isInPolygon
}

const markerProps = { icon: makeIcon(), draggable: true }

export class AddMarkerControlClass extends L.Control {
  constructor ({ input, point, markerConstraints, onDragEnd }) {
    super()
    this.marker = null
    this.oldCoords = null
    this.map = null
    this.input = input
    this.markerConstraints = null
    this.onDragEndHandler = onDragEnd

    if (markerConstraints) {
      this.markerConstraints = L.geoJSON(markerConstraints)
    }

    if (point) {
      const pointObj = JSON.parse(point)
      const latlng = pointObj.geometry.coordinates.reverse()
      this.marker = L.marker(latlng, markerProps)
      this.oldCoords = latlng
    }
  }

  updateMarker (latlng) {
    const isInsideConstraints = checkPointInsidePolygon(latlng, this.markerConstraints)
    if (isInsideConstraints) {
      this.oldCoords = latlng
      if (this.marker) {
        this.marker.setLatLng(latlng)
      } else {
        this.marker = L.marker(latlng, markerProps).addTo(this.map)
        this.marker.on('dragend', this.onDragend.bind(this))
      }
      this.input.value = JSON.stringify(this.marker.toGeoJSON())
    }

    return isInsideConstraints
  }

  onDragend (e) {
    const targetPosition = e.target.getLatLng()
    const isInsideConstraints = checkPointInsidePolygon(targetPosition, this.markerConstraints)
    if (!isInsideConstraints) {
      e.target.setLatLng(this.oldCoords)
    } else {
      this.updateMarker(targetPosition)
    }
    this.onDragEndHandler?.(isInsideConstraints)
  }

  addTo (map) {
    this.map = map
    this.boundClickHandler = (e) => this.updateMarker(e.latlng)
    map.on('click', this.boundClickHandler)

    if (this.marker) {
      this.marker.addTo(this.map)
      this.marker.on('dragend', this.onDragend.bind(this))
    }
  }

  onRemove (map) {
    map.off('click', this.boundClickHandler)
    if (this.marker) {
      this.marker.off('dragend', this.onDragend)
      this.marker.remove()
      this.marker = null
    }
  }
}
const createControl = (props) => new AddMarkerControlClass(props)

const AddMarkerControl = createControlComponent(createControl)
export default AddMarkerControl
