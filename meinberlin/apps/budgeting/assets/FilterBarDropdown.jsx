import React from 'react'

export const FilterBarDropdown = props => {
  const { filter: { position, label, choices, current, icons } } = props

  const dropdownClass =
    position === 'right' ? 'dropdown control-bar__right' : 'dropdown'

  const onSelectFilter = filter => {
    props.onSelectFilter(filter)
  }

  const hasIcon = (icons, choice) => {
    if (!icons) return false
    return choice[0] === icons[0][0]
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
        {current ? `${label}: ${current}` : `${label}`}
        <i className="fa fa-caret-down" aria-hidden />
      </button>
      <ul aria-labelledby="id_category" className="dropdown-menu">
        {choices.map((choice, idx) => (
          <li key={`filter-choice_${idx}`}>
            <button onClick={() => onSelectFilter(choice)}>
              {hasIcon(icons, choice) && (
                <img className="dropdown-item__icon" src={icons[0][1]} alt="" />
              )}
              {choice[1]}
            </button>
          </li>
        ))}
      </ul>
    </div>
  )
}
