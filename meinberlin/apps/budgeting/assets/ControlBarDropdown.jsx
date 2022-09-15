import React, { useEffect } from 'react'

export const ControlBarDropdown = props => {
  const { filter: { label, choices, current, icons } } = props

  const onSelectFilter = filter => {
    props.onSelectFilter(filter)
  }

  const getFilterByValue = filterval => {
    return choices.find(choice => choice[0] === filterval)
  }

  useEffect(() => {
    if (!current) {
      if (props.filter.default) {
        onSelectFilter(getFilterByValue(props.filter.default))
      } else {
        onSelectFilter(choices[0])
      }
    }
  })

  const getIcon = choiceIndex => {
    return icons.find(icon => icon[0] === choiceIndex)
  }

  return (
    <div className="dropdown control-bar__item">
      <button
        type="button"
        className="dropdown-toggle btn btn--light btn--select"
        data-bs-toggle="dropdown"
        data-flip="false"
        aria-haspopup="true"
        aria-expanded="false"
        id={props.filterId}
      >
        {current ? `${label}: ${current}` : `${label}`}
        <i className="fa fa-caret-down" aria-hidden />
      </button>
      <ul aria-labelledby={props.filterId} className="dropdown-menu">
        {choices.map((choice, idx) => {
          const icon = icons && getIcon(choice[0])
          return (
            <li key={`filter-choice_${idx}`}>
              <button onClick={() => onSelectFilter(choice)}>
                {icon && (
                  <img className="dropdown-item__icon" src={icon[1]} alt="" />
                )}
                {choice[1]}
              </button>
            </li>
          )
        })}
      </ul>
    </div>
  )
}
