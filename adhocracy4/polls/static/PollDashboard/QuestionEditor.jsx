import React, { useState } from 'react'
import django from 'django'

import FormFieldError from '../../../static/FormFieldError'
import QuestionImageUploadButton from './QuestionImageUploadButton'

const TRANSLATED = {
  question: django.gettext('Question'),
  questionOfTotal: django.gettext('%(number)s of %(total)s'),
  moveUp: django.gettext('Move question up'),
  moveDown: django.gettext('Move question down'),
  questionLabel: django.gettext('Question'),
  required: django.gettext('This field is required'),
  answerType: django.gettext('Answer type'),
  openText: django.gettext('Open Text'),
  singleChoice: django.gettext('Single choice'),
  multipleChoice: django.gettext('Multiple choice'),
  confidential: django.gettext('Do not display answers publicly'),
  answer: django.pgettext('noun', 'Answer'),
  other: django.gettext('Other'),
  remove: django.gettext('remove'),
  addAnswer: django.gettext('Answer option'),
  addOpenAnswer: django.gettext('Open answer'),
  addExplanation: django.gettext('Explanation'),
  explanation: django.gettext('Explanation')
}

export const QuestionEditor = (props) => {
  const {
    question,
    index,
    total,
    errors,
    questionImagesEnabled,
    onMove
  } = props

  const [hasHelptext, setHasHelptext] = useState(Boolean(question.help_text))
  const hasOtherOption = question.choices.some((choice) => choice.is_other_choice)
  const regularChoices = question.choices.filter((choice) => !choice.is_other_choice)
  const visibleChoices = question.choices

  return (
    <section className="poll-management__editor">
      <header className="poll-management__editor-header">
        <h3 className="poll-management__editor-title">
          {django.interpolate(TRANSLATED.questionOfTotal, { number: index + 1, total }, true)}
        </h3>
        <div className="btn-group poll-management__editor-nav" role="group">
          <button
            type="button"
            className="btn poll-management__nav-button"
            onClick={() => onMove(-1)}
            disabled={index === 0}
            title={TRANSLATED.moveUp}
            aria-label={TRANSLATED.moveUp}
          >
            <i className="fa fa-chevron-up" aria-hidden="true" />
          </button>
          <button
            type="button"
            className="btn poll-management__nav-button"
            onClick={() => onMove(1)}
            disabled={index === total - 1}
            title={TRANSLATED.moveDown}
            aria-label={TRANSLATED.moveDown}
          >
            <i className="fa fa-chevron-down" aria-hidden="true" />
          </button>
        </div>
      </header>

      <div className="form-group">
        <label htmlFor={'id_questions-' + question.key + '-name'}>
          {TRANSLATED.questionLabel}
          <span
            role="presentation"
            title={TRANSLATED.required}
            className="poll-management__required"
          >
            *
          </span>
          {question.id && (
            <span className="editpoll__help-text"> Id: Q{question.id}</span>
          )}
          <textarea
            id={'id_questions-' + question.key + '-name'}
            name={'questions-' + question.key + '-name'}
            value={question.label}
            onChange={(e) => props.onLabelChange(e.target.value)}
            aria-invalid={errors.label ? 'true' : 'false'}
            aria-describedby={errors.label ? 'id_error-' + question.key : undefined}
            required
          />
        </label>
        <FormFieldError id={'id_error-' + question.key} error={errors} field="label" />
      </div>

      {questionImagesEnabled && (
        <QuestionImageUploadButton
          id={question.key}
          question={question}
          onImageChange={props.onImageChange}
          errors={errors}
          helpText={question.image_help_text}
          altText={question.image_alt_text}
          onAltTextChange={props.onAltTextChange}
        />
      )}

      <div className="form-check poll-management__confidential">
        <label
          className="form-check__label"
          htmlFor={'id_questions-' + question.key + '-is_confidential'}
        >
          <input
            type="checkbox"
            id={'id_questions-' + question.key + '-is_confidential'}
            name={'questions-' + question.key + '-is_confidential'}
            checked={question.is_confidential || false}
            onChange={(e) => props.onConfidentialChange(e.target.checked)}
          />
          &nbsp;
          {TRANSLATED.confidential}
        </label>
      </div>

      <fieldset className="poll-management__answer-type form-fieldset">
        <legend>{TRANSLATED.answerType}</legend>
        <div className="poll-management__answer-type-group" role="group">
          <button
            type="button"
            className={'btn poll-management__answer-type-btn' + (question.is_open ? ' poll-management__answer-type-btn--active' : '')}
            onClick={() => props.onOpenChange(true)}
            aria-pressed={question.is_open}
          >
            {TRANSLATED.openText}
          </button>
          <button
            type="button"
            className={'btn poll-management__answer-type-btn' + (!question.is_open && question.multiple_choice ? ' poll-management__answer-type-btn--active' : '')}
            onClick={() => {
              props.onOpenChange(false)
              props.onMultipleChoiceChange(true)
            }}
            aria-pressed={!question.is_open && question.multiple_choice}
          >
            {TRANSLATED.multipleChoice}
          </button>
          <button
            type="button"
            className={'btn poll-management__answer-type-btn' + (!question.is_open && !question.multiple_choice ? ' poll-management__answer-type-btn--active' : '')}
            onClick={() => {
              props.onOpenChange(false)
              props.onMultipleChoiceChange(false)
            }}
            aria-pressed={!question.is_open && !question.multiple_choice}
          >
            {TRANSLATED.singleChoice}
          </button>
        </div>
      </fieldset>

      {!question.is_open && (
        <div className="poll-management__answers">
          <h4 className="poll-management__answers-title">{TRANSLATED.answer}</h4>
          {visibleChoices.map((choice) => {
            const actualIndex = question.choices.indexOf(choice)
            const choiceErrors = errors.choices?.[actualIndex] || {}
            if (choice.is_other_choice) {
              return (
                <div key={choice.key} className="poll-management__choice form-group">
                  <div>
                    {TRANSLATED.other}
                    <span
                      role="presentation"
                      title={TRANSLATED.required}
                      className="poll-management__required"
                    >
                      *
                    </span>
                    {choice.id && (
                      <span className="editpoll__help-text"> Id: A{choice.id}</span>
                    )}
                  </div>
                  <div className="input-group">
                    <input
                      type="text"
                      className="input-group__input"
                      value={TRANSLATED.other}
                      disabled
                      aria-label={TRANSLATED.other}
                    />
                    <span className="input-group__after">
                      <button
                        type="button"
                        className="btn poll-management__choice-delete"
                        onClick={props.onOtherChoiceToggle}
                        title={TRANSLATED.remove}
                      >
                        <i className="fa fa-times" aria-label={TRANSLATED.remove} />
                      </button>
                    </span>
                  </div>
                </div>
              )
            }
            return (
              <div key={choice.key} className="poll-management__choice form-group">
                <label htmlFor={'id_choices-' + choice.key + '-name'}>
                  {TRANSLATED.answer + ' #' + (regularChoices.findIndex((regular) => regular.key === choice.key) + 1)}
                  <span
                    role="presentation"
                    title={TRANSLATED.required}
                    className="poll-management__required"
                  >
                    *
                  </span>
                  {choice.id && (
                    <span className="editpoll__help-text"> Id: A{choice.id}</span>
                  )}
                </label>
                <div className="input-group">
                  <input
                    id={'id_choices-' + choice.key + '-name'}
                    name={'choices-' + choice.key + '-name'}
                    type="text"
                    className="input-group__input"
                    value={choice.label}
                    onChange={(e) => props.onChoiceLabelChange(actualIndex, e.target.value)}
                    aria-invalid={choiceErrors.label ? 'true' : 'false'}
                  />
                  <span className="input-group__after">
                    <button
                      type="button"
                      className="btn poll-management__choice-delete"
                      onClick={() => props.onChoiceDelete(actualIndex)}
                      disabled={question.choices.length < 3}
                      title={TRANSLATED.remove}
                    >
                      <i className="fa fa-times" aria-label={TRANSLATED.remove} />
                    </button>
                  </span>
                </div>
                <FormFieldError
                  id={'id_error-choice-' + choice.key}
                  error={choiceErrors}
                  field="label"
                />
              </div>
            )
          })}

          <div className="poll-management__buttons">
            <button
              type="button"
              className="btn poll-management__btn"
              onClick={props.onChoiceAppend}
            >
              <i className="fa fa-plus" aria-hidden="true" />
              {' '}
              {TRANSLATED.addAnswer}
            </button>
            <button
              type="button"
              className={'btn poll-management__btn' + (hasOtherOption ? ' poll-management__btn--active' : '')}
              onClick={props.onOtherChoiceToggle}
              aria-pressed={hasOtherOption}
            >
              <i className={'fa ' + (hasOtherOption ? 'fa-check' : 'fa-plus')} aria-hidden="true" />
              {' '}
              {TRANSLATED.addOpenAnswer}
            </button>
            <button
              type="button"
              className={'btn poll-management__btn' + (hasHelptext ? ' poll-management__btn--active' : '')}
              onClick={() => setHasHelptext(!hasHelptext)}
              aria-pressed={hasHelptext}
            >
              <i className={'fa ' + (hasHelptext ? 'fa-check' : 'fa-plus')} aria-hidden="true" />
              {' '}
              {TRANSLATED.addExplanation}
            </button>
          </div>
        </div>
      )}

      {question.is_open && (
        <div className="poll-management__buttons">
          <button
            type="button"
            className={'btn poll-management__btn' + (hasHelptext ? ' poll-management__btn--active' : '')}
            onClick={() => setHasHelptext(!hasHelptext)}
            aria-pressed={hasHelptext}
          >
            <i className={'fa ' + (hasHelptext ? 'fa-check' : 'fa-plus')} aria-hidden="true" />
            {' '}
            {TRANSLATED.addExplanation}
          </button>
        </div>
      )}

      {hasHelptext && (
        <div className="form-group poll-management__explanation">
          <label htmlFor={'id_helptext-' + question.key + '-name'}>
            {TRANSLATED.explanation}
            <span
              role="presentation"
              title={TRANSLATED.required}
              className="poll-management__required"
            >
              *
            </span>
            <textarea
              id={'id_helptext-' + question.key + '-name'}
              name={'helptext-' + question.key + '-name'}
              value={question.help_text}
              onChange={(e) => props.onHelpTextChange(e.target.value)}
              aria-invalid={errors.help_text ? 'true' : 'false'}
              aria-describedby={errors.help_text ? 'id_error-help-' + question.key : undefined}
            />
          </label>
          <FormFieldError
            id={'id_error-help-' + question.key}
            error={errors}
            field="help_text"
          />
        </div>
      )}
    </section>
  )
}
