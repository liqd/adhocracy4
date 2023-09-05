import React, { useState } from 'react'

export const SwitchButton = (props) => {
  const [isChecked, setIsChecked] = useState(props.isChecked || false)

  const handleButtonClick = () => {
    setIsChecked(!isChecked)

    if (props.onClickCallback) {
      props.onClickCallback(!isChecked)
    }
  }

  return (
    <button
      id={props.id}
      className="btn-switch"
      aria-labelledby={'switch-id-' + props.id}
      role="switch"
      aria-checked={isChecked}
      onClick={handleButtonClick}
    >
      <span className="btn-switch__switch">
        <span className="btn-switch__adjuster" />
      </span>
      <span
        id={'switch-id-' + props.id}
      >
        {isChecked
          ? props.switchLabelOn
          : props.switchLabelOff}
      </span>
    </button>
  )
}
