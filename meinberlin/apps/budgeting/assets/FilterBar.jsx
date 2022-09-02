import React, { useState, useEffect } from 'react'
import { FilterBarDropdown } from './FilterBarDropdown'
import { FilterBarListMapSwitch } from './FilterBarListMapSwitch'

export const FilterBar = props => {
  const [filterString, setFilterString] = useState('')
  const [filterObject, setFilterObject] = useState({})

  // Creating an object with all used filters.
  // Input: filterType: 'ordering', filterChoice = '[-created, am aktuellsten]'
  // Output: { ordering: ['-created', 'am aktuellsten'] }
  const makeFilterObject = (filterType, filterChoice) => {
    const newFilterChoice = {}
    newFilterChoice[filterType] = filterChoice
    const newFilterObject = Object.assign(filterObject, newFilterChoice)
    setFilterObject(newFilterObject)
  }

  // From a given object it returns a query string to use
  // for API requests.
  // Input: { ordering: ['-created', 'am aktuellsten'] }
  // Output: '&ordering=-created'
  const encodeFilterString = filterObject => {
    const newFilterString = Object.keys(filterObject).reduce((acc, curr) => {
      // if filter with empty string is selected ('All')
      // then do not append a querystring, e.g. '&is_archived=' is ommitted
      return filterObject[curr][0]
        ? `${acc}&${curr}=${filterObject[curr][0]}`
        : acc
    }, '')
    setFilterString(newFilterString)
  }

  const applyFilter = (filterType, filterChoice) => {
    makeFilterObject(filterType, filterChoice)
    encodeFilterString(filterObject)
  }

  const prepareFilter = (filter, filterType) => {
    filter.current = selectedFilter(filterType)
    return filter
  }

  const selectedFilter = filterType =>
    filterObject && filterObject[filterType] && filterObject[filterType][1]

  useEffect(() => {
    props.onChangeFilters(filterString)
  }, [filterObject, filterString])

  return (
    <div className="container u-spacer-bottom u-spacer-top-double">
      <div className="offset-lg-2 col-lg-8">
        <div className="control-bar control-bar--list">
          <FilterBarListMapSwitch query={filterString} />
          {props.filters &&
            Object.keys(props.filters).map((type, idx) => {
              const filterCopy = props.filters[type]
              const filter = prepareFilter(filterCopy, type)
              return (
                <FilterBarDropdown
                  key={`filter_${idx}`}
                  filter={filter}
                  onSelectFilter={choice => applyFilter(type, choice)}
                />
              )
            })}
        </div>
      </div>
    </div>
  )
}
