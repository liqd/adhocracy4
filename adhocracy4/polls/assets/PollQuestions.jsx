import React from 'react'
import { PollQuestion } from './PollQuestion'
import { PollOpenQuestion } from './PollOpenQuestion'
import Alert from '../../static/Alert'
import django from 'django'
import PollResults from './PollResults'

const api = require('adhocracy4').api
const config = require('adhocracy4').config

class PollQuestions extends React.Component {
  constructor (props) {
    super(props)

    this.state = {
      questions: [],
      showResults: false,
      alert: false,
      votes: [],
      errors: {}
    }

    this.linkToPoll = (
      <button type="button" className="btn btn--link" onClick={() => this.handleToggleResultsPage()}>
        {django.gettext('To poll')}
      </button>
    )

    this.linkChangeVote = (
      <button type="button" className="btn btn--link" onClick={() => this.handleToggleResultsPage()}>
        {django.gettext('Change vote')}
      </button>)

    this.linkShowResults = (
      <button type="button" className="btn btn--link" onClick={() => this.handleToggleResultsPage()}>
        {django.gettext('Show preliminary results')}
      </button>
    )
  }

  setModified (questionId, value) {
    const currQuestion = this.state.questions.find(q => q.id === questionId)
    currQuestion.modified = value
  }

  handleVoteSingle (questionId, choiceId) {
    this.setState(prevState => {
      const currQuestion = prevState.questions.find(q => q.id === questionId)
      currQuestion.userChoices = [choiceId]
    })
    this.setModified(questionId, true)
  }

  handleVoteMulti (questionId, choiceId) {
    this.setState(prevState => {
      const currQuestion = prevState.questions.find(q => q.id === questionId)
      const toRemove = currQuestion.userChoices.findIndex(uc => uc === choiceId)
      toRemove !== -1 && currQuestion.userChoices.splice(toRemove, 1)
      toRemove !== -1 || currQuestion.userChoices.push(choiceId)
    })
    this.setModified(questionId, true)
  }

  handleVoteOther (questionId, otherAnswer) {
    this.setState(prevState => {
      const currQuestion = prevState.questions.find(q => q.id === questionId)
      currQuestion.other_choice_answer = otherAnswer
    })
    this.setModified(questionId, true)
  }

  handleVoteOpen (questionId, openAnswer) {
    this.setState(prevState => {
      const currQuestion = prevState.questions.find(q => q.id === questionId)
      currQuestion.open_answer = openAnswer
    })
    this.setModified(questionId, true)
  }

  handleToggleResultsPage () {
    this.setState(prevState => ({ showResults: !prevState.showResults }))
  }

  hasAnyVotes () {
    return this.state.votes.length > 0
  }

  isReadOnly () {
    return this.state.questions.length > 0 && this.state.questions[0].isReadOnly
  }

  removeAlert () {
    this.setState({ alert: false })
  }

  getVoteButton () {
    const isAuthenticated = this.state.questions.length > 0 && this.state.questions[0].authenticated

    if (isAuthenticated) {
      const disabled = this.hasAnyVotes()
      return (
        <button
          type="button"
          className="btn btn--primary u-spacer-right"
          onClick={(e) => this.handleSubmit(e)}
          disabled={disabled}
        >
          {django.gettext('Vote')}
        </button>
      )
    } else {
      return (
        <a href={config.getLoginUrl()} className="btn btn--primary u-spacer-right">
          {django.gettext('Please login to vote')}
        </a>
      )
    }
  }

  addValidationError (choiceId) {
    this.setState(prevState => {
      const newErrors = { ...prevState.errors }
      newErrors[choiceId] = [django.gettext('Please enter your answer in this field.')]
      return {
        ...prevState,
        errors: { ...newErrors }
      }
    })
  }

  removeValidationError (choiceId) {
    this.setState(prevState => {
      const newErrors = { ...prevState.errors }
      newErrors[choiceId] && delete newErrors[choiceId]
      return {
        ...prevState,
        errors: { ...newErrors }
      }
    })
  }

  handleSubmit (e) {
    e.preventDefault()
    const modifiedQuestions = this.state.questions.filter(q => q.modified)
    const validatedQuestions = modifiedQuestions.filter(q => {
      if (!q.is_open) {
        const otherChoice = q.choices.find(c => c.is_other_choice)
        const otherChoiceSelected = otherChoice && q.userChoices.filter(uc => uc === otherChoice.id).length > 0
        if (otherChoiceSelected) {
          if (!q.other_choice_answer) {
            this.addValidationError(otherChoice.id)
            return
          } else {
            this.removeValidationError(otherChoice.id)
            return q
          }
        }
      }
      return q
    })

    const datalist = []
    for (const question of validatedQuestions) {
      datalist.push({
        urlReplaces: { questionId: question.id },
        choices: question.userChoices,
        other_choice_answer: question.other_choice_answer || '',
        open_answer: question.open_answer || ''
      })
    }

    validatedQuestions.length > 0 && api.poll.batchvote(datalist)
      .then(response => {
        this.setModified(response[0].question.id, false)
        this.setState({
          alert: {
            type: 'success',
            message: django.gettext('Vote counted')
          }
        })
      })
      .catch(() => {
        this.setState({
          alert: {
            type: 'danger',
            message: django.gettext('Vote has not been counted due to a server error.')
          }
        })
      })
  }

  componentDidMount () {
    api.poll.get(this.props.pollId)
      .done(r => this.setState({ questions: r.questions }))
  }

  render () {
    this.buttonVote = this.getVoteButton()
    return this.state.showResults ? (
      <div className="pollquestionlist-container">
        {this.state.questions.map((q, idx) => (
          <PollResults
            key={idx}
            question={q}
          />
        ))}
      </div>
    ) : (
      <div className="pollquestionlist-container">
        <div className="u-border">
          {this.state.questions.map((q, idx) => (
            q.is_open ? (
              <PollOpenQuestion
                key={idx}
                question={q}
                onOpenChange={(questionId, voteData) => this.handleVoteOpen(questionId, voteData)}
              />
            ) : (
              <PollQuestion
                key={idx}
                question={q}
                onSingleChange={(questionId, voteData) => this.handleVoteSingle(questionId, voteData)}
                onMultiChange={(questionId, voteData) => this.handleVoteMulti(questionId, voteData)}
                onOtherChange={(questionId, voteAnswer) => this.handleVoteOther(questionId, voteAnswer)}
                errors={this.state.errors}
              />
            )
          ))}
          <Alert onClick={() => this.removeAlert()} {...this.state.alert} />
          {!this.isReadOnly() && (
            <div className="poll">
              {this.buttonVote}{this.linkShowResults}
            </div>
          )}
        </div>
      </div>
    )
  }
}

export default PollQuestions
