import React, { useState, useEffect } from 'react'
import { ControlBarDropdown } from './ControlBarDropdown'
import { ControlBarListMapSwitch } from './ControlBarListMapSwitch'
import { ControlBarSearch } from './ControlBarSearch'
import { ControlBarSearchTerm } from './ControlBarSearchTerm'
import { SpacedSpan } from './SpacedSpan'
import django from 'django'

const translated = {
  toggleFilters: django.gettext('Toggle filters'),
  filters: django.gettext('Filters'),
  results: django.gettext('results found.')
}

export const ControlBar = props => {
  const [filterString, setFilterString] = useState('')
  const [filterObject, setFilterObject] = useState({})
  const [expandFilters, setExpandFilters] = useState()
  const [term, setTerm] = useState('')

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

  const handleSearch = (value) => {
    setTerm(value)
    applyFilter('search', [value])
  }

  useEffect(() => {
    props.onChangeFilters(filterString)
  }, [filterObject, filterString])

  return (
    <div className="container u-spacer-bottom u-spacer-top-double">
      <div className="offset-lg-2 col-lg-8">
        <ControlBarListMapSwitch query={filterString} />
      </div>
      <div className="offset-lg-2 col-lg-8">
        <div className="control-bar">
          <div className="control-bar__item">
            <ControlBarSearch
              term={term}
              onSearch={value => handleSearch(value)}
            />
          </div>
          {props.filters?.ordering && (
            <ControlBarDropdown
              key="ordering_dropdown"
              filter={props.filters.ordering}
              filterId="id_ordering"
              onSelectFilter={choice => applyFilter('ordering', choice)}
            />
          )}
          <div className="control-bar__item control-bar__right">
            <button
              className={
                expandFilters
                  ? 'btn btn--light active'
                  : 'btn btn--light'
              }
              aria-label={translated.toggleFilters}
              onClick={() => setExpandFilters(!expandFilters)}
            >
              <i className="fa fa-filter" aria-hidden="true" />
              <SpacedSpan>
                {translated.filters}
              </SpacedSpan>
            </button>
          </div>
        </div>
      </div>
      {props.filters && expandFilters &&
        <div className="offset-lg-2 col-lg-8">
          <div className="control-bar">
            {Object.keys(props.filters).map((type, idx) => {
              const filterCopy = props.filters[type]
              const filter = prepareFilter(filterCopy, type)
              return type !== 'ordering' && (
                <ControlBarDropdown
                  key={`filter_${idx}`}
                  filter={filter}
                  filterId={`id_${type}`}
                  onSelectFilter={choice => applyFilter(type, choice)}
                />
              )
            })}
          </div>
        </div>}
      <div className="offset-lg-2 col-lg-8">
        <div className="control-bar">
          {`${props.numOfResults} ${translated.results}`}
        </div>
      </div>
      {term &&
        <div className="offset-lg-2 col-lg-8">
          <ControlBarSearchTerm
            term={term}
            onDismiss={() => handleSearch('')}
          />
        </div>}
    </div>
  )
}
