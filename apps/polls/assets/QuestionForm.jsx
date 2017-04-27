var React = require('react')
var django = require('django')
var update = require('react-addons-update')
var FlipMove = require('react-flip-move')
var ChoiceForm = require('./ChoiceForm')

let QuestionForm = React.createClass({
  getInitialState: function () {
    return {
      choices: this.props.question.choices,
      choiceErrors: {},
      maxChoiceKey: 0
    }
  },
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

  handleUpdateChoiceLabel: function (index, label) {
    var diff = {}
    diff[index] = {$merge: {label: label}}
    this.setState({
      choices: update(this.state.choices, diff)
    })
  },
  handleDeleteChoice: function (index) {
    var newArray = update(this.state.choices, {$splice: [[index, 1]]})
    this.setState({
      choices: newArray
    })
  },

  getNextChoiceKey: function () {
    /** Get an artifical key for non-commited questions.
     *
     *  Prefix to prevent collisions with real database keys;
     */
    var choiceKey = 'local_' + (this.state.maxChoiceKey + 1)
    this.setState({maxChoiceKey: this.state.maxChoiceKey + 1})
    return choiceKey
  },

  getNewChoice: function (label) {
    var newChoice = {}
    newChoice['label'] = label
    newChoice['key'] = this.getNextChoiceKey()
    return newChoice
  },

  handleAppendChoice: function () {
    var newChoice = this.getNewChoice('')
    var newChoices = update(this.state.choices, {$push: [newChoice]})
    this.setState({
      choices: newChoices
    })
  },

  getChoiceErrors: function (key) {
    // Props or State?
    return this.state.choiceErrors[key]
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
              {this.props.errors && this.props.errors.name
                ? <ul className="errorlist">
                  {this.props.errors.name.map(function (msg, index) {
                    return <li key={msg}>{msg}</li>
                  })}
                </ul>
                : null}
            </div>

            <div className="form-group">
              <FlipMove easing="cubic-bezier(0.25, 0.5, 0.75, 1)">
                {
                  this.state.choices.map(function (choice, index) {
                    var key = choice.id || choice.key
                    return (
                      <ChoiceForm
                        key={key}
                        index={index}
                        choice={choice}
                        updateChoiceLabel={this.handleUpdateChoiceLabel}
                        deleteChoice={this.handleDeleteChoice}
                        errors={this.getChoiceErrors(key)}
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
