import React, { useEffect, useState } from 'react'
import django from 'django'
import { useMap } from 'react-leaflet'
import L from 'leaflet'

import useDebounce from '../../../static/useDebounce'
import { AutoComplete } from '../../../static/forms/AutoComplete'
import { makeIcon } from './GeoJsonMarker'

const addressSearchCapStr = django.gettext('Address Search')
let activeMarker = null

function fetchSuggestions (address) {
  return fetch(apiUrl + '?address=' + address)
    .then((response) => response.json())
}

function getSearchResultText (feature) {
  return feature.properties.strname + ' ' + feature.properties.hsnr + ' in ' + feature.properties.plz + ' ' + feature.properties.bezirk_name
}

const apiUrl = 'https://bplan-prod.liqd.net/api/addresses/'

const AddressSearch = ({
  onSubmitHandler
}) => {
  const [geoJson, setGeoJson] = useState(null)
  const [searchString, setSearchString] = useState('')
  const map = useMap()

  const debouncedOnChange = useDebounce(async () => {
    const geoJson = await fetchSuggestions(searchString)
    setGeoJson(geoJson)
  })

  const onAddressSelect = (val) => {
    let leafletMarker
    if (activeMarker) {
      map.removeLayer(activeMarker)
    }
    const feature = geoJson.features[val[0]]
    activeMarker = L.geoJSON(feature, {
      pointToLayer: function (feature, latlng) {
        leafletMarker = L.marker(latlng, {
          icon: makeIcon('/static/images/map_pin_active.svg'),
          alt: 'Marker: ' + getSearchResultText(feature)
        })
        return leafletMarker
      }
    }).addTo(map)
    leafletMarker.getElement()?.focus()

    map.flyToBounds(activeMarker.getBounds(), { maxZoom: 13 })
  }

  useEffect(() => {
    debouncedOnChange()
  }, [searchString])

  return (
    <div className="a4-address-search">
      <form
        onSubmit={(e) => {
          e.preventDefault()
          onSubmitHandler(e)
        }}
        data-embed-target="ignore"
      >
        <div className="a4-address-search__search-form">
          <div className="form-group">
            <AutoComplete
              choices={geoJson
                ? geoJson.features.map((feature, index) => ({
                  name: getSearchResultText(feature),
                  value: index
                }))
                : []}
              // filtering is happening on the server
              filterFn={() => true}
              hideLabel
              label={addressSearchCapStr}
              placeholder={addressSearchCapStr}
              onChangeInput={(val) => {
                setSearchString(val)

                if (val === '' && activeMarker) {
                  map.removeLayer(activeMarker)
                  activeMarker = null
                }
              }}
              onChange={onAddressSelect}
              inputValue={searchString}
              before={
                <i className="fa fa-search" aria-hidden="true" />
              }
            />
          </div>
        </div>
      </form>
    </div>
  )
}

export default AddressSearch
