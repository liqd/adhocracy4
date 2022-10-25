import React from 'react'
import django from 'django'
import FormFieldError from '../../../static/FormFieldError'

export const HelptextForm = (props) => {
  return (
    <div className="form-group">
      <label
        htmlFor={'id_helptext-' + props.id + '-name'}
      >
        {django.gettext('Explanation')}
        <textarea
          id={'id_helptext-' + props.id + '-name'}
          name={'helptext-' + props.id + '-name'}
          value={props.question.help_text}
          onChange={(e) => { props.onHelptextChange(e.target.value) }}
          aria-invalid={props.errors ? 'true' : 'false'}
          aria-describedby={props.errors && 'id_error-' + props.id}
        />
        <FormFieldError id={'id_error-' + props.id} error={props.errors} field="help_text" />
      </label>
    </div>
  )
}
