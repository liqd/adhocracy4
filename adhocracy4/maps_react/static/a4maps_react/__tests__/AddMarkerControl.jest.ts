import { AddMarkerControlClass } from '../AddMarkerControl'
import { polygonData as markerConstraints } from './Map.jest'
import { jest } from '@jest/globals'

describe('AddMarkerControlClass', () => {
  const map = { on: jest.fn(), off: jest.fn(), addLayer: jest.fn() }
  const point = JSON.stringify({
    type: 'Feature',
    properties: {},
    geometry: {
      type: 'Point',
      coordinates: [5, 5]
    }
  })

  it('sets a marker', () => {
    const input = document.createElement('input')
    const instance = new AddMarkerControlClass({ input, markerConstraints })
    instance.map = map

    const latlng = { lat: 10, lng: 5 }

    expect(instance.marker).toBe(null)
    instance.updateMarker(latlng)
    expect(instance.marker).toBeDefined()
    expect(input.value).toEqual(expect.stringContaining('5,10'))
    instance.updateMarker({ lat: 2, lng: 5 })
    expect(input.value).toEqual(expect.stringContaining('5,2'))
  })

  it('does not set a marker when outside', () => {
    const input = document.createElement('input')
    const instance = new AddMarkerControlClass({ input, markerConstraints })
    instance.map = map
    const latlng = { lat: 15, lng: 15 }
    expect(instance.marker).toBe(null)
    instance.updateMarker(latlng)
    expect(instance.marker).toBe(null)
    expect(input.value).toEqual('')
  })

  it('updates on drag', () => {
    const input = document.createElement('input')
    const instance = new AddMarkerControlClass({ input, point, markerConstraints })
    instance.map = map
    expect(instance.oldCoords).toStrictEqual([5, 5])
    const newCoords = { lat: 10, lng: 10 }

    const e = { target: { getLatLng: () => newCoords, setLatLng: jest.fn() } }
    instance.onDragend(e)
    expect(instance.oldCoords).toStrictEqual(newCoords)

    const e2 = { target: { getLatLng: () => ({ lat: 15, lng: 15 }), setLatLng: jest.fn() } }
    instance.onDragend(e2)
    expect(e2.target.setLatLng).toHaveBeenCalledWith(newCoords)
    expect(instance.oldCoords).toStrictEqual(newCoords)
  })
})
