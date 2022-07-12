import React, { useState } from 'react'
import django from 'django'

const translated = {
  termsOfUseLabelText: django.gettext('Yes, I have read and agree to this organisation\'s %(linkStart)s terms of use %(linkEnd)s.'),
  termsOfUseHelpText: django.gettext('You can still manage all your preferences on User Agreements.')
}

export const TermsOfUseCheckbox = (props) => {
  const [checked, setChecked] = useState(false)
  const handleOnChange = (e) => {
    setChecked(e.target.checked)
    props.onChange(e.target.checked)
  }
  const linkParts = {
    linkStart: '<a href="' + props.orgTermsUrl + '" target="_blank">',
    linkEnd: '</a>'
  }
  const termsOfUseLabel = django.interpolate(translated.termsOfUseLabelText, linkParts, true)

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
      <label // eslint-disable-line jsx-a11y/label-has-associated-control
        // eslint ignores the dangerouslySetInnerHTML and gives a wrong error
        className="a4-termsofuse__checkbox-label"
        htmlFor={props.id}
        dangerouslySetInnerHTML={{ __html: termsOfUseLabel }}
      />
      <p className="a4-termsofuse__checkbox-helptext">
        {translated.termsOfUseHelpText}
      </p>
    </div>
  )
}
