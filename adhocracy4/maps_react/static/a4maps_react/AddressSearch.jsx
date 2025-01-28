import React, { useEffect, useState } from 'react'
import django from 'django'

import useDebounce from '../../../static/useDebounce'
import { AutoComplete } from '../../../static/forms/AutoComplete'

const addressSearchCapStr = django.gettext('Address Search')

function fetchSuggestions (address, apiUrl) {
  return fetch(apiUrl + '?address=' + address)
    .then((response) => response.json())
}

export function getSearchResultText (feature) {
  return feature.properties.strname + ' ' + feature.properties.hsnr + ' in ' + feature.properties.plz + ' ' + feature.properties.bezirk_name
}

const AddressSearch = ({
  onSelectAddress,
  onChangeInput,
  apiUrl
}) => {
  const [geoJson, setGeoJson] = useState(null)
  const [searchString, setSearchString] = useState('')

  const debouncedOnChange = useDebounce(async () => {
    const geoJson = await fetchSuggestions(searchString, apiUrl)
    setGeoJson(geoJson)
  })

  useEffect(() => {
    debouncedOnChange()
  }, [searchString, debouncedOnChange])

  return (
    <div className="a4-address-search">
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
              onChangeInput?.(val)
            }}
            onChange={(val) => {
              onSelectAddress(geoJson.features[val[0]])
            }}
            inputValue={searchString}
            before={
              <i className="fa fa-search" aria-hidden="true" />
            }
          />
        </div>
      </div>
    </div>
  )
}

export default AddressSearch
