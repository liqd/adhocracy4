import React, { useEffect, useState } from 'react'

export const ControlBarDropdown = props => {
  const { filter } = props
  const [currentChoiceName, setCurrentChoiceName] = useState(filter.current)

  const onSelectFilter = filterChoice => {
    setCurrentChoiceName(filterChoice[1])
    props.onSelectFilter(filterChoice)
  }

  const getFilterByValue = filterval => {
    return filter.choices.find(choice => choice[0] === filterval)
  }

  useEffect(() => {
    if (!filter.current) {
      if (filter.default) {
        const filterChoice = getFilterByValue(filter.default)
        setCurrentChoiceName(filterChoice[1])
        onSelectFilter(filterChoice)
      } else {
        setCurrentChoiceName(filter.choices[0])
        onSelectFilter(filter.choices[0])
      }
    }
  }, [])

  const getIcon = choiceIndex => {
    return filter.icons.find(icon => icon[0] === choiceIndex)
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
        {`${filter.label}: ${currentChoiceName}`}
        <i className="fa fa-caret-down" aria-hidden />
      </button>
      <ul aria-labelledby={props.filterId} className="dropdown-menu">
        {filter.choices.map((choice, idx) => {
          const icon = filter.icons && getIcon(choice[0])
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
