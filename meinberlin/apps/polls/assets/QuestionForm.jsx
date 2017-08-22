var React = require('react')
var django = require('django')
var FlipMove = require('react-flip-move')
var ChoiceForm = require('./ChoiceForm')
var ErrorList = require('../../contrib/assets/ErrorList')

class QuestionForm extends React.Component {
  /*
  |--------------------------------------------------------------------------
  | Choice state related handlers
  |--------------------------------------------------------------------------
  */

  handleUpdateChoiceLabel (index, label) {
    this.props.updateChoiceLabel(this.props.index, index, label)
  }
  handleDeleteChoice (index) {
    this.props.deleteChoice(this.props.index, index)
  }

  handleAppendChoice () {
    this.props.appendChoice(this.props.index)
  }

  /*
  |--------------------------------------------------------------------------
  | Question state related handlers
  |--------------------------------------------------------------------------
  */

  handleDelete () {
    this.props.deleteQuestion(this.props.index)
  }

  handleMoveUp () {
    this.props.moveQuestionUp(this.props.index)
  }

  handleMoveDown () {
    this.props.moveQuestionDown(this.props.index)
  }

  handleLabelChange (e) {
    var index = this.props.index
    var label = e.target.value
    this.props.updateQuestionLabel(index, label)
  }

  render () {
    return (
      <section className="commenting">
        <div className="commenting__content commenting__content--border">
          <div className="form-group">
            <label
              htmlFor={'id_questions-' + this.props.key + '-name'}>
              {django.gettext('Question')}
            </label>
            <textarea
              id={'id_questions-' + this.props.key + '-name'}
              name={'questions-' + this.props.key + '-name'}
              value={this.props.question.label}
              onChange={this.handleLabelChange.bind(this)} />
            <ErrorList errors={this.props.errors} field="label" />
          </div>

          <FlipMove easing="cubic-bezier(0.25, 0.5, 0.75, 1)">
            {
              this.props.question.choices.map((choice, index) => {
                var key = choice.id || choice.key
                var errors = this.props.errors && this.props.errors.choices
                  ? this.props.errors.choices[index] : {}
                return (
                  <ChoiceForm
                    key={key}
                    index={index}
                    choice={choice}
                    updateChoiceLabel={this.handleUpdateChoiceLabel.bind(this)}
                    deleteChoice={this.handleDeleteChoice.bind(this)}
                    errors={errors}
                  />
                )
              })
            }
          </FlipMove>
          <button
            className="btn btn--light btn--small"
            onClick={this.handleAppendChoice.bind(this)}
            type="button">
            <i className="fa fa-plus" /> {django.gettext('Add a new choice')}
          </button>
        </div>

        <div className="commenting__actions btn-group">
          <button
            className="btn btn--light btn--small"
            onClick={this.handleMoveUp.bind(this)}
            disabled={!this.props.moveQuestionUp}
            title={django.gettext('Move up')}
            type="button">
            <i className="fa fa-chevron-up"
              aria-label={django.gettext('Move up')} />
          </button>
          <button
            className="btn btn--light btn--small"
            onClick={this.handleMoveDown.bind(this)}
            disabled={!this.props.moveQuestionDown}
            title={django.gettext('Move down')}
            type="button">
            <i className="fa fa-chevron-down"
              aria-label={django.gettext('Move down')} />
          </button>
          <button
            className="btn btn--light btn--small"
            onClick={this.handleDelete.bind(this)}
            title={django.gettext('Delete')}
            type="button">
            <i className="fa fa-trash"
              aria-label={django.gettext('Delete')} />
          </button>
        </div>
      </section>
    )
  }
}

module.exports = QuestionForm
