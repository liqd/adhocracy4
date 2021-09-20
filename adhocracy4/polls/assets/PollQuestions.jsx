import React from 'react'
import { PollQuestion } from './PollQuestion'
import { PollOpenQuestion } from './PollOpenQuestion'
import Alert from '../../static/Alert'
import django from 'django'
import PollResults from './PollResults'

const api = require('adhocracy4').api
const config = require('adhocracy4').config

const ALERT_SUCCESS = {
  type: 'success',
  message: django.gettext('Your answer has been saved.')
}

const ALERT_ERROR = {
  type: 'danger',
  message: django.gettext('Your answer could not be saved due to a server error. Please try again later.')
}

const ALERT_INVALID = {
  type: 'danger',
  message: django.gettext('Your answer is invalid or empty. Please try again.')
}

class PollQuestions extends React.Component {
  constructor (props) {
    super(props)

    this.state = {
      questions: [],
      showResults: false,
      alert: false,
      hasVotes: false,
      errors: {},
      loading: false
    }

    this.linkToPoll = (
      <button type="button" className="btn poll__btn--link" onClick={() => this.handleToggleResultsPage()}>
        {django.gettext('To poll')}
      </button>
    )

    this.linkChangeVote = (
      <button type="button" className="btn poll__btn--link" onClick={() => this.handleToggleResultsPage()}>
        {django.gettext('Change answer')}
      </button>
    )

    this.loadingIndicator = (
      <div className="spinner-border" role="status">
        <span className="visually-hidden">Loading...</span>
      </div>
    )
  }

  setModified (questionId, value) {
    const currQuestion = this.state.questions.find(q => q.id === questionId)
    this.setState({ hasVotes: value })
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

  handleVoteOther (questionId, otherAnswer, otherChoice) {
    this.setState(prevState => {
      const currQuestion = prevState.questions.find(q => q.id === questionId)
      otherChoice && delete this.state.errors[otherChoice.id]
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

  isReadOnly () {
    return this.state.questions.length > 0 && this.state.questions[0].isReadOnly
  }

  removeAlert () {
    this.setState({ alert: false })
  }

  getVoteButton () {
    const isAuthenticated = this.state.questions.length > 0 && this.state.questions[0].authenticated

    if (isAuthenticated) {
      return (
        <button
          type="button"
          className="btn poll__btn--dark a4-spacer--right"
          onClick={(e) => this.handleSubmit(e)}
          disabled={!this.state.hasVotes}
        >
          {this.state.hasUserVote ? django.gettext('Change answer') : django.gettext('Submit answer')}
        </button>
      )
    } else {
      return (
        <a href={config.getLoginUrl()} className="btn poll__btn--dark a4-spacer--right">
          {django.gettext('Please login to answer')}
        </a>
      )
    }
  }

  getLinkShowResultsText () {
    if (this.isReadOnly()) {
      return (
        <span>
          {django.gettext('Show results')}
        </span>
      )
    } else {
      return (
        <span>
          {django.gettext('Show preliminary results')}
        </span>
      )
    }
  }

  linkShowResults () {
    return (
      <button
        type="button"
        className="btn poll__btn--link"
        onClick={() => this.handleToggleResultsPage()}
      >
        {this.getLinkShowResultsText()}
      </button>
    )
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

  sendRequest (datalist) {
    api.poll.batchvote(datalist)
      .then(() => {
        this.getPollData()
        this.setState(prevState => {
          return {
            loading: false,
            alert: ALERT_SUCCESS
          }
        })
      })
      .catch(() => {
        this.setState(prevState => {
          return {
            loading: false,
            alert: ALERT_ERROR
          }
        })
      })
  }

  handleSubmit (e) {
    e.preventDefault()
    this.setState({ loading: true })
    const modifiedQuestions = this.state.questions.filter(q => q.modified)
    const validatedQuestions = modifiedQuestions.filter(q => {
      if (!q.is_open) {
        const otherChoice = q.choices.find(c => c.is_other_choice)
        const otherChoiceSelected = otherChoice && q.userChoices.filter(uc => uc === otherChoice.id).length > 0
        if (otherChoiceSelected) {
          if (!q.other_choice_answer) {
            this.addValidationError(otherChoice.id)
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

    validatedQuestions.length > 0
      ? this.sendRequest(datalist)
      : Object.keys(this.state.errors).length > 0
        ? this.setState({ loading: false, alert: ALERT_SUCCESS })
        : this.setState({ loading: false, alert: ALERT_INVALID })
  }

  getPollData () {
    api.poll.get(this.props.pollId)
      .done(poll => this.setState({
        result: JSON.parse(JSON.stringify(poll.questions)),
        questions: poll.questions,
        showResults: (poll.questions.length > 0 && poll.questions[0].isReadOnly) || poll.has_user_vote,
        hasUserVote: poll.has_user_vote
      }))
  }

  componentDidMount () {
    this.getPollData()
  }

  render () {
    this.buttonVote = this.getVoteButton()
    return this.state.showResults
      ? (
        <div className="pollquestionlist-container">
          {this.state.result.map((q, idx) => (
            <PollResults
              key={idx}
              question={q}
            />
          ))}
          <div className="poll">
            {this.state.hasUserVote ? this.linkChangeVote : this.linkToPoll}
          </div>
        </div>
        )
      : (
        <div className="pollquestionlist-container">
          {this.state.questions.map((q, idx) => (
            q.is_open
              ? (
                <PollOpenQuestion
                  key={idx}
                  question={q}
                  onOpenChange={(questionId, voteData) => this.handleVoteOpen(questionId, voteData)}
                />
                )
              : (
                <PollQuestion
                  key={idx}
                  question={q}
                  onSingleChange={(questionId, voteData) => this.handleVoteSingle(questionId, voteData)}
                  onMultiChange={(questionId, voteData) => this.handleVoteMulti(questionId, voteData)}
                  onOtherChange={(questionId, voteAnswer, otherChoice) => this.handleVoteOther(questionId, voteAnswer, otherChoice)}
                  errors={this.state.errors}
                />
                )
          ))}
          <Alert onClick={() => this.removeAlert()} {...this.state.alert} />
          {!this.isReadOnly()
            ? (
              <div className="poll poll__btn--wrapper">
                {this.buttonVote}{!this.state.loading ? this.linkShowResults() : this.loadingIndicator}
              </div>
              )
            : (
              <div className="poll">
                {!this.state.loading ? this.linkShowResults() : this.loadingIndicator}
              </div>
              )}
        </div>
        )
  }
}

export default PollQuestions
