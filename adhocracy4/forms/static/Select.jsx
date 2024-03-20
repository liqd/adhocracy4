import React from 'react'

export const Select = ({ onSelect, choices, label, placeholder, id, ...rest }) => {
  const onSelectWrapper = (e) => {
    const choice = choices.find(choice => choice[0] === e.target.value)
    onSelect(choice)
  }

  return (
    <div className="form-group a4-forms__select">
      <label htmlFor={id} className="form-label a4-forms__select__label">
        {label}
      </label>
      <div className="a4-forms__select__wrapper">
        <select className="form-control a4-forms__select__input" id={id} onChange={onSelectWrapper} {...rest}>
          {placeholder && <option value="">{placeholder}</option>}
          {choices.map((choice, idx) => (
            <option key={'filter-choice_' + idx} value={choice[0]}>
              {choice[1]}
            </option>
          ))}
        </select>
      </div>
    </div>
  )
}
