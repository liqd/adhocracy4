import React from 'react'

export const ToggleSwitch = (props) => {
  const {
    onSwitchStr,
    offSwitchStr,
    uniqueId,
    toggleSwitch
  } = props

  return (
    <div className="switch__group">
      <label htmlFor={uniqueId} className="switch__label">
        <span className="switch__label-text" aria-hidden="true">{onSwitchStr}</span>
        <input
          className="switch__input"
          type="checkbox"
          data-check-switch=""
          role="switch"
          id={uniqueId}
          name={uniqueId}
          onChange={toggleSwitch}
          aria-label={offSwitchStr}
        />
        <span className="switch__toggle" aria-hidden="true" />
      </label>
    </div>
  )
}
