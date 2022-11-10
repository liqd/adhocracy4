import React from 'react'
import { SpacedSpan } from './SpacedSpan'

export const ControlBarSearchTerm = (props) => {
  return (
    <div className="switch-filter__btn-group u-spacer-top">
      <button
        className="btn btn--light btn--small"
        aria-describedby="remove-search-filter"
        onClick={props.onDismiss}
      >
        {props.term}
        <SpacedSpan>
          <i
            className="fa fa-times"
            aria-hidden="true"
          />
        </SpacedSpan>
      </button>
      <span
        id="remove-search-filter"
        className="visually-hidden"
      >
        Filter entfernen
      </span>
    </div>
  )
}
