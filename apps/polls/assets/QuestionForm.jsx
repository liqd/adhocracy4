var React = require('react')
var django = require('django')
var FlipMove = require('react-flip-move')
var ChoiceForm = require('./ChoiceForm')

let QuestionForm = React.createClass({
  getInitialState: function () {
    return {}
  },

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
      <section>
        <div className="commenting">
          <div className="commenting__content">
            <div className="form-group">
              <label
                htmlFor={'id_questions-' + this.props.key + '-name'}>
                {django.gettext('Question:')}
              </label>
              <input
                className="form-control"
                id={'id_questions-' + this.props.key + '-name'}
                name={'questions-' + this.props.key + '-name'}
                type="text"
                defaultValue={this.props.question.label}
                onChange={this.handleLabelChange} />
              {this.props.errors && this.props.errors.label
                ? <ul className="errorlist">
                  {this.props.errors.label.map(function (msg, index) {
                    return <li key={msg}>{msg}</li>
                  })}
                </ul>
                : null}
            </div>

            <div className="form-group">
              <FlipMove easing="cubic-bezier(0.25, 0.5, 0.75, 1)">
                {
                  this.props.question.choices.map(function (choice, index) {
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
                  }.bind(this))
                }
              </FlipMove>
              <button
                className="button button--full"
                onClick={this.handleAppendChoice}
                type="button">
                <i className="fa fa-plus" /> {django.gettext('add a new choice')}
              </button>
            </div>
          </div>

          <div className="commenting__actions button-group">
            <button
              className="button"
              onClick={this.handleMoveUp}
              disabled={!this.props.moveQuestionUp}
              type="button">
              <i className="fa fa-chevron-up" />
            </button>
            <button
              className="button"
              onClick={this.handleMoveDown}
              disabled={!this.props.moveQuestionDown}
              type="button">
              <i className="fa fa-chevron-down" />
            </button>
            <button
              className="button"
              onClick={this.handleDelete}
              type="button">
              <i className="fa fa-trash" />
            </button>
          </div>
        </div>
      </section>
    )
  }
})

module.exports = QuestionForm
