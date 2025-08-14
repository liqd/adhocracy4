import React, { useEffect, useRef, useImperativeHandle } from 'react'
import { useMap } from 'react-leaflet'
import L from 'leaflet'
import { point, booleanPointInPolygon } from '@turf/turf'
import { Feature, Point, Polygon, MultiPolygon, FeatureCollection } from 'geojson'
import { makeIcon } from './GeoJsonMarker'

interface LatLng {
  lat: number;
  lng: number;
}

type ValidPolygonGeoJSON =
  | Feature<Polygon | MultiPolygon>
  | FeatureCollection<Polygon | MultiPolygon>

interface AddMarkerControlProps {
  input: HTMLInputElement;
  point?: string;
  markerConstraints?: ValidPolygonGeoJSON;
  onDragEnd?: (isInsideConstraints: boolean) => void;
}

const markerProps: L.MarkerOptions = {
  icon: makeIcon(),
  draggable: true
}

const AddMarkerControl = React.forwardRef<L.Control, AddMarkerControlProps>((props, ref) => {
  const map = useMap()
  const controlRef = useRef<L.Control>(null)
  const markerRef = useRef<L.Marker | null>(null)
  const oldCoordsRef = useRef<L.LatLngExpression | null>(null)
  const markerConstraintsRef = useRef<L.GeoJSON | null>(null)
  const clickHandlerRef = useRef<(e: L.LeafletMouseEvent) => void>(null)

  // Initialize marker constraints
  useEffect(() => {
    if (props.markerConstraints) {
      markerConstraintsRef.current = L.geoJSON(props.markerConstraints)
    }
  }, [props.markerConstraints])

  // Initialize marker if point is provided
  useEffect(() => {
    if (props.point) {
      const pointObj: Feature<Point> = JSON.parse(props.point)
      const latlng = pointObj.geometry.coordinates.reverse() as [number, number]
      markerRef.current = L.marker(latlng, markerProps)
      oldCoordsRef.current = latlng
    }
  }, [props.point])

  function isFeatureWithPolygon (geoJson: any): geoJson is Feature<Polygon | MultiPolygon> {
    return geoJson?.geometry?.type === 'Polygon' || geoJson?.geometry?.type === 'MultiPolygon'
  }

  function checkPointInsidePolygon (marker: LatLng, polygons: L.GeoJSON): boolean {
    const pointGeoJSON = point([marker.lng, marker.lat])
    let isInside = false

    polygons.eachLayer((layer: L.Layer) => {
      if ('toGeoJSON' in layer) {
        const layerGeoJSON = (layer as L.GeoJSON).toGeoJSON()
        if (isFeatureWithPolygon(layerGeoJSON)) {
          if (booleanPointInPolygon(pointGeoJSON, layerGeoJSON)) {
            isInside = true
          }
        }
      }
    })

    return isInside
  }

  const updateMarker = (latlng: L.LatLngExpression): boolean => {
    if (!markerConstraintsRef.current || !map) return false

    const latLngObj = L.latLng(latlng)
    const isInsideConstraints = checkPointInsidePolygon(
      { lat: latLngObj.lat, lng: latLngObj.lng },
      markerConstraintsRef.current
    )

    if (isInsideConstraints) {
      oldCoordsRef.current = latlng
      if (markerRef.current) {
        markerRef.current.setLatLng(latlng)
      } else {
        markerRef.current = L.marker(latlng, markerProps).addTo(map)
        markerRef.current.on('dragend', onDragend)
      }
      props.input.value = JSON.stringify(markerRef.current.toGeoJSON())
    }

    return isInsideConstraints
  }

  const onDragend = (e: L.DragEndEvent) => {
    if (!markerConstraintsRef.current || !markerRef.current) return

    const targetPosition = e.target.getLatLng()
    const isInsideConstraints = checkPointInsidePolygon(
      { lat: targetPosition.lat, lng: targetPosition.lng },
      markerConstraintsRef.current
    )

    if (!isInsideConstraints) {
      e.target.setLatLng(oldCoordsRef.current!)
    } else {
      updateMarker(targetPosition)
    }

    props.onDragEnd?.(isInsideConstraints)
  }

  // Set up the control and event handlers
  useEffect(() => {
    if (!map) return

    const control = new L.Control()
    controlRef.current = control

    clickHandlerRef.current = (e: L.LeafletMouseEvent) => updateMarker(e.latlng)
    map.on('click', clickHandlerRef.current)

    if (markerRef.current) {
      markerRef.current.addTo(map)
      markerRef.current.on('dragend', onDragend)
    }

    return () => {
      if (map && clickHandlerRef.current) {
        map.off('click', clickHandlerRef.current)
      }
      if (markerRef.current) {
        markerRef.current.off('dragend', onDragend)
        markerRef.current.remove()
      }
    }
  }, [map])

  useImperativeHandle(ref, () => controlRef.current as L.Control)

  return null
})

AddMarkerControl.displayName = 'AddMarkerControl'

export default AddMarkerControl
