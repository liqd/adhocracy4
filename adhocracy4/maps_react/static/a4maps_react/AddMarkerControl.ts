import L from 'leaflet'
import React from 'react'
import { createControlComponent } from '@react-leaflet/core'
import { point, booleanPointInPolygon } from '@turf/turf'
import { makeIcon } from './GeoJsonMarker'

interface PolygonLayer {
  eachLayer: (fn: (layer: any) => void) => void
}

export function checkPointInsidePolygon (marker: { lat: number; lng: number }, polygons: PolygonLayer | null) {
  const pointGeoJSON = point([marker.lng, marker.lat])
  let isInPolygon = false

  if (!polygons) {
    return isInPolygon
  }

  polygons.eachLayer((layer) => {
    const polygonGeoJSON = layer.toGeoJSON()
    if (booleanPointInPolygon(pointGeoJSON, polygonGeoJSON)) {
      isInPolygon = true
    }
  })

  return isInPolygon
}

const markerProps = { icon: makeIcon(), draggable: true }

interface AddMarkerControlOptions {
  input: HTMLInputElement
  point?: string
  markerConstraints?: any
  onDragEnd?: (isInside: boolean) => void
}

export class AddMarkerControlClass extends L.Control {
  marker: any
  oldCoords: any
  map: any
  input: HTMLInputElement
  markerConstraints: any
  onDragEndHandler?: (isInside: boolean) => void
  boundClickHandler: ((e: any) => void) | undefined

  constructor ({ input, point, markerConstraints, onDragEnd }: AddMarkerControlOptions) {
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

  updateMarker (latlng: { lat: number; lng: number }) {
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

  onDragend (e: any) {
    const targetPosition = e.target.getLatLng()
    const isInsideConstraints = checkPointInsidePolygon(targetPosition, this.markerConstraints)
    if (!isInsideConstraints) {
      e.target.setLatLng(this.oldCoords)
    } else {
      this.updateMarker(targetPosition)
    }
    this.onDragEndHandler?.(isInsideConstraints)
  }

  addTo (map: any): this {
    this.map = map
    this.boundClickHandler = (e) => this.updateMarker(e.latlng)
    map.on('click', this.boundClickHandler)

    if (this.marker) {
      this.marker.addTo(this.map)
      this.marker.on('dragend', this.onDragend.bind(this))
    }
    return this
  }

  onRemove (map: any): this {
    map.off('click', this.boundClickHandler)
    if (this.marker) {
      this.marker.off('dragend', this.onDragend)
      this.marker.remove()
      this.marker = null
    }
    return this
  }
}

const createControl = (props: any): L.Control => new AddMarkerControlClass(props)

const AddMarkerControl = createControlComponent(createControl as any) as React.ComponentType<any>
export default AddMarkerControl
