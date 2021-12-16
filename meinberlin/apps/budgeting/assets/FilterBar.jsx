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
    const defaultFilter = getDefaultFilter(filter)
    filterType === 'ordering' && (filter.position = 'right')
    filter.current = selectedFilter(filterType) || defaultFilter
    return filter
  }

  const selectedFilter = filterType =>
    filterObject && filterObject[filterType] && filterObject[filterType][1]

  const getDefaultFilter = filter => {
    // Return Early, if no default, take "All"-choice
    if (!filter.default) return filter.choices[0][1]
    // Get name of default filter
    return filter.choices
      .map(f => f[0] === filter.default && f[1])
      .filter(f => !!f)
  }

  const getClassName = position => {
    return position ? `control-bar-item__${position}` : 'control-bar-item'
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
            Object.keys(props.filters).map((type, idx) => {
              const filterCopy = props.filters[type]
              const filter = prepareFilter(filterCopy, type)
              return (
                <div
                  className={getClassName(filter.position)}
                  key={`filter_${idx}`}
                >
                  <FilterBarDropdown
                    filter={filter}
                    onSelectFilter={choice => applyFilter(type, choice)}
                  />
                </div>
              )
            })}
        </div>
      </div>
    </div>
  )
}
