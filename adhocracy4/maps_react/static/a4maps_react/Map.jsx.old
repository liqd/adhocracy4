import React, { useImperativeHandle } from 'react'
import { MapContainer, GeoJSON, useMap } from 'react-leaflet'
import MaplibreGlLayer from './MaplibreGlLayer'

const polygonStyle = {
  color: '#0076ae',
  weight: 2,
  opacity: 1,
  fillOpacity: 0.2
}

const Map = React.forwardRef(function Map (
  { attribution, baseUrl, polygon, omtToken, children, ...rest },
  ref
) {
  const MapLayers = () => {
    const map = useMap()
    // forwarding our map ref
    // FIXME: do we need the ref?
    useImperativeHandle(ref, () => map)
    const refCallback = (polygon) => {
      if (!map || !polygon) {
        return
      }
      map.fitBounds(polygon.getBounds())
      map.setMinZoom(map.getZoom())
    }
    return (
      <>
        {map && polygon && (
          <GeoJSON style={polygonStyle} data={polygon} ref={refCallback} />
        )}
        <MaplibreGlLayer
          attribution={attribution}
          baseUrl={baseUrl}
          omtToken={omtToken}
        />
      </>
    )
  }

  return (
    <MapContainer style={{ minHeight: 300 }} zoom={13} maxZoom={18} {...rest}>
      <MapLayers />
      {children}
    </MapContainer>
  )
})

export default Map
