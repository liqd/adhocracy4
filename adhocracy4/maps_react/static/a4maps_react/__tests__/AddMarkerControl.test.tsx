import React from 'react'
import { describe, it, expect, vi } from 'vitest'
import { render } from '@testing-library/react'
import { MapContainer } from 'react-leaflet'
import AddMarkerControl from '../AddMarkerControl'
import { mockGeoJSON, mockMarker } from '../../../../../tests/__mocks__/leaflet'

// Simple GeoJsonMarker mock
vi.mock('../GeoJsonMarker', () => ({
  makeIcon: vi.fn().mockReturnValue({})
}))

describe('AddMarkerControl', () => {
  const mockInput = document.createElement('input')
  const mockPolygon = {
    type: 'FeatureCollection',
    features: [{
      type: 'Feature',
      geometry: {
        type: 'Polygon',
        coordinates: [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]
      }
    }]
  }

  it('creates marker when point is provided', async () => {
    const mockPoint = JSON.stringify({
      type: 'Feature',
      geometry: {
        type: 'Point',
        coordinates: [10, 20]
      }
    })

    render(
      <MapContainer>
        <AddMarkerControl input={mockInput} point={mockPoint} />
      </MapContainer>
    )

    expect(mockMarker).toHaveBeenCalledWith(
      [20, 10],
      expect.objectContaining({ draggable: true })
    )
  })

  it('creates geoJSON when constraints are provided', () => {
    render(
      <MapContainer>
        <AddMarkerControl input={mockInput} markerConstraints={mockPolygon} />
      </MapContainer>
    )

    expect(mockGeoJSON).toHaveBeenCalledWith(mockPolygon)
  })
})
