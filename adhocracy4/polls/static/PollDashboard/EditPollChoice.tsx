import React from 'react'
import FormFieldError from '../../../static/FormFieldError'
import django from 'django'

interface Choice {
  label: string;
  // Add other choice properties if they exist
}

interface EditPollChoiceProps {
  id: string | number;
  index: number;
  choiceId?: string | number;
  label?: string;
  choice: Choice;
  errors?: Record<string, string>;
  isOther?: boolean;
  undeletable?: boolean;
  onLabelChange?: (value: string) => void;
  onDelete: () => void;
}

export const EditPollChoice = React.forwardRef<HTMLDivElement, EditPollChoiceProps>((props, ref) => {
  return (
    <div className="form-group" ref={ref}>
      <label htmlFor={'id_choices-' + props.id + '-name'}>
        {django.pgettext('noun', 'Answer')} {props.index}
        {props.choiceId &&
          <span className="editpoll__help-text"> Id: A{props.choiceId}</span>}
        <span className="visually-hidden">{props.label}</span>
      </label>
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
})

EditPollChoice.displayName = 'EditPollChoice'
