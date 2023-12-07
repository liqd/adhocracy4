import React, { useRef, useImperativeHandle } from 'react'
import { MapContainer, GeoJSON } from 'react-leaflet'
import MaplibreGlLayer from './MaplibreGlLayer'
import ZoomControl from './ZoomControl'

const polygonStyle = {
  color: '#0076ae',
  weight: 2,
  opacity: 1,
  fillOpacity: 0.2
}

export const Map = React.forwardRef(function Map (
  { attribution, baseUrl, polygon, omtToken, children, ...rest }, ref
) {
  const map = useRef()
  // forwarding our map ref
  useImperativeHandle(ref, () => map.current)
  const refCallback = (polygon) => {
    if (!map.current || !polygon) {
      return
    }
    map.current.fitBounds(polygon.getBounds())
    map.current.options.minZoom = map.current.getZoom()
    map.current.constraints = polygon
  }

  return (
    <MapContainer
      style={{ minHeight: 300 }}
      zoom={13}
      maxZoom={18}
      zoomControl={false}
      {...rest}
      ref={map}
    >
      {polygon && <GeoJSON style={polygonStyle} data={polygon} ref={refCallback} />}
      <MaplibreGlLayer attribution={attribution} baseUrl={baseUrl} omtToken={omtToken} />
      <ZoomControl position="topleft" />
      {children}
    </MapContainer>
  )
})
