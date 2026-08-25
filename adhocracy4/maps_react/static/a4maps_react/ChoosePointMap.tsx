import django from 'django'
import React, { useRef, useState } from 'react'
import AddressSearch from './AddressSearch'
import Map from './Map'
import AddMarkerControl from './AddMarkerControl'
import Alert from '../../../static/Alert'

const error = django.gettext('The chosen address is outside this map\'s bounds. Please choose another one.')

interface ChoosePointMapProps {
  BaseMap?: any
  apiUrl: string
  input: any
  [key: string]: any
}

const ChoosePointMap = ({ BaseMap = Map, apiUrl, input, ...mapProps }: ChoosePointMapProps) => {
  const mapRef = useRef<any>(null)
  const controlRef = useRef<any>(null)
  const [showOutsideBoundsError, setShowOutsideBoundsError] = useState(false)

  const flyToCoordinates = (coordinates: any) => {
    const map = mapRef.current
    if (map) {
      map.getContainer().scrollIntoView({ behavior: 'smooth', block: 'center' })
      map.flyTo(coordinates, 18)
    }
  }

  return (
    <div className="a4-choose-point-map">
      <AddressSearch
        apiUrl={apiUrl}
        onSelectAddress={(feature: any) => {
          if (controlRef.current && controlRef.current.updateMarker({
            lat: feature.geometry.coordinates[1],
            lng: feature.geometry.coordinates[0]
          })) {
            setShowOutsideBoundsError(false)
            flyToCoordinates(feature.geometry.coordinates.toReversed())
          } else {
            setShowOutsideBoundsError(true)
          }
        }}
        onChangeInput={() => {
          if (showOutsideBoundsError) {
            setShowOutsideBoundsError(false)
          }
        }}
      />
      {showOutsideBoundsError && <Alert type="danger" message={error} />}
      <BaseMap {...mapProps} ref={mapRef} id="choose-point">
        <AddMarkerControl
          point={mapProps.point}
          input={input}
          markerConstraints={mapProps.polygon}
          onDragEnd={() => setShowOutsideBoundsError(false)}
          ref={controlRef}
        />
      </BaseMap>
    </div>
  )
}

export default ChoosePointMap
