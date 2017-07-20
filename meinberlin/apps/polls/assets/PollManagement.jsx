var api = require('adhocracy4').api
var React = require('react')
var django = require('django')
var update = require('react-addons-update')
var FlipMove = require('react-flip-move')
var QuestionForm = require('./QuestionForm')
var Alert = require('../../contrib/assets/Alert')

let PollManagement = React.createClass({
  getInitialState: function () {
    var questions = this.props.poll.questions

    if (questions.length === 0) {
      questions = [
        this.getNewQuestion()
      ]
    }

    return {
      questions: questions,
      errors: [],
      alert: null
    }
  },

  maxLocalKey: 0,
  getNextLocalKey: function () {
    /** Get an artificial key for non-committed items.
     *
     *  The key is prefixed to prevent collisions with real database keys.
     */
    this.maxLocalKey++
    return 'local_' + this.maxLocalKey
  },

  /*
  |--------------------------------------------------------------------------
  | Question state related handlers
  |--------------------------------------------------------------------------
  */

  getNewQuestion: function (label = '') {
    return {
      label: label,
      key: this.getNextLocalKey(),
      choices: [
        this.getNewChoice(),
        this.getNewChoice()
      ]
    }
  },

  handleUpdateQuestionLabel: function (index, label) {
    var diff = {}
    diff[index] = {$merge: {label: label}}

    this.setState({
      questions: update(this.state.questions, diff)
    })
  },

  handleMoveQuestionUp: function (index) {
    var question = this.state.questions[index]
    var diff = {$splice: [[index, 1], [index - 1, 0, question]]}

    this.setState({
      questions: update(this.state.questions, diff)
    })
  },

  handleMoveQuestionDown: function (index) {
    var question = this.state.questions[index]
    var diff = {$splice: [[index, 1], [index + 1, 0, question]]}

    this.setState({
      questions: update(this.state.questions, diff)
    })
  },

  handleAppendQuestion: function () {
    var newQuestion = this.getNewQuestion()
    var diff = {$push: [newQuestion]}

    this.setState({
      questions: update(this.state.questions, diff)
    })
  },

  handleDeleteQuestion: function (index) {
    var diff = {$splice: [[index, 1]]}

    this.setState({
      questions: update(this.state.questions, diff)
    })
  },

  /*
  |--------------------------------------------------------------------------
  | Choice state related handlers
  |--------------------------------------------------------------------------
  */

  getNewChoice: function (label = '') {
    return {
      label: label,
      key: this.getNextLocalKey()
    }
  },

  handleUpdateChoiceLabel: function (questionIndex, choiceIndex, label) {
    var diff = {}
    diff[questionIndex] = {choices: {}}
    diff[questionIndex]['choices'][choiceIndex] = {$merge: {label: label}}

    this.setState({
      questions: update(this.state.questions, diff)
    })
  },

  handleAppendChoice: function (questionIndex) {
    var newChoice = this.getNewChoice()
    var diff = {}
    diff[questionIndex] = {choices: {$push: [newChoice]}}

    this.setState({
      questions: update(this.state.questions, diff)
    })
  },

  handleDeleteChoice: function (questionIndex, choiceIndex) {
    var diff = {}
    diff[questionIndex] = {choices: {$splice: [[choiceIndex, 1]]}}

    this.setState({
      questions: update(this.state.questions, diff)
    })
  },

  /*
  |--------------------------------------------------------------------------
  | Poll form and submit logic
  |--------------------------------------------------------------------------
  */

  removeAlert: function () {
    this.setState({
      alert: null
    })
  },

  handleSubmit: function (e) {
    e.preventDefault()

    let data = {
      questions: this.state.questions
    }

    api.poll.change(data, this.props.poll.id)
      .done((data) => {
        this.setState({
          alert: {
            type: 'success',
            message: django.gettext('The poll has been updated.')
          },
          errors: []
        })
      })
      .fail((xhr, status, err) => {
        let errors = []
        if (xhr.responseJSON && 'questions' in xhr.responseJSON) {
          errors = xhr.responseJSON.questions
        }

        this.setState({
          alert: {
            type: 'danger',
            message: django.gettext('The poll could not be updated.')
          },
          errors: errors
        })
      })
  },

  render: function () {
    return (
      <form onSubmit={this.handleSubmit} onChange={this.removeAlert}>
        <FlipMove easing="cubic-bezier(0.25, 0.5, 0.75, 1)">
          {
            this.state.questions.map((question, index) => {
              var key = question.id || question.key
              var errors = this.state.errors && this.state.errors[index] ? this.state.errors[index] : {}
              return (
                <QuestionForm
                  key={key}
                  index={index}
                  question={question}
                  updateQuestionLabel={this.handleUpdateQuestionLabel}
                  moveQuestionUp={index !== 0 ? this.handleMoveQuestionUp : null}
                  moveQuestionDown={index < this.state.questions.length - 1 ? this.handleMoveQuestionDown : null}
                  deleteQuestion={this.handleDeleteQuestion}
                  errors={errors}
                  updateChoiceLabel={this.handleUpdateChoiceLabel}
                  deleteChoice={this.handleDeleteChoice}
                  appendChoice={this.handleAppendChoice}
                />
              )
            })
          }
        </FlipMove>

        <p>
          <button
            className="button button--light button--small"
            onClick={this.handleAppendQuestion}
            type="button">
            <i className="fa fa-plus" /> {django.gettext('Add a new question')}
          </button>
        </p>

        <Alert onClick={this.removeAlert} {...this.state.alert} />

        <button type="submit" className="button button--primary">{django.gettext('Save')}</button>
      </form>
    )
  }
})

module.exports = PollManagement
