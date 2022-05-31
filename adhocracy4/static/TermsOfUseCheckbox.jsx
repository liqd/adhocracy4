import React, { useState } from 'react'
import django from 'django'

const translated = {
  termsOfUse: django.gettext('I confirm that I have read and accepted the Terms of Use of the organisation. You can still manage your User Agreements in your account settings.')
}

export const TermsOfUseCheckbox = (props) => {
  const [checked, setChecked] = useState(false)
  const handleOnChange = (e) => {
    setChecked(e.target.checked)
    props.onChange(e.target.checked)
  }

  return (
    <div className="a4-termsofuse__checkbox-container">
      <input
        className="a4-termsofuse__checkbox"
        type="checkbox"
        name="checkbox-terms-of-use"
        id={props.id}
        checked={checked}
        onChange={handleOnChange}
      />
      <label
        className="a4-termsofuse__checkbox-label"
        htmlFor={props.id}
      >
        {translated.termsOfUse}
      </label>
    </div>
  )
}
