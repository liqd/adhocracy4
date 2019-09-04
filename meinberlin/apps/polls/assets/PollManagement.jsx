var api = require('adhocracy4').api
var React = require('react')
var django = require('django')
var dashboard = require('adhocracy4/adhocracy4/dashboard/assets/dashboard')
var update = require('immutability-helper')
var FlipMove = require('react-flip-move').default
var QuestionForm = require('./QuestionForm')
var Alert = require('../../contrib/assets/Alert')

class PollManagement extends React.Component {
  constructor (props) {
    super(props)
    this.maxLocalKey = 0

    var questions = this.props.poll.questions

    if (questions.length === 0) {
      questions = [
        this.getNewQuestion()
      ]
    }

    this.state = {
      questions: questions,
      errors: [],
      alert: null
    }
  }

  getNextLocalKey () {
    /** Get an artificial key for non-committed items.
     *
     *  The key is prefixed to prevent collisions with real database keys.
     */
    this.maxLocalKey++
    return 'local_' + this.maxLocalKey
  }

  /*
  |--------------------------------------------------------------------------
  | Question state related handlers
  |--------------------------------------------------------------------------
  */

  getNewQuestion (label = '') {
    return {
      label: label,
      multiple_choice: false,
      key: this.getNextLocalKey(),
      choices: [
        this.getNewChoice(),
        this.getNewChoice()
      ]
    }
  }

  handleUpdateQuestionLabel (index, label) {
    var diff = {}
    diff[index] = { $merge: { label: label } }

    this.setState({
      questions: update(this.state.questions, diff)
    })
  }

  handleUpdateMultipleChoice (index, multipleChoice) {
    var diff = {}
    diff[index] = { $merge: { multiple_choice: multipleChoice } }

    this.setState({
      questions: update(this.state.questions, diff)
    })
  }

  handleMoveQuestionUp (index) {
    var question = this.state.questions[index]
    var diff = { $splice: [[index, 1], [index - 1, 0, question]] }

    this.setState({
      questions: update(this.state.questions, diff)
    })
  }

  handleMoveQuestionDown (index) {
    var question = this.state.questions[index]
    var diff = { $splice: [[index, 1], [index + 1, 0, question]] }

    this.setState({
      questions: update(this.state.questions, diff)
    })
  }

  handleAppendQuestion () {
    var newQuestion = this.getNewQuestion()
    var diff = { $push: [newQuestion] }

    this.setState({
      questions: update(this.state.questions, diff)
    }, () => { this.focusOnQuestion(newQuestion) })
  }

  handleDeleteQuestion (index) {
    var diff = { $splice: [[index, 1]] }

    this.setState({
      questions: update(this.state.questions, diff)
    })
  }

  focusOnQuestion (question) {
    const key = question.id || question.key
    const id = 'id_questions-' + key + '-name'
    window.document.getElementById(id).focus()
  }

  /*
  |--------------------------------------------------------------------------
  | Choice state related handlers
  |--------------------------------------------------------------------------
  */

  getNewChoice (label = '') {
    return {
      label: label,
      key: this.getNextLocalKey()
    }
  }

  handleUpdateChoiceLabel (questionIndex, choiceIndex, label) {
    var diff = {}
    diff[questionIndex] = { choices: {} }
    diff[questionIndex].choices[choiceIndex] = { $merge: { label: label } }

    this.setState({
      questions: update(this.state.questions, diff)
    })
  }

  handleAppendChoice (questionIndex) {
    var newChoice = this.getNewChoice()
    var diff = {}
    diff[questionIndex] = { choices: { $push: [newChoice] } }

    this.setState({
      questions: update(this.state.questions, diff)
    }, () => { this.focusOnChoice(newChoice) })
  }

  handleDeleteChoice (questionIndex, choiceIndex) {
    var diff = {}
    diff[questionIndex] = { choices: { $splice: [[choiceIndex, 1]] } }

    this.setState({
      questions: update(this.state.questions, diff)
    })
  }

  focusOnChoice (choice) {
    const key = choice.id || choice.key
    const id = 'id_choices-' + key + '-name'
    window.document.getElementById(id).focus()
  }

  /*
  |--------------------------------------------------------------------------
  | Poll form and submit logic
  |--------------------------------------------------------------------------
  */

  removeAlert () {
    this.setState({
      alert: null
    })
  }

  handleSubmit (e) {
    e.preventDefault()

    const data = {
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
        if (this.props.reloadOnSuccess) {
          dashboard.updateDashboard()
        }
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
  }

  render () {
    return (
      <form onSubmit={this.handleSubmit.bind(this)} onChange={this.removeAlert.bind(this)}>
        <FlipMove easing="cubic-bezier(0.25, 0.5, 0.75, 1)">
          {
            this.state.questions.map((question, index, arr) => {
              var key = question.id || question.key
              var errors = this.state.errors && this.state.errors[index] ? this.state.errors[index] : {}
              return (
                <div key={key}>
                  <QuestionForm
                    id={key}
                    question={question}
                    onLabelChange={(label) => { this.handleUpdateQuestionLabel(index, label) }}
                    onMultipleChoiceChange={(multipleChoice) => { this.handleUpdateMultipleChoice(index, multipleChoice) }}
                    onMoveUp={index !== 0 ? () => { this.handleMoveQuestionUp(index) } : null}
                    onMoveDown={index < arr.length - 1 ? () => { this.handleMoveQuestionDown(index) } : null}
                    onDelete={() => { this.handleDeleteQuestion(index) }}
                    errors={errors}
                    onChoiceLabelChange={(choiceIndex, label) => { this.handleUpdateChoiceLabel(index, choiceIndex, label) }}
                    onDeleteChoice={(choiceIndex) => { this.handleDeleteChoice(index, choiceIndex) }}
                    onAppendChoice={() => { this.handleAppendChoice(index) }}
                  />
                </div>
              )
            })
          }
        </FlipMove>

        <p>
          <button
            className="btn btn--light btn--small"
            onClick={this.handleAppendQuestion.bind(this)}
            type="button"
          >
            <i className="fa fa-plus" /> {django.gettext('Add a new question')}
          </button>
        </p>

        <Alert onClick={this.removeAlert.bind(this)} {...this.state.alert} />

        <button type="submit" className="btn btn--primary">{django.gettext('Save')}</button>
      </form>
    )
  }
}

module.exports = PollManagement
