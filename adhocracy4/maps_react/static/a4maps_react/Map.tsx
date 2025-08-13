import React, { useImperativeHandle, ForwardedRef } from 'react'
import { MapContainer, GeoJSON, useMap, MapContainerProps } from 'react-leaflet'
import MaplibreGlLayer from './MaplibreGlLayer'

interface PolygonStyle {
  color: string;
  weight: number;
  opacity: number;
  fillOpacity: number;
}

interface MapProps extends MapContainerProps {
  attribution?: string;
  baseUrl?: string;
  polygon?: GeoJSON.GeoJsonObject;
  omtToken?: string;
  children?: React.ReactNode;
}

const polygonStyle: PolygonStyle = {
  color: '#0076ae',
  weight: 2,
  opacity: 1,
  fillOpacity: 0.2
}

const Map = React.forwardRef(function Map (
  { attribution, baseUrl, polygon, omtToken, children, ...rest }: MapProps,
  ref: ForwardedRef<L.Map>
) {
  const MapLayers = () => {
    const map = useMap()

    useImperativeHandle(ref, () => map as L.Map)

    const refCallback = (layer: L.Layer | null) => {
      if (!map || !layer) {
        return
      }
      const geoJSONLayer = layer as L.GeoJSON
      map.fitBounds(geoJSONLayer.getBounds())
      map.setMinZoom(map.getZoom())
    }

    return (
      <>
        {map && polygon && (
          <GeoJSON
            style={polygonStyle}
            data={polygon}
            ref={refCallback}
          />
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
    <MapContainer
      style={{ minHeight: 300 }}
      zoom={13}
      maxZoom={18}
      {...rest}
    >
      <MapLayers />
      {children}
    </MapContainer>
  )
})

export default Map
