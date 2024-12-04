import React, { useState } from 'react'
import { ControlBarDropdown } from './ControlBarDropdown'
import { ControlBarListMapSwitch } from './ControlBarListMapSwitch'
import { ControlBarSearch } from './ControlBarSearch'
import { ControlBarSearchTerm } from './ControlBarSearchTerm'
import { FilterToggle } from '../../contrib/assets/FilterToggle'
import django from 'django'
import { useSearchParams } from 'react-router'

const translated = {
  showFilters: django.gettext('Show filters'),
  hideFilters: django.gettext('Hide filters'),
  filters: django.gettext('Filters'),
  nav: django.gettext('Search, filter and sort the ideas list')
}

const getResultCountText = (count) => {
  const foundProposalsText = django.ngettext(
    '1 proposal found.',
    '%s proposals found.',
    count
  )
  return django.interpolate(foundProposalsText, [count])
}

export const ControlBar = (props) => {
  const [expandFilters, setExpandFilters] = useState()
  const [resultString, setResultString] = useState(false)
  const [queryParams, setQueryParams] = useSearchParams()
  const [term, setTerm] = useState(queryParams.get('search') || '')

  // check list is filtered not just ordered
  // else needed for search term deletion
  const handleResultString = () => {
    const entryArray = Array.from(queryParams.keys())
    if (
      (entryArray.length === 2 && entryArray[1] !== 'ordering') ||
      entryArray.length > 2
    ) {
      setResultString(true)
    } else {
      setResultString(false)
    }
  }

  const applyFilter = (filterType, filterChoice) => {
    queryParams.set(filterType, filterChoice[0])

    // to avoid empty pagination page for given
    // filter settings, always show first page,
    queryParams.delete('page')
    handleResultString()
    setQueryParams(queryParams)
  }

  const applySearch = (value) => {
    setTerm(value)
    applyFilter('search', [value])
    handleResultString()
  }

  const handleToggleFilters = (e) => {
    e.preventDefault()
    setExpandFilters(!expandFilters)
  }

  return (
    <nav
      className="container u-spacer-bottom u-spacer-top-double"
      aria-label={translated.nav}
    >
      <div className="offset-lg-2 col-lg-8">
        <ControlBarListMapSwitch query={queryParams} />
        <>
          <div className="control-bar">
            <div className="control-bar__item">
              <ControlBarSearch
                term={term}
                onSearch={(value) => applySearch(value)}
              />
            </div>
            {props.filters?.ordering && (
              <ControlBarDropdown
                key="ordering_dropdown"
                filter={props.filters.ordering}
                current={queryParams.get('ordering')}
                filterId="id_ordering"
                onSelectFilter={(choice) => applyFilter('ordering', choice)}
              />
            )}
            <div className="control-bar__item control-bar__right">
              <FilterToggle
                showFilters={expandFilters}
                onClickToggleFilter={handleToggleFilters}
                btnString={translated.filters}
                showFiltersString={translated.showFilters}
                hideFiltersString={translated.hideFilters}
              />
            </div>
          </div>
          {props.filters && expandFilters && (
            <>
              <div className="control-bar">
                {Object.keys(props.filters).map((type, idx) => {
                  const filterItem = props.filters[type]
                  return (
                    type !== 'ordering' && (
                      <ControlBarDropdown
                        key={'filter_' + idx}
                        filter={filterItem}
                        current={queryParams.get(type)}
                        filterId={'id_' + type}
                        onSelectFilter={(choice) => applyFilter(type, choice)}
                      />
                    )
                  )
                })}
              </div>
            </>
          )}
        </>
        {/* only show result string if list filtered or searched not just ordered */}
        {resultString && (
          <div className="control-bar">
            {props.numOfResults >= 0 && getResultCountText(props.numOfResults)}
          </div>
        )}
        {term && (
          <ControlBarSearchTerm term={term} onDismiss={() => applySearch('')} />
        )}
      </div>
    </nav>
  )
}
