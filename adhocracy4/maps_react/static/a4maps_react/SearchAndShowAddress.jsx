import React, { useEffect, useRef } from 'react'
import { useMap } from 'react-leaflet'
import AddressSearch, { getSearchResultText } from './AddressSearch'
import GeoJsonMarker, { makeIcon } from './GeoJsonMarker'
import ControlWrapper from './ControlWrapper'

const SearchAndShowAddress = ({
  apiUrl
}) => {
  const map = useMap()
  const markerRef = useRef(null)
  const [activeFeature, setActiveFeature] = React.useState(null)

  useEffect(() => {
    if (markerRef.current && map) {
      map.getContainer().scrollIntoView({ behavior: 'smooth', block: 'center' })
      map.flyTo(markerRef.current.getLatLng(), 13)
      map.once('zoomend moveend', () => {
        markerRef.current.getElement().focus()
      })
    }
  }, [markerRef, map, activeFeature])

  return (
    <>
      <ControlWrapper position="topleft" className="projects-map__search">
        <AddressSearch
          apiUrl={apiUrl}
          onSelectAddress={setActiveFeature} onChangeInput={(val) => {
            if (val === '' && activeFeature) {
              setActiveFeature(null)
            }
          }}
        />
      </ControlWrapper>
      {activeFeature && (
        <GeoJsonMarker
          ref={markerRef}
          feature={activeFeature}
          icon={makeIcon('/static/images/map_pin_active.svg')}
          alt={'Marker: ' + getSearchResultText(activeFeature)}
        />
      )}
    </>
  )
}

export default SearchAndShowAddress
