import React from 'react'
import { act, fireEvent, render, screen } from '@testing-library/react'
import { useMap } from 'react-leaflet'

import { ShowMyLocationControl } from '../ShowMyLocationControl'

jest.mock('react-leaflet', () => {
  const React = require('react')

  return {
    useMap: jest.fn(() => ({ flyTo: jest.fn() })),
    Marker: React.forwardRef(function MockMarker ({ position }, ref) {
      const nodeRef = React.useRef(null)

      React.useImperativeHandle(ref, () => ({
        getElement: () => nodeRef.current
      }))

      return (
        <div
          ref={nodeRef}
          data-testid="show-my-location-marker"
          data-position={position.lat + ',' + position.lng}
        />
      )
    })
  }
})

jest.mock('../ControlWrapper', () => ({
  __esModule: true,
  default: ({ children }) => <div data-testid="control-wrapper">{children}</div>
}))

const originalGeolocation = navigator.geolocation

const setGeolocation = (value) => {
  Object.defineProperty(navigator, 'geolocation', {
    configurable: true,
    value
  })
}

describe('ShowMyLocationControl', () => {
  let mockMap
  let successCallback
  let errorCallback

  beforeEach(() => {
    mockMap = { flyTo: jest.fn() }
    useMap.mockReturnValue(mockMap)

    successCallback = null
    errorCallback = null

    setGeolocation({
      getCurrentPosition: jest.fn((success, error) => {
        successCallback = success
        errorCallback = error
      })
    })
  })

  afterEach(() => {
    setGeolocation(originalGeolocation)
    delete window.isSecureContext
    jest.clearAllMocks()
  })

  const clickButton = () => {
    fireEvent.click(screen.getByRole('button', { name: 'Show my location' }))
  }

  test('renders a button and does not request the location on mount', () => {
    render(<ShowMyLocationControl />)

    expect(screen.getByRole('button', { name: 'Show my location' })).toBeInTheDocument()
    expect(navigator.geolocation.getCurrentPosition).not.toHaveBeenCalled()
  })

  test('shows a loading state and centres the map on success', () => {
    render(<ShowMyLocationControl />)
    clickButton()

    expect(navigator.geolocation.getCurrentPosition).toHaveBeenCalledTimes(1)
    expect(screen.getByRole('button', { name: 'Locating...' })).toBeDisabled()
    expect(screen.getByRole('status')).toHaveTextContent('Locating...')

    act(() => {
      successCallback({ coords: { latitude: 52.52, longitude: 13.405 } })
    })

    expect(mockMap.flyTo).toHaveBeenCalledWith(
      expect.objectContaining({ lat: 52.52, lng: 13.405 }),
      14
    )
    expect(screen.getByRole('status')).toHaveTextContent('Location found.')

    const marker = screen.getByTestId('show-my-location-marker')
    expect(marker).toHaveAttribute('role', 'img')
    expect(marker).toHaveAttribute('aria-label', 'Your location')
  })

  test('informs about denied permission without moving the map', () => {
    render(<ShowMyLocationControl />)
    clickButton()

    act(() => {
      errorCallback({ code: 1 })
    })

    expect(screen.getByRole('status')).toHaveTextContent(
      'Location access was denied. Please enable location services in your browser settings and try again.'
    )
    expect(screen.queryByTestId('show-my-location-marker')).toBeNull()
    expect(mockMap.flyTo).not.toHaveBeenCalled()
  })

  test('informs about a timeout without moving the map', () => {
    render(<ShowMyLocationControl />)
    clickButton()

    act(() => {
      errorCallback({ code: 3 })
    })

    expect(screen.getByRole('status')).toHaveTextContent(
      'Locating your position took too long. Please try again.'
    )
    expect(screen.queryByTestId('show-my-location-marker')).toBeNull()
    expect(mockMap.flyTo).not.toHaveBeenCalled()
  })

  test('informs when geolocation is not supported', () => {
    setGeolocation(undefined)
    render(<ShowMyLocationControl />)
    clickButton()

    expect(screen.getByRole('status')).toHaveTextContent(
      'Geolocation is not supported by your browser.'
    )
    expect(screen.queryByTestId('show-my-location-marker')).toBeNull()
  })

  test('informs when the page is not served over a secure connection', () => {
    Object.defineProperty(window, 'isSecureContext', {
      configurable: true,
      value: false
    })
    render(<ShowMyLocationControl />)
    clickButton()

    expect(screen.getByRole('status')).toHaveTextContent(
      'Location is only available over a secure HTTPS connection. Please open this page via HTTPS or localhost.'
    )
    expect(navigator.geolocation.getCurrentPosition).not.toHaveBeenCalled()
    expect(screen.queryByTestId('show-my-location-marker')).toBeNull()
  })

  test('does not move the map when the position is outside the area', () => {
    render(
      <ShowMyLocationControl areaBounds={[[51.2, 11.0], [53.7, 15.0]]} />
    )
    clickButton()

    act(() => {
      successCallback({ coords: { latitude: 48.13, longitude: 11.58 } })
    })

    expect(screen.getByRole('status')).toHaveTextContent(
      'Your location is outside the map area. The map was not moved.'
    )
    expect(screen.queryByTestId('show-my-location-marker')).toBeNull()
    expect(mockMap.flyTo).not.toHaveBeenCalled()
  })

  test('accepts every position when no area bounds are given', () => {
    render(<ShowMyLocationControl />)
    clickButton()

    act(() => {
      successCallback({ coords: { latitude: 48.13, longitude: 11.58 } })
    })

    expect(mockMap.flyTo).toHaveBeenCalledWith(
      expect.objectContaining({ lat: 48.13, lng: 11.58 }),
      14
    )
    expect(screen.getByTestId('show-my-location-marker')).toBeInTheDocument()
  })
})
