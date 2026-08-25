import React from 'react'

interface EditPollCheckboxProps {
  id: number | string
  field: string
  label: string
  checked?: boolean
  onChange?: (checked: boolean) => void
  disabled?: boolean
}

export const EditPollCheckbox = ({
  id,
  field,
  label,
  checked,
  onChange,
  disabled = false
}: EditPollCheckboxProps) => (
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
        onChange={(e) => onChange?.(e.target.checked)}
      />
      &nbsp;
      {label}
    </label>
  </div>
)