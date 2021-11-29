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

  useEffect(() => {
    props.onChangeFilters(filterString)
  }, [filterObject, filterString])

  return (
    <div className="l-wrapper u-spacer-bottom u-spacer-top-double">
      <div className="l-center-8">
        <div className="control-bar">
          <div className="control-bar-item">
            <FilterBarListMapSwitch query={filterString} />
          </div>
          {props.filters &&
            Object.keys(props.filters).map((filterType, idx) => {
              const filter = props.filters[filterType]
              // adding position to ordering dropdown
              filterType === 'ordering' && (filter.position = 'right')
              const selectedFilter =
                filterObject &&
                filterObject[filterType] &&
                filterObject[filterType][1]
              return (
                <div
                  className={
                    filter.position
                      ? `control-bar-item__${filter.position}`
                      : 'control-bar-item'
                  }
                  key={`filter_${idx}`}
                >
                  <FilterBarDropdown
                    filterName={filter.label}
                    selectedFilter={selectedFilter}
                    filterChoices={filter.choices}
                    onSelectFilter={
                      filterChoice => applyFilter(filterType, filterChoice)
                    }
                  />
                </div>
              )
            })}
        </div>
      </div>
    </div>
  )
}
