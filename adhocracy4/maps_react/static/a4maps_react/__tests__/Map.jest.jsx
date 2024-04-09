import React from 'react'
import { render, screen } from '@testing-library/react'
import Map from '../Map'

export const polygonData = {
  type: 'Feature',
  properties: {},
  geometry: {
    type: 'Polygon',
    coordinates: [
      [
        [0, 0],
        [10, 0],
        [10, 10],
        [0, 10]
      ]
    ]
  }
}

jest.mock('react-leaflet', () => {
  const ActualReactLeaflet = jest.requireActual('react-leaflet')
  const React = require('react')

  const MapContainer = React.forwardRef((props, ref) => (
    <div data-testid="map">
      <ActualReactLeaflet.MapContainer ref={ref} {...props} />
    </div>
  ))
  MapContainer.displayName = 'MapContainer'

  const GeoJSON = React.forwardRef((props, ref) => (
    <div data-testid="geojson" />
  ))
  GeoJSON.displayName = 'GeoJSON'

  return {
    __esModule: true,
    ...ActualReactLeaflet,
    GeoJSON,
    MapContainer
  }
})

describe('Map component tests', () => {
  test('component renders', () => {
    render(<Map />)
    const mapNode = screen.getByTestId('map')

    expect(mapNode).toBeTruthy()
  })

  // FIXME: test is broken as before this commit the polygon callback would
  // return because map is null, since this commit the map works as intended but
  // polygon.getBounds() returns null and hence map.fitBounds() fails.
  test('renders map with GeoJSON when polygon prop is provided', () => {
    render(<Map polygon={polygonData} />)
    const geoJsonNode = screen.getByTestId('geojson')

    expect(geoJsonNode).toBeTruthy()
  })

  test('does not render GeoJSON when polygon prop is not provided', () => {
    render(<Map />)
    const geoJsonNode = screen.queryByTestId('geojson')

    expect(geoJsonNode).toBeFalsy()
  })
})
