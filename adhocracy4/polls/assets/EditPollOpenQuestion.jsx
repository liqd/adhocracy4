import React, { useState } from 'react'
import django from 'django'
import ErrorList from '../../static/ErrorList'
import { HelptextForm } from './HelptextForm'

export const EditPollOpenQuestion = (props) => {
  const [hasHelptext, setHasHelptext] = useState(props.question.help_text)

  return (
    <section className="questionform">
      <div className="questionform__content questionform__content--border">
        <div className="form-group">
          <label
            htmlFor={'id_questions-' + props.id + '-name'}
          >
            {django.gettext('Question')}
            <textarea
              id={'id_questions-' + props.id + '-name'}
              name={'questions-' + props.id + '-name'}
              value={props.question.label}
              onChange={(e) => { props.onLabelChange(e.target.value) }}
            />
          </label>
          <ErrorList errors={props.errors} field="label" />
        </div>
        {hasHelptext
          ? <HelptextForm id={props.id} question={props.question} onHelptextChange={props.onHelptextChange} errors={props.errors} />
          : null}
        <button
          className={`btn btn--small ${hasHelptext ? 'btn--primary' : 'btn--light'}`}
          onClick={() => setHasHelptext(!hasHelptext)}
          type="button"
        >
          <i className={`fa ${hasHelptext ? 'fa-check' : 'fa-plus'}`} /> {django.gettext('Add Helptext')}
        </button>
      </div>

      <div className="questionform__actions btn-group" role="group">
        <button
          className="btn btn--light btn--small"
          onClick={props.onMoveUp}
          disabled={!props.onMoveUp}
          title={django.gettext('Move up')}
          type="button"
        >
          <i
            className="fa fa-chevron-up"
            aria-label={django.gettext('Move up')}
          />
        </button>
        <button
          className="btn btn--light btn--small"
          onClick={props.onMoveDown}
          disabled={!props.onMoveDown}
          title={django.gettext('Move down')}
          type="button"
        >
          <i
            className="fa fa-chevron-down"
            aria-label={django.gettext('Move down')}
          />
        </button>
        <button
          className="btn btn--light btn--small"
          onClick={props.onDelete}
          title={django.gettext('Delete')}
          type="button"
        >
          <i
            className="fas fa-trash-alt"
            aria-label={django.gettext('Delete')}
          />
        </button>
      </div>
    </section>
  )
}
