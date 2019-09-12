var React = require('react')
var django = require('django')
var FlipMove = require('react-flip-move').default
var ChoiceForm = require('./ChoiceForm')
var ErrorList = require('../../../static/ErrorList')

const QuestionForm = (props) => {
  const questionTag = django.gettext('Question')
  const answerTag = django.gettext('Answer')
  const selectAnswerText = django.gettext('Users can select more than one answer.')
  const newChoiceText = django.gettext('Add a new choice')
  const moveUpTag = django.gettext('Move up')
  const moveDownTag = django.gettext('Move down')
  const deleteTag = django.gettext('Delete')
  return (
    <section className="questionform">
      <div className="questionform__content questionform__content--border">
        <div className="form-group">
          <label
            className="questionform__label"
            htmlFor={'id_questions-' + props.id + '-name'}>
            {questionTag}
          </label>
          <textarea
            className="questionform__textarea"
            id={'id_questions-' + props.id + '-name'}
            name={'questions-' + props.id + '-name'}
            value={props.question.label}
            onChange={(e) => { props.onLabelChange(e.target.value) }} />
          <ErrorList errors={props.errors} field="label" />
        </div>

        <label>{answerTag}</label>
        <div className="form-check">
          <label className="form-check__label">
            <input
              type="checkbox"
              id={'id_questions-' + props.id + '-multiple_choice'}
              name={'questions-' + props.id + '-multiple_choice'}
              checked={props.question.multiple_choice}
              onChange={(e) => { props.onMultipleChoiceChange(e.target.checked) }}
            />
            &nbsp;
            {selectAnswerText}
          </label>
        </div>

        <FlipMove easing="cubic-bezier(0.25, 0.5, 0.75, 1)">
          {
            props.question.choices.map((choice, index) => {
              var key = choice.id || choice.key
              var label = django.gettext('Choice') + ` #${index + 1}`
              var errors = props.errors && props.errors.choices
                ? props.errors.choices[index] : {}
              return (
                <div key={key}>
                  <ChoiceForm
                    id={key}
                    label={label}
                    choice={choice}
                    onLabelChange={(label) => { props.onChoiceLabelChange(index, label) }}
                    onDelete={() => { props.onDeleteChoice(index) }}
                    errors={errors}
                  />
                </div>
              )
            })
          }
        </FlipMove>
        <button
          className="btn btn--light btn--small"
          onClick={props.onAppendChoice}
          type="button">
          <i className="fa fa-plus" /> {newChoiceText}
        </button>
      </div>

      <div className="questionform__actions btn-group" role="group">
        <button
          className="btn btn--light btn--small"
          onClick={props.onMoveUp}
          disabled={!props.onMoveUp}
          title={moveUpTag}
          type="button">
          <i className="fa fa-chevron-up"
            aria-label={moveUpTag} />
        </button>
        <button
          className="btn btn--light btn--small"
          onClick={props.onMoveDown}
          disabled={!props.onMoveDown}
          title={moveDownTag}
          type="button">
          <i className="fa fa-chevron-down"
            aria-label={moveDownTag} />
        </button>
        <button
          className="btn btn--light btn--small"
          onClick={props.onDelete}
          title={deleteTag}
          type="button">
          <i className="fas fa-trash-alt"
            aria-label={deleteTag} />
        </button>
      </div>
    </section>
  )
}

module.exports = QuestionForm
