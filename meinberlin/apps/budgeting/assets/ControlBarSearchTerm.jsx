import React from 'react'
import django from 'django'

const translated = {
  removeFilters: django.gettext('Remove filters')
}

export const ControlBarSearchTerm = (props) => {
  return (
    <div className="switch-filter__btn-group u-spacer-top">
      <button
        className="btn btn--icon-end btn--light"
        aria-describedby="remove-search-filter"
        onClick={props.onDismiss}
      >
        {props.term}
        <i
          className="fa fa-times"
          aria-hidden="true"
        />
      </button>
      <span
        id="remove-search-filter"
        className="visually-hidden"
      >
        {translated.removeFilters}
      </span>
    </div>
  )
}
