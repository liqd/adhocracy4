var React = require('react')
var django = require('django')
var FlipMove = require('react-flip-move')
var ChoiceForm = require('./ChoiceForm')
var ErrorList = require('../../contrib/static/js/ErrorList')

let QuestionForm = React.createClass({
  /*
  |--------------------------------------------------------------------------
  | Choice state related handlers
  |--------------------------------------------------------------------------
  */

  handleUpdateChoiceLabel: function (index, label) {
    this.props.updateChoiceLabel(this.props.index, index, label)
  },
  handleDeleteChoice: function (index) {
    this.props.deleteChoice(this.props.index, index)
  },

  handleAppendChoice: function () {
    this.props.appendChoice(this.props.index)
  },

  /*
  |--------------------------------------------------------------------------
  | Question state related handlers
  |--------------------------------------------------------------------------
  */

  handleDelete: function () {
    this.props.deleteQuestion(this.props.index)
  },

  handleMoveUp: function () {
    this.props.moveQuestionUp(this.props.index)
  },

  handleMoveDown: function () {
    this.props.moveQuestionDown(this.props.index)
  },

  handleLabelChange: function (e) {
    var index = this.props.index
    var label = e.target.value
    this.props.updateQuestionLabel(index, label)
  },

  render: function () {
    return (
      <section className="commenting">
        <div className="commenting__content commenting__content--border">
          <div className="form-group">
            <label
              htmlFor={'id_questions-' + this.props.key + '-name'}>
              {django.gettext('Question:')}
            </label>
            <textarea
              id={'id_questions-' + this.props.key + '-name'}
              name={'questions-' + this.props.key + '-name'}
              defaultValue={this.props.question.label}
              onChange={this.handleLabelChange} />
            <ErrorList errors={this.props.errors} />
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
                    updateChoiceLabel={this.handleUpdateChoiceLabel}
                    deleteChoice={this.handleDeleteChoice}
                    errors={errors}
                  />
                )
              })
            }
          </FlipMove>
          <button
            className="button button--light"
            onClick={this.handleAppendChoice}
            type="button">
            <i className="fa fa-plus" /> {django.gettext('add a new choice')}
          </button>
        </div>

        <div className="commenting__actions button-group">
          <button
            className="button button--light"
            onClick={this.handleMoveUp}
            disabled={!this.props.moveQuestionUp}
            type="button">
            <i className="fa fa-chevron-up" />
          </button>
          <button
            className="button button--light"
            onClick={this.handleMoveDown}
            disabled={!this.props.moveQuestionDown}
            type="button">
            <i className="fa fa-chevron-down" />
          </button>
          <button
            className="button button--light"
            onClick={this.handleDelete}
            type="button">
            <i className="fa fa-trash" />
          </button>
        </div>
      </section>
    )
  }
})

module.exports = QuestionForm
