import React from 'react'
import django from 'django'
import ErrorList from '../../static/ErrorList'

export const EditPollChoice = (props) => {
  return (
    <div className="form-group">
      <div className="input-group">
        <label htmlFor={'id_choices-' + props.id + '-name'}>
          <span className="visually-hidden">{props.label}</span>
          <input
            id={'id_choices-' + props.id + '-name'}
            name={'choices-' + props.id + '-name'}
            type="text"
            className="input-group__input"
            value={props.choice.label}
            onChange={(e) => { props.onLabelChange(e.target.value) }}
            disabled={props.isOther}
          />
        </label>
        <button
          className="input-group__after input-group__after-outside btn btn--light"
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
      <ErrorList errors={props.errors} field="label" />
    </div>
  )
}
