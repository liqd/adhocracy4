import React from 'react'
import django from 'django'
import FormFieldError from '../../../static/FormFieldError'

export const EditPollChoice = (props) => {
  return (
    <div className="form-group">
      <div htmlFor={'id_choices-' + props.id + '-name'}>
        {django.pgettext('noun', 'Answer')} {props.index}
        {props.choiceId &&
          <span className="editpoll__help-text"> Id: A{props.choiceId}</span>}
        <span className="visually-hidden">{props.label}</span>
      </div>
      <div className="input-group">
        <input
          id={'id_choices-' + props.id + '-name'}
          name={'choices-' + props.id + '-name'}
          type="text"
          className="input-group__input"
          value={props.choice.label}
          onChange={(e) => { props.onLabelChange(e.target.value) }}
          disabled={props.isOther}
          aria-invalid={props.errors ? 'true' : 'false'}
          aria-describedby={props.errors && 'id_error-' + props.id}
        />
        <button
          className="input-group__after btn editpoll__btn--delete"
          onClick={props.onDelete}
          title={django.gettext('remove')}
          type="button"
          disabled={props.undeletable}
        >
          <i
            className="fa fa-times"
            aria-label={django.gettext('remove')}
          />
        </button>
      </div>
      <FormFieldError
        id={'id_error-' + props.id}
        error={props.errors}
        field="label"
      />
    </div>
  )
}
