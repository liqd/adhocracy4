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
      alert: false
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

  handleVoteSingle (questionId, choiceId) {
    this.setState(prevState => {
      const currQuestion = prevState.questions.find(q => q.id === questionId)
      currQuestion.userChoices = [choiceId]
    })
  }

  handleVoteMulti (questionId, choiceId) {
    this.setState(prevState => {
      const currQuestion = prevState.questions.find(q => q.id === questionId)
      const toRemove = currQuestion.userChoices.findIndex(uc => uc === choiceId)
      toRemove !== -1 && currQuestion.userChoices.splice(toRemove, 1)
      toRemove !== -1 || currQuestion.userChoices.push(choiceId)
    })
  }

  handleVoteOther (questionId, otherAnswer) {
    this.setState(prevState => {
      const currQuestion = prevState.questions.find(q => q.id === questionId)
      currQuestion.other_choice_answer = otherAnswer
    })
  }

  handleVoteOpen (questionId, openAnswer) {
    this.setState(prevState => {
      const currQuestion = prevState.questions.find(q => q.id === questionId)
      currQuestion.open_answer = openAnswer
    })
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

  handleSubmit (e) {
    e.preventDefault()
    const modifiedQuestions = this.state.questions.filter(q => q.modified)
    const datalist = []
    for (const question of modifiedQuestions) {
      datalist.push({
        urlReplaces: { questionId: question.id },
        choices: question.userChoices,
        other_choice_answer: question.other_choice_answer || '',
        open_answer: question.open_answer || ''
      })
    }
    modifiedQuestions.length > 0 && api.poll.batchvote(datalist)
      .then(response => {
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
                onOtherChange={(questionId, voteId, voteData) => this.handleVoteOther(questionId, voteId, voteData)}
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
