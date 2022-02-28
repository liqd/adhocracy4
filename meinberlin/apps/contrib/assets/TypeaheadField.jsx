import React from 'react'
import { Typeahead } from 'react-bootstrap-typeahead'

export const TypeaheadField = (props) => {
  const {
    typeaheadHeading,
    uniqueId,
    onTypeaheadChange,
    typeaheadOptions,
    typeaheadSelected,
    typeaheadPlaceholder,
    multipleBoolean
  } = props

  return (
    <div className="form-group filter-bar__typeahead">
      <label htmlFor={uniqueId} className="typeahead__input-label">
        <h2 className="u-no-margin">{typeaheadHeading}</h2>
      </label>
      <span className="typeahead__input-group">
        <span className="typeahead__input-group-prepend">
          <span className="typeahead__input-group-text input-group__before">
            <i className="fas fa-sort-alpha-down" />
          </span>
        </span>
        <Typeahead
          id={uniqueId}
          className="typeahead__input-group-append"
          onChange={onTypeaheadChange}
          labelKey="name"
          multiple={multipleBoolean}
          options={typeaheadOptions}
          selected={typeaheadSelected}
          placeholder={typeaheadPlaceholder}
        />
      </span>
    </div>
  )
}
