import React from 'react'

export const IconSwitch = (props) => {
  const {
    activeClass,
    inactiveClass,
    startIconClass,
    endIconClass,
    startText,
    endText,
    startID,
    endID,
    startAria,
    endAria,
    showStartObject,
    showEndObject,
    displayStartObject
  } = props

  return (
    <div className="switch-btn-group-container">
      <div className="btn-group switch-btn-group" role="group">
        <label
          htmlFor={startID}
          className={!displayStartObject ? activeClass : inactiveClass}
        >
          <input
            className="radio__input"
            type="radio"
            value={startID}
            id={startID}
            aria-label={startAria}
            onClick={showStartObject}
            onKeyDown={showStartObject}
          />
          <i className={startIconClass} />
          <span>{startText}</span>
        </label>
        <label
          htmlFor={endID}
          className={displayStartObject ? activeClass : inactiveClass}
        >
          <input
            className="radio__input"
            type="radio"
            id={endID}
            value={endID}
            aria-label={endAria}
            onClick={showEndObject}
            onKeyDown={showEndObject}
          />
          <i className={endIconClass} />
          <span>{endText}</span>
        </label>
      </div>
    </div>
  )
}
