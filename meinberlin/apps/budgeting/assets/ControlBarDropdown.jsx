import React, { useState } from 'react'

// FIXME: maybe more elegant way?
// this is only relevant for the first page load,
// where the url does not contain all default query params.
// case 1: if there is a current, get the name of the current
// case 2: if there is a default, get its verbose name
// case 3a: if there is no default and choices has '', get the name of ''
// case 3b: otherwise get name of first choice
const getDefaultName = (f, curr) => {
  let filterChoice
  if (f.choices.some(c => c[0] === curr)) {
    filterChoice = f.choices.filter(c => c[0] === curr)[0]
  } else if (f.default) {
    filterChoice = f.choices.filter(c => c[0] === f.default)[0]
  } else {
    const emptyStringIndex = f.choices.findIndex(choice => choice === '')
    filterChoice = emptyStringIndex > -1
      ? f.choices[emptyStringIndex]
      : f.choices[0]
  }
  return filterChoice[1]
}

export const ControlBarDropdown = props => {
  const { filter } = props
  const [currentChoiceName, setCurrentChoiceName] =
    useState(getDefaultName(filter, props.current))

  const onSelectFilter = filterChoice => {
    setCurrentChoiceName(filterChoice[1])
    props.onSelectFilter(filterChoice)
  }

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
        {filter.label + ':' + ' ' + currentChoiceName}
        <i className="fa fa-caret-down" aria-hidden />
      </button>
      <ul aria-labelledby={props.filterId} className="dropdown-menu">
        {filter.choices.map((choice, idx) => {
          const icon = filter.icons && getIcon(choice[0])
          return (
            <li key={'filter-choice_' + idx}>
              <button
                className="dropdown-item"
                onClick={() => onSelectFilter(choice)}
              >
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
