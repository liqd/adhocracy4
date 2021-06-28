import React from 'react'
import django from 'django'
import ErrorList from '../../static/ErrorList'

export const HelptextForm = (props) => {
  return (
    <div className="form-group">
      <label
        htmlFor={'id_helptext-' + props.id + '-name'}
      >
        {django.gettext('Helptext')}
        <textarea
          id={'id_helptext-' + props.id + '-name'}
          name={'helptext-' + props.id + '-name'}
          value={props.question.help_text}
          onChange={(e) => { props.onHelptextChange(e.target.value) }}
        />
      </label>
      <ErrorList errors={props.errors} field="label" />
    </div>
  )
}
