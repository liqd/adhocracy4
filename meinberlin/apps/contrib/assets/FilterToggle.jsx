import React from 'react'

export const FilterToggle = (props) => {
  const {
    showFilters,
    onClickToggleFilter,
    btnString,
    showFiltersString,
    hideFiltersString
  } = props

  return (
    <>
      {!showFilters
        ? <button
            className="btn btn--icon btn--light"
            type="button"
            aria-describedby="span-id"
            onClick={onClickToggleFilter}
          >
          <i
            className="fas fa-sliders-h"
            aria-hidden="true"
          />
          <span id="span-id" className="visually-hidden">{showFiltersString}</span>
          {btnString}
        </button> // eslint-disable-line react/jsx-closing-tag-location
        : <button
            className="btn btn--icon btn--light"
            type="button"
            aria-describedby="span-id"
            onClick={onClickToggleFilter}
          >
          <i
            className="fas fa-times"
            aria-hidden="true"
          />
          <span id="span-id" className="visually-hidden">{hideFiltersString}</span>
          {btnString}
          {/* eslint-disable-next-line react/jsx-closing-tag-location */}
        </button>}
    </>

  )
}
