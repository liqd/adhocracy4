import React from 'react'

export const EditPollCheckbox = ({
  id,
  field,
  label,
  checked,
  onChange,
  disabled = false
}) => (
  <div className="form-check">
    <label
      className="form-check__label"
      htmlFor={'id_questions-' + id + '-' + field}
    >
      <input
        type="checkbox"
        id={'id_questions-' + id + '-' + field}
        name={'questions-' + id + '-' + field}
        checked={checked || false}
        disabled={disabled}
        onChange={(e) => onChange(e.target.checked)}
      />
      &nbsp;
      {label}
    </label>
  </div>
)
