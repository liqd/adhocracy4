import React, { useState } from 'react'
import { EditPollChoice } from './EditPollChoice'
import django from 'django'
import ErrorList from '../../static/ErrorList'
import { HelptextForm } from './HelptextForm'

const FlipMove = require('react-flip-move').default

export const EditPollQuestion = (props) => {
  const [hasHelptext, setHasHelptext] = useState(props.question.help_text)
  const hasOtherOption = props.question.choices.find(c => c.is_other_choice)
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

        <div className="form-check">
          <label className="form-check__label" htmlFor={'id_questions-' + props.id + '-multiple_choice'}>
            <input
              type="checkbox"
              id={'id_questions-' + props.id + '-multiple_choice'}
              name={'questions-' + props.id + '-multiple_choice'}
              checked={props.question.multiple_choice}
              onChange={(e) => { props.onMultipleChoiceChange(e.target.checked) }}
            />
            &nbsp;
            {django.gettext('Users can select more than one answer.')}
          </label>
        </div>

        <div className="form-check">
          <label className="form-check__label" htmlFor={'id_questions-' + props.id + '-is_other_choice'}>
            <input
              type="checkbox"
              id={'id_questions-' + props.id + '-is_other_choice'}
              name={'questions-' + props.id + '-is_other_choice'}
              checked={hasOtherOption || false}
              onChange={(e) => { props.onHasOtherChoiceChange(e.target.checked) }}
              disabled={props.question.choices.length < 3 && hasOtherOption}
            />
            &nbsp;
            {django.gettext('Users can answer openly.')}
          </label>
        </div>

        <FlipMove easing="cubic-bezier(0.25, 0.5, 0.75, 1)">
          {
            props.question.choices.map((choice, index) => {
              const key = choice.id || choice.key
              const label = django.gettext('Choice') + ` #${index + 1}`
              const errors = props.errors && props.errors.choices
                ? props.errors.choices[index]
                : {}
              return !choice.is_other_choice
                ? (
                  <div key={key}>
                    <EditPollChoice
                      id={key}
                      label={label}
                      choice={choice}
                      onLabelChange={(label) => { props.onChoiceLabelChange(index, label) }}
                      onDelete={() => { props.onDeleteChoice(index) }}
                      errors={errors}
                      undeletable={props.question.choices.length < 3}
                    />
                  </div>
                )
                : (
                  <div key={key}>
                    <EditPollChoice
                      id={key}
                      label={django.gettext('Other')}
                      choice={{ label: django.gettext('Other') }}
                      onDelete={() => props.onHasOtherChoiceChange(false)}
                      undeletable={props.question.choices.length < 3}
                      isOther
                    />
                  </div>
                )
            })
          }
        </FlipMove>
        <div className="questionform-buttons-container">
          <button
            className="btn btn--light btn--small questionform-button-wrapper"
            onClick={() => props.onAppendChoice(hasOtherOption)}
            type="button"
          >
            <i className="fa fa-plus" /> {django.gettext('Add a new choice')}
          </button>
          <button
            className={`questionform-button-wrapper btn btn--small ${hasHelptext ? 'btn--primary' : 'btn--light'}`}
            onClick={() => setHasHelptext(!hasHelptext)}
            type="button"
          >
            <i className={`fa ${hasHelptext ? 'fa-check' : 'fa-plus'}`} /> {django.gettext('Add Helptext')}
          </button>
        </div>
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
