import React from 'react'

export const FilterBarDropdown = props => {
  const { position, filterName, filterChoices, selectedFilter } = props

  const dropdownClass =
    position === 'right' ? 'dropdown control-bar__right' : 'dropdown'

  const onSelectFilter = filter => {
    props.onSelectFilter(filter)
  }

  return (
    <div className={dropdownClass}>
      <button
        type="button"
        className="dropdown-toggle btn btn--light btn--select"
        data-bs-toggle="dropdown"
        data-flip="false"
        aria-haspopup="true"
        aria-expanded="false"
        id="id_category"
      >
        {selectedFilter ? `${filterName}: ${selectedFilter}` : `${filterName}`}
        <i className="fa fa-caret-down" aria-hidden />
      </button>
      <ul aria-labelledby="id_category" className="dropdown-menu">
        {filterChoices.map((fc, idx) => (
          <li key={`filterChoice_${idx}`}>
            <button onClick={() => onSelectFilter(fc)}>
              {/* FIXME: variant with img (point svg) */}
              {fc[1]}
            </button>
          </li>
        ))}
      </ul>
    </div>
  )
}
