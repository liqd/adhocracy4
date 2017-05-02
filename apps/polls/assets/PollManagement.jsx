var React = require('react')
var django = require('django')
var update = require('react-addons-update')
var FlipMove = require('react-flip-move')
var QuestionForm = require('./QuestionForm')

var $ = require('jquery')

let PollManagement = React.createClass({
  getInitialState: function () {
    return {
      questions: this.props.poll.questions,
      errors: [],
      successMessage: '',
      maxQuestionKey: 0,
      maxChoiceKey: 0
    }
  },

  /*
  |--------------------------------------------------------------------------
  | Question state related handlers
  |--------------------------------------------------------------------------
  */

  getNextQuestionKey: function () {
    /** Get an artifical key for non-commited questions.
     *
     *  Prefix to prevent collisions with real database keys;
     */
    var questionKey = 'local_' + (this.state.maxQuestionKey + 1)
    this.setState({maxQuestionKey: this.state.maxQuestionKey + 1})
    return questionKey
  },

  getNewQuestion: function (label) {
    var newQuestion = {}
    newQuestion['label'] = label
    newQuestion['key'] = this.getNextQuestionKey()
    newQuestion['choices'] = []
    return newQuestion
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
    var newQuestion = this.getNewQuestion('')
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

  getNextChoiceKey: function () {
    /** Get an artifical key for non-commited choices.
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

  handleUpdateChoiceLabel: function (questionIndex, choiceIndex, label) {
    var diff = {}
    diff[questionIndex] = {choices: {}}
    diff[questionIndex]['choices'][choiceIndex] = {$merge: {label: label}}

    this.setState({
      questions: update(this.state.questions, diff)
    })
  },

  handleAppendChoice: function (questionIndex) {
    var newChoice = this.getNewChoice('')
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

  handleSubmit: function (e) {
    e.preventDefault()

    var baseURL = '/api/'
    var url = baseURL + 'modules/$moduleId/polls/'

    var urlReplaces = {moduleId: this.props.module}

    url = url.replace(/\$(\w+?)\b/g, (match, group) => {
      return urlReplaces[group]
    })

    url = url + this.props.poll.id + '/'

    var data = {
      id: this.props.poll.id,
      questions: this.state.questions
    }

    var $body = $('body')

    var params = {
      url: url,
      type: 'PUT',
      contentType: 'application/json; charset=utf-8',
      dataType: 'json',
      data: JSON.stringify(data),
      error: function (xhr, status, err) {
        console.error(url, status, err.toString())
      },
      complete: function () {
        $body.removeClass('loading')
      }
    }

    $body.addClass('loading')
    var promise = $.ajax(params)

    promise
      .done(function (data) {
        this.setState({
          successMessage: django.gettext('The poll has been updated.')
        })

        setTimeout(function () {
          this.setState({
            successMessage: ''
          })
        }.bind(this), 1500)
      }.bind(this))
      .fail(function (xhr, status, err) {
        this.setState({
          errors: xhr.responseJSON.questions || []
        })
      }.bind(this))
  },

  render: function () {
    return (
      <form onSubmit={this.handleSubmit}>
        { this.state.successMessage
          ? <p className="alert alert-success ">
            {this.state.successMessage}
          </p> : null
        }

        <FlipMove easing="cubic-bezier(0.25, 0.5, 0.75, 1)">
          {
            this.state.questions.map(function (question, index) {
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
            }.bind(this))
          }
        </FlipMove>

        <button
          className="button button--full"
          onClick={this.handleAppendQuestion}
          type="button">
          <i className="fa fa-plus" /> {django.gettext('add a new quesion')}
        </button>

        { this.state.successMessage
          ? <p className="alert alert-success ">
            {this.state.successMessage}
          </p> : null
        }

        <button type="submit" className="button button--primary">{django.gettext('save')}</button>
      </form>
    )
  }
})

module.exports = PollManagement
