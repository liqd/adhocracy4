import React from 'react'
import django from 'django'
import FormFieldError from '../../../static/FormFieldError'
import type { PollChoiceEdit } from '../../../static/api/types'

interface EditPollChoiceProps {
  id: number | string
  index: number
  label: string
  choice: PollChoiceEdit
  choiceId?: number | string
  onLabelChange?: (label: string) => void
  onDelete?: () => void
  errors?: Record<string, string[]>
  isOther?: boolean
  undeletable?: boolean
}

export const EditPollChoice = React.forwardRef<HTMLDivElement, EditPollChoiceProps>(
  (props, ref) => {
    return (
      <div className="editpoll__choice form-group" ref={ref}>
        <div {...{ htmlFor: 'id_choices-' + props.id + '-name' }}>
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
            onChange={(e) => { props.onLabelChange?.(e.target.value) }}
            disabled={props.isOther}
            aria-invalid={props.errors ? 'true' : 'false'}
            aria-describedby={props.errors ? 'id_error-' + props.id : undefined}
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
)

EditPollChoice.displayName = 'EditPollChoice'