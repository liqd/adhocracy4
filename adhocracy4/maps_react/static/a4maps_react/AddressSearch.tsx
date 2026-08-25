import React, { useEffect, useState } from 'react'
import django from 'django'

import useDebounce from '../../../static/useDebounce'
import { AutoComplete } from '../../../static/forms/AutoComplete'

const addressSearchCapStr = django.gettext('Address Search')

function fetchSuggestions (address: string, apiUrl: string) {
  return fetch(apiUrl + '?search=' + address)
    .then((response) => response.json())
}

interface GeoJsonFeature {
  properties?: {
    strasse?: string
    haus?: string
    plz?: string
    ortsteil?: string
  }
}

export function getSearchResultText (feature: GeoJsonFeature | undefined) {
  const {
    strasse = '',
    haus = '',
    plz = '',
    ortsteil = ''
  } = feature?.properties || {}

  // eslint-disable-next-line no-restricted-syntax
  return `${strasse} ${haus} in ${plz} ${ortsteil}`.trim()
}

interface AddressSearchProps {
  onSelectAddress?: (feature: GeoJsonFeature) => void
  onChangeInput?: (val: string) => void
  apiUrl: string
}

const AddressSearch = ({
  onSelectAddress,
  onChangeInput,
  apiUrl
}: AddressSearchProps) => {
  const [suggestions, setSuggestions] = useState<Array<{ name: string; value: string }>>([])
  const [rawFeatures, setRawFeatures] = useState<GeoJsonFeature[]>([])
  const [searchString, setSearchString] = useState('')

  const debouncedOnChange = useDebounce(async () => {
    if (!searchString.trim()) {
      setSuggestions([])
      setRawFeatures([])
      return
    }

    const data = await fetchSuggestions(searchString, apiUrl)
    const features: GeoJsonFeature[] = data.results?.features || []
    setRawFeatures(features)

    const newSuggestions = features.map((feature: GeoJsonFeature, index: number) => ({
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
            onChangeInput={(val: string) => {
              setSearchString(val)
              if (onChangeInput) onChangeInput(val)
            }}
            onChange={(val: string[]) => {
              if (val.length > 0 && rawFeatures.length > 0) {
                const selectedIndex = parseInt(val[0])
                const selectedAddress = rawFeatures[selectedIndex]
                const newSearchString = getSearchResultText(selectedAddress)
                setSearchString(newSearchString)
                if (onSelectAddress && selectedAddress) onSelectAddress(selectedAddress)
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
