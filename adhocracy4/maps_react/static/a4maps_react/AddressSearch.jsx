import React, { useEffect, useState } from 'react'
import django from 'django'

import useDebounce from '../../../static/useDebounce'
import { AutoComplete } from '../../../static/forms/AutoComplete'

const addressSearchCapStr = django.gettext('Address Search')

function fetchSuggestions (address, apiUrl) {
  return fetch(apiUrl + '?search=' + address)
    .then((response) => response.json())
}

export function getSearchResultText (feature) {
  return feature.properties.str_name + ' ' + feature.properties.hnr + ' in ' + feature.properties.plz + ' ' + feature.properties.bez_name
}

const AddressSearch = ({
  onSelectAddress,
  onChangeInput,
  apiUrl
}) => {
  const [suggestions, setSuggestions] = useState([])
  const [rawFeatures, setRawFeatures] = useState([])
  const [searchString, setSearchString] = useState('')

  const debouncedOnChange = useDebounce(async () => {
    if (!searchString.trim()) {
      setSuggestions([])
      setRawFeatures([])
      return
    }

    const data = await fetchSuggestions(searchString, apiUrl)
    const features = data.results?.features || []
    setRawFeatures(features)

    const newSuggestions = features.map((feature, index) => ({
      name: getSearchResultText(feature),
      value: index.toString()
    }))
    setSuggestions(newSuggestions)
  })

  useEffect(() => {
    debouncedOnChange()
  }, [searchString, debouncedOnChange])

  return (
    <div className="a4-address-search">
      <div className="a4-address-search__search-form">
        <div className="form-group">
          <AutoComplete
            choices={suggestions}
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
              if (val.length > 0 && rawFeatures.length > 0) {
                const selectedIndex = parseInt(val[0])
                const selectedAddress = rawFeatures[selectedIndex]
                const newSearchString = getSearchResultText(selectedAddress)
                setSearchString(newSearchString)
                onChangeInput?.(newSearchString)
                onSelectAddress(selectedAddress)
              }
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
