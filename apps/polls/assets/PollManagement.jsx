var React = require('react')
var django = require('django')
var update = require('react-addons-update')
var FlipMove = require('react-flip-move')
var QuestionForm = require('./QuestionForm')

let PollManagement = React.createClass({
  getInitialState: function () {
    return {
      questions: this.props.poll.questions,
      questionErrors: {},
      successMessage: '',
      maxQuestionKey: 0
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
    var questions = update(this.state.questions, {
      $splice: [[index, 1], [index - 1, 0, question]]
    })
    this.setState({
      questions: questions
    })
  },

  handleMoveQuestionDown: function (index) {
    var question = this.state.questions[index]
    var questions = update(this.state.questions, {
      $splice: [[index, 1], [index + 1, 0, question]]
    })
    this.setState({
      questions: questions
    })
  },

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

  handleAppendQuestion: function () {
    var newQuestion = this.getNewQuestion('')
    var newQuestions = update(this.state.questions, {$push: [newQuestion]})
    this.setState({
      questions: newQuestions
    })
  },

  handleDeleteQuestion: function (index) {
    var newArray = update(this.state.questions, {$splice: [[index, 1]]})
    this.setState({
      questions: newArray
    })
  },

  getQuestionErrors: function (key) {
    // Props or State?
    return this.state.questionErrors[key]
  },

  render: function () {
    return (
      <form onSubmit={this.submitDocument}>
        { this.state.successMessage
          ? <p className="alert alert-success ">
            {this.state.successMessage}
          </p> : null
        }

        <FlipMove easing="cubic-bezier(0.25, 0.5, 0.75, 1)">
          {
            this.state.questions.map(function (question, index) {
              var key = question.id || question.key
              return (
                <QuestionForm
                  key={key}
                  index={index}
                  question={question}
                  updateQuestionLabel={this.handleUpdateQuestionLabel}
                  moveQuestionUp={index !== 0 ? this.handleMoveQuestionUp : null}
                  moveQuestionDown={index < this.state.questions.length - 1 ? this.handleMoveQuestionDown : null}
                  deleteQuestion={this.handleDeleteQuestion}
                  errors={this.getQuestionErrors(key)}
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
