import React, { useState } from 'react'
import { EditPollChoice } from './EditPollChoice'
import django from 'django'
import FormFieldError from '../../../static/FormFieldError'
import { HelptextForm } from './HelptextForm'

const FlipMove = require('react-flip-move').default

export const EditPollQuestion = (props) => {
  const [hasHelptext, setHasHelptext] = useState(props.question.help_text)
  const hasOtherOption = props.question.choices.find(c => c.is_other_choice)
  return (
    <section className="editpoll__question-container">
      <div className="editpoll__question">
        <div className="form-group editpoll__question--border">
          <label
            htmlFor={'id_questions-' + props.id + '-name'}
          >
            {django.gettext('Question')}
            {props.question.id &&
              <span className="editpoll__help-text"> Id: Q{props.question.id}</span>}
            <textarea
              id={'id_questions-' + props.id + '-name'}
              name={'questions-' + props.id + '-name'}
              value={props.question.label}
              onChange={(e) => { props.onLabelChange(e.target.value) }}
              aria-invalid={props.errors ? 'true' : 'false'}
              aria-describedby={props.errors && 'id_error-' + props.id}
            />
            <FormFieldError id={'id_error-' + props.id} error={props.errors} field="label" />
          </label>

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
              {django.gettext('Participants can vote for more than one option (multiple choice)')}
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
              {django.gettext('Participants can add their own answer')}
            </label>
          </div>

          <FlipMove easing="cubic-bezier(0.25, 0.5, 0.75, 1)">
            {
              props.question.choices.map((choice, index) => {
                const key = choice.id || choice.key
                const label = django.pgettext('noun', 'Answer') + ' #' + (index + 1)
                const errors = props.errors && props.errors.choices
                  ? props.errors.choices[index]
                  : {}
                return !choice.is_other_choice
                  ? (
                    <div key={key}>
                      <EditPollChoice
                        id={'id_questions-poll' + props.id + '-multiple_choice'}
                        index={index + 1}
                        label={label}
                        choice={choice}
                        choiceId={choice.id}
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
                        id={'id_questions-poll' + props.id + '-is_other_choice'}
                        index={index + 1}
                        label={django.gettext('Other')}
                        choice={{ label: django.gettext('Other') }}
                        choiceId={choice.id}
                        onDelete={() => props.onHasOtherChoiceChange(false)}
                        undeletable={props.question.choices.length < 3}
                        isOther
                      />
                    </div>
                    )
              })
            }
          </FlipMove>
          <div className="editpoll__btns--question">
            <button
              className="btn editpoll__btn--question"
              onClick={() => props.onAppendChoice(hasOtherOption)}
              type="button"
            >
              <i className="fa fa-plus" /> {django.gettext('New answer')}
            </button>
            <button
              className={'btn ' + (hasHelptext ? 'editpoll__btn--dark' : 'editpoll__btn--question')}
              onClick={() => setHasHelptext(!hasHelptext)}
              type="button"
            >
              <i className={'fa ' + (hasHelptext ? 'fa-check' : 'fa-plus')} /> {django.gettext('Explanation')}
            </button>
          </div>
        </div>
      </div>

      <div className="editpoll__question-actions btn-group" role="group">
        <button
          className="btn poll__btn--light"
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
          className="btn poll__btn--light"
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
          className="btn poll__btn--light"
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
