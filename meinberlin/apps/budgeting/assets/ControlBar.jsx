import React, { useState } from 'react'
import { ControlBarDropdown } from './ControlBarDropdown'
import { ControlBarListMapSwitch } from './ControlBarListMapSwitch'
import { ControlBarSearch } from './ControlBarSearch'
import { ControlBarSearchTerm } from './ControlBarSearchTerm'
import { SpacedSpan } from './SpacedSpan'
import django from 'django'
import { useSearchParams } from 'react-router-dom'

const translated = {
  showFilters: django.gettext('Show filters'),
  hideFilters: django.gettext('Hide filters'),
  filters: django.gettext('Filters')
}

const getResultCountText = (count) => {
  const foundProposalsText =
    django.ngettext('1 proposal found.', '%s proposals found.', count)
  return django.interpolate(foundProposalsText, [count])
}

export const ControlBar = props => {
  const [expandFilters, setExpandFilters] = useState()
  const [queryParams, setQueryParams] = useSearchParams()
  const [term, setTerm] = useState(queryParams.get('search') || '')

  const applyFilter = (filterType, filterChoice) => {
    if (filterChoice[0] !== '') {
      queryParams.set(filterType, filterChoice[0])
    } else {
      queryParams.delete(filterType)
    }

    // to avoid empty pagination page for given
    // filter settings, always show first page,
    queryParams.delete('page')

    setQueryParams(queryParams)
  }

  const applySearch = (value) => {
    setTerm(value)
    applyFilter('search', [value])
  }

  return (
    <div className="container u-spacer-bottom u-spacer-top-double">
      <div className="offset-lg-2 col-lg-8">
        <ControlBarListMapSwitch query={queryParams} />
      </div>
      <div className="offset-lg-2 col-lg-8">
        <div className="control-bar">
          <div className="control-bar__item">
            <ControlBarSearch
              term={term}
              onSearch={value => applySearch(value)}
            />
          </div>
          {props.filters?.ordering && (
            <ControlBarDropdown
              key="ordering_dropdown"
              filter={props.filters.ordering}
              current={queryParams.get('ordering')}
              filterId="id_ordering"
              onSelectFilter={choice => applyFilter('ordering', choice)}
            />
          )}
          <div className="control-bar__item control-bar__right">
            <button
              className="btn btn--light"
              aria-label={
                expandFilters
                  ? translated.hideFilters
                  : translated.showFilters
              }
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
              const filterItem = props.filters[type]
              return type !== 'ordering' && (
                <ControlBarDropdown
                  key={`filter_${idx}`}
                  filter={filterItem}
                  current={queryParams.get(type)}
                  filterId={`id_${type}`}
                  onSelectFilter={choice => applyFilter(type, choice)}
                />
              )
            })}
          </div>
        </div>}
      <div className="offset-lg-2 col-lg-8">
        <div className="control-bar">
          {props.numOfResults >= 0 && getResultCountText(props.numOfResults)}
        </div>
      </div>
      {term &&
        <div className="offset-lg-2 col-lg-8">
          <ControlBarSearchTerm
            term={term}
            onDismiss={() => applySearch('')}
          />
        </div>}
    </div>
  )
}
