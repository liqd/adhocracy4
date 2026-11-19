import React, { useEffect, useRef, useState } from 'react'
import django from 'django'
import L from 'leaflet'
import { Marker, useMap } from 'react-leaflet'
import ControlWrapper from './ControlWrapper'

// Firefox's network based geolocation can be slow. A long timeout and a
// low accuracy are enough for centring the map and avoid avoidable timeouts.
const GEOLOCATION_TIMEOUT = 30000
const GEOLOCATION_MAX_AGE = 300000
const LOCATION_ZOOM = 14

// GeolocationPositionError codes. The constants are not exposed consistently
// across browsers, so compare the numeric codes directly.
const PERMISSION_DENIED = 1
const TIMEOUT = 3

const translations = {
  showMyLocation: django.gettext('Show my location'),
  locating: django.gettext('Locating...'),
  locationFound: django.gettext('Location found.'),
  yourLocation: django.gettext('Your location'),
  unsupported: django.gettext('Geolocation is not supported by your browser.'),
  insecureContext: django.gettext('Location is only available over a secure HTTPS connection. Please open this page via HTTPS or localhost.'),
  permissionDenied: django.gettext('Location access was denied. Please enable location services in your browser settings and try again.'),
  unavailable: django.gettext('Could not determine your location. Please try again.'),
  timeout: django.gettext('Locating your position took too long. Please try again.'),
  outsideArea: django.gettext('Your location is outside the map area. The map was not moved.')
}

const defaultIcon = L.divIcon({
  className: 'a4-show-my-location__marker',
  html: '<span style="display:block;width:16px;height:16px;margin:1px;border:3px solid #fff;border-radius:50%;background:#0076ae;box-shadow:0 0 0 2px rgba(0,118,174,.35)"></span>',
  iconSize: [24, 24],
  iconAnchor: [12, 12]
})

/**
 * Map control that shows the current position of the user. The position is
 * only kept in the browser and is never sent to the server.
 *
 * @param {object} props
 * @param {Array<Array<number>>} [props.areaBounds] - [[south, west],
 *   [north, east]] of the area in which a position may move the map. Without
 *   bounds every position is accepted.
 * @param {object} [props.icon] - Leaflet icon used for the position marker.
 * @param {number} [props.zoom] - Zoom level to use when the position is found.
 */
export const ShowMyLocationControl = ({
  areaBounds = null,
  icon = defaultIcon,
  zoom = LOCATION_ZOOM
}) => {
  const map = useMap()
  const markerRef = useRef(null)
  const mountedRef = useRef(true)
  const [position, setPosition] = useState(null)
  const [status, setStatus] = useState('idle')
  const [message, setMessage] = useState('')

  useEffect(() => {
    mountedRef.current = true

    return () => {
      mountedRef.current = false
    }
  }, [])

  // Div icons have no alt attribute, so describe the marker element directly.
  useEffect(() => {
    const element = markerRef.current?.getElement?.()

    if (!element) {
      return
    }

    element.setAttribute('role', 'img')
    element.setAttribute('aria-label', translations.yourLocation)
    element.setAttribute('title', translations.yourLocation)
  }, [position])

  const showError = (errorMessage) => {
    setStatus('error')
    setMessage(errorMessage)
  }

  const handleLocate = () => {
    if (window.isSecureContext === false) {
      showError(translations.insecureContext)
      return
    }

    if (!navigator.geolocation) {
      showError(translations.unsupported)
      return
    }

    setStatus('loading')
    setMessage(translations.locating)

    navigator.geolocation.getCurrentPosition(
      ({ coords }) => {
        if (!mountedRef.current) {
          return
        }

        const latlng = L.latLng(coords.latitude, coords.longitude)

        if (areaBounds && !L.latLngBounds(areaBounds).contains(latlng)) {
          showError(translations.outsideArea)
          return
        }

        setPosition(latlng)
        setStatus('success')
        setMessage(translations.locationFound)
        map.flyTo(latlng, zoom)
      },
      (error) => {
        if (!mountedRef.current) {
          return
        }

        if (error?.code === PERMISSION_DENIED) {
          showError(translations.permissionDenied)
        } else if (error?.code === TIMEOUT) {
          showError(translations.timeout)
        } else {
          showError(translations.unavailable)
        }
      },
      {
        enableHighAccuracy: false,
        timeout: GEOLOCATION_TIMEOUT,
        maximumAge: GEOLOCATION_MAX_AGE
      }
    )
  }

  const buttonLabel = status === 'loading'
    ? translations.locating
    : translations.showMyLocation

  const statusClassName = [
    'a4-show-my-location__status',
    status === 'success' ? 'aural' : '',
    status === 'error' ? 'a4-show-my-location__status--error' : ''
  ].filter(Boolean).join(' ')

  return (
    <>
      <ControlWrapper position="topleft" className="a4-show-my-location-control">
        <button
          type="button"
          className="a4-show-my-location__button"
          onClick={handleLocate}
          disabled={status === 'loading'}
          aria-label={buttonLabel}
          aria-busy={status === 'loading'}
          title={buttonLabel}
        >
          {status === 'loading'
            ? <span className="a4-show-my-location__spinner" aria-hidden="true" />
            : <i className="fas fa-location-crosshairs" aria-hidden="true" />}
        </button>
        {message && (
          <div
            className={statusClassName}
            role="status"
            aria-live="polite"
          >
            {message}
          </div>
        )}
      </ControlWrapper>
      {position && (
        <Marker
          ref={markerRef}
          position={position}
          icon={icon}
          alt={translations.yourLocation}
          interactive={false}
          keyboard={false}
          zIndexOffset={1000}
        />
      )}
    </>
  )
}

export default ShowMyLocationControl
