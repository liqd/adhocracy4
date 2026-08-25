import React, { useEffect, useRef, useState } from 'react'
import { useMap } from 'react-leaflet'
import AddressSearch, { getSearchResultText } from './AddressSearch'
import GeoJsonMarker, { makeIcon } from './GeoJsonMarker'
import ControlWrapper from './ControlWrapper'

interface SearchAndShowAddressProps {
  apiUrl: string
}

const SearchAndShowAddress = ({
  apiUrl
}: SearchAndShowAddressProps) => {
  const map = useMap()
  const markerRef = useRef<any>(null)
  const [activeFeature, setActiveFeature] = useState<any>(null)

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
          onSelectAddress={setActiveFeature} onChangeInput={(val: string) => {
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
