import React from 'react'
import django from 'django'

import { PollChoice } from './PollChoice'
import { PollOpenQuestion } from './PollOpenQuestion'
import PollResults from './PollResults'

import Alert from '../../../static/Alert'
import api from '../../../static/api'
import Captcha from '../../../static/Captcha'
import config from '../../../static/config'
import { TermsOfUseCheckbox } from '../../../static/TermsOfUseCheckbox'

const ALERT_SUCCESS = {
  alertAttribute: 'polite',
  type: 'success',
  message: django.gettext('Your answer has been saved.')
}

const ALERT_ERROR = {
  alertAttribute: 'assertive',
  type: 'danger',
  message: django.gettext(
    'Your answer could not be saved. Please check the data you entered again.'
  )
}

const ALERT_INVALID = {
  alertAttribute: 'assertive',
  type: 'danger',
  message: django.gettext('Your answer is invalid or empty. Please try again.')
}

class PollQuestions extends React.Component {
  constructor (props) {
    super(props)

    this.state = {
      questions: [],
      captcha: '',
      showResults: false,
      allowUnregisteredUsers: false,
      alert: false,
      hasVotes: false,
      errors: {},
      loading: false,
      loadingPage: true,
      refreshCaptcha: true
    }

    this.handleTermsOfUse = this.handleTermsOfUse.bind(this)

    this.linkToPoll = (
      <button
        type="button"
        className="btn poll__btn--link"
        onClick={() => {
          this.handleToggleResultsPage()
          this.removeAlert()
        }}
      >
        {django.gettext('To poll')}
      </button>
    )

    this.linkChangeVote = (
      <button
        type="button"
        className="btn poll__btn--link"
        onClick={() => {
          this.handleToggleResultsPage()
          this.removeAlert()
        }}
      >
        {django.gettext('Change answer')}
      </button>
    )

    this.loadingIndicator = (
      <div className="u-spinner__container">
        <i className="fa fa-spinner fa-pulse" aria-hidden="true" />
        <span className="visually-hidden">Loading...</span>
      </div>
    )
  }

  setModified (questionId, value) {
    const currentQuestion = this.state.questions.find(
      (question) => question.id === questionId
    )
    this.setState({ hasVotes: value })
    currentQuestion.modified = value
  }

  handleVoteSingle (questionId, choiceId) {
    this.setState((prevState) => {
      const currentQuestion = prevState.questions.find(
        (question) => question.id === questionId
      )
      currentQuestion.userChoices = [choiceId]
    })
    this.setModified(questionId, true)
  }

  handleVoteMulti (questionId, choiceId) {
    this.setState((prevState) => {
      const currentQuestion = prevState.questions.find(
        (question) => question.id === questionId
      )
      const toRemove = currentQuestion.userChoices.findIndex(
        (userChoice) => userChoice === choiceId
      )
      toRemove !== -1 && currentQuestion.userChoices.splice(toRemove, 1)
      toRemove !== -1 || currentQuestion.userChoices.push(choiceId)
    })
    this.setModified(questionId, true)
  }

  handleVoteOther (questionId, otherAnswer, otherChoice) {
    this.setState((prevState) => {
      const currentQuestion = prevState.questions.find(
        (question) => question.id === questionId
      )
      otherChoice && delete this.state.errors[otherChoice.id]
      currentQuestion.other_choice_answer = otherAnswer
    })
    this.setModified(questionId, true)
  }

  handleVoteOpen (questionId, openAnswer) {
    this.setState((prevState) => {
      const currentQuestion = prevState.questions.find(
        (question) => question.id === questionId
      )
      currentQuestion.open_answer = openAnswer
    })
    this.setModified(questionId, true)
  }

  handleToggleResultsPage () {
    this.setState((prevState) => ({ showResults: !prevState.showResults }))
  }

  isReadOnly () {
    return this.state.questions.length > 0 && this.state.questions[0].isReadOnly
  }

  removeAlert () {
    this.setState({ alert: false })
  }

  getVoteButton () {
    const isAuthenticated =
      this.state.questions.length > 0 &&
      (this.state.questions[0].authenticated ||
        this.state.allowUnregisteredUsers)

    if (isAuthenticated) {
      return (
        <button
          type="button"
          className="btn poll__btn--dark a4-spacer--right"
          onClick={(e) => this.handleSubmit(e)}
          disabled={
            !this.state.hasVotes ||
            (this.state.allowUnregisteredUsers &&
              !this.state.questions[0].authenticated &&
              this.state.captcha === '') ||
            (this.state.useTermsOfUse &&
              !this.state.agreedTermsOfUse &&
              !this.state.checkedTermsOfUse)
          }
        >
          {this.state.hasUserVote
            ? django.gettext('Change answer')
            : django.gettext('Submit answer')}
        </button>
      )
    } else {
      return (
        <a
          href={config.getLoginUrl()}
          className="btn poll__btn--dark a4-spacer--right"
        >
          {django.gettext('Please login to answer')}
        </a>
      )
    }
  }

  getLinkShowResultsText () {
    if (this.isReadOnly()) {
      return <span>{django.gettext('Show results')}</span>
    } else {
      return <span>{django.gettext('Show preliminary results')}</span>
    }
  }

  linkShowResults () {
    return (
      <button
        type="button"
        className="btn poll__btn--link"
        onClick={() => {
          this.handleToggleResultsPage()
          this.removeAlert()
        }}
      >
        {this.getLinkShowResultsText()}
      </button>
    )
  }

  addValidationError (choiceId) {
    this.setState((prevState) => {
      const newErrors = { ...prevState.errors }
      newErrors[choiceId] = [
        django.gettext('Please enter your answer in this field.')
      ]
      return {
        ...prevState,
        errors: { ...newErrors }
      }
    })
  }

  removeValidationError (choiceId) {
    this.setState((prevState) => {
      const newErrors = { ...prevState.errors }
      newErrors[choiceId] && delete newErrors[choiceId]
      return {
        ...prevState,
        errors: { ...newErrors }
      }
    })
  }

  handleTermsOfUse () {
    if (!this.state.agreedTermsOfUse) {
      this.setState({ agreedTermsOfUse: true })
    }
  }

  updateAgreedTOS () {
    if (!this.state.agreedTermsOfUse) {
      this.setState({ agreedTermsOfUse: true })
      const event = new Event('agreedTos')
      dispatchEvent(event)
    }
  }

  sendRequest (data) {
    api.poll
      .vote(data)
      .then((poll) => {
        this.setState((prevState) => {
          return {
            result: JSON.parse(JSON.stringify(poll.questions)),
            questions: poll.questions,
            showResults:
              (poll.questions.length > 0 && poll.questions[0].isReadOnly) ||
              poll.has_user_vote,
            hasUserVote: poll.has_user_vote,
            useTermsOfUse: poll.use_org_terms_of_use,
            agreedTermsOfUse: poll.user_has_agreed,
            orgTermsUrl: poll.org_terms_url,
            loadingPage: false,
            loading: false,
            alert: ALERT_SUCCESS
          }
        })
        return null
      })
      .catch(() => {
        this.setState((prevState) => {
          return {
            loading: false,
            alert: ALERT_ERROR,
            agreedTermsOfUse: prevState.agreedTermsOfUse && prevState.questions.length > 0 && prevState.questions[0].authenticated,
            refreshCaptcha: !prevState.refreshCaptcha
          }
        })
      })
  }

  handleSubmit (e) {
    e.preventDefault()

    this.setState({
      loading: true,
      checkedTermsOfUse: false
    })

    const modifiedAnswers = this.state.questions.filter(
      (question) => question.modified
    )

    const validatedQuestions = modifiedAnswers.filter((question) => {
      if (!question.is_open) {
        const otherChoice = question.choices.find(
          (choice) => choice.is_other_choice
        )
        const otherChoiceSelected =
          otherChoice &&
          question.userChoices.filter(
            (userChoice) => userChoice === otherChoice.id
          ).length > 0
        if (otherChoiceSelected) {
          if (!question.other_choice_answer) {
            this.addValidationError(otherChoice.id)
          } else {
            this.removeValidationError(otherChoice.id)
            return question
          }
        }
      }
      return question
    })

    const voteData = {}
    for (const question of validatedQuestions) {
      voteData[question.id] = {
        choices: question.userChoices,
        other_choice_answer: question.other_choice_answer || '',
        open_answer: question.open_answer || ''
      }
    }
    const data = {
      urlReplaces: { pollId: this.props.pollId },
      votes: voteData,
      captcha: this.state.captcha
    }
    if (
      this.state.useTermsOfUse &&
      !this.state.agreedTermsOfUse &&
      this.state.checkedTermsOfUse
    ) {
      data.agreed_terms_of_use = true
    }
    this.updateAgreedTOS()
    validatedQuestions.length > 0
      ? this.sendRequest(data)
      : Object.keys(this.state.errors).length > 0
        ? this.setState({ loading: false, alert: ALERT_SUCCESS })
        : this.setState({ loading: false, alert: ALERT_INVALID })
  }

  getPollData () {
    api.poll.get(this.props.pollId).done((poll) => {
      this.setState({
        result: JSON.parse(JSON.stringify(poll.questions)),
        questions: poll.questions,
        allowUnregisteredUsers: poll.allow_unregistered_users,
        showResults:
          (poll.questions.length > 0 && poll.questions[0].isReadOnly) ||
          poll.has_user_vote,
        hasUserVote: poll.has_user_vote,
        useTermsOfUse: poll.use_org_terms_of_use,
        agreedTermsOfUse: poll.user_has_agreed,
        orgTermsUrl: poll.org_terms_url,
        loadingPage: false
      })
    }
    )
  }

  componentDidMount () {
    this.getPollData()
    window.addEventListener('agreedTos', this.handleTermsOfUse)
  }

  componentWillUnmount () {
    window.removeEventListener('agreedTos', this.handleTermsOfUse)
  }

  render () {
    this.buttonVote = this.getVoteButton()
    return this.state.loadingPage
      ? (
          this.loadingIndicator
        )
      : (
        <>
          {this.state.showResults
            ? (
              <div className="poll__preliminary-results">
                {this.state.result.map((question, idx) => (
                  <PollResults key={idx} question={question} />
                ))}
                <Alert onClick={() => this.removeAlert()} {...this.state.alert} />
                {this.state.questions.length > 0 && this.state.questions[0].authenticated &&
                  <div className="poll">
                    {this.state.hasUserVote ? this.linkChangeVote : this.linkToPoll}
                  </div>}
              </div>
              )
            : (
              <div className="pollquestionlist-container">
                <form>
                  {this.state.questions.map((question, idx) =>
                    question.is_open
                      ? (
                        <PollOpenQuestion
                          key={idx}
                          allowUnregisteredUsers={this.state.allowUnregisteredUsers}
                          question={question}
                          onOpenChange={(questionId, voteData) =>
                            this.handleVoteOpen(questionId, voteData)}
                          errors={this.state.errors}
                        />
                        )
                      : (
                        <PollChoice
                          key={idx}
                          question={question}
                          allowUnregisteredUsers={this.state.allowUnregisteredUsers}
                          onSingleChange={(questionId, voteData) =>
                            this.handleVoteSingle(questionId, voteData)}
                          onMultiChange={(questionId, voteData) =>
                            this.handleVoteMulti(questionId, voteData)}
                          onOtherChange={(questionId, voteAnswer, otherChoice) =>
                            this.handleVoteOther(questionId, voteAnswer, otherChoice)}
                          errors={this.state.errors}
                        />
                        )
                  )}
                </form>
                <Alert onClick={() => this.removeAlert()} {...this.state.alert} />

                {this.isReadOnly()
                  ? (
                    <div className="poll">
                      {this.state.loading
                        ? this.loadingIndicator
                        : this.linkShowResults()}
                    </div>
                    )
                  : (
                    <>
                      {/* Terms of Use Section */}
                      {this.state.useTermsOfUse && !this.state.agreedTermsOfUse && (
                        <div className="col-12">
                          <TermsOfUseCheckbox
                            id="terms-of-use"
                            onChange={(val) => this.setState({ checkedTermsOfUse: val })}
                            orgTermsUrl={this.state.orgTermsUrl}
                          />
                        </div>
                      )}

                      {/* Captcha Section */}
                      {this.state.allowUnregisteredUsers &&
                        this.state.questions.length > 0 &&
                        !this.state.questions[0].authenticated && (
                          <Captcha
                            onChange={(val) => this.setState({ captcha: val })}
                            apiUrl={this.props.captchaUrl}
                            name="id_captcheck"
                            refresh={this.state.refreshCaptcha}
                          />
                      )}

                      {/* Button Wrapper */}
                      <div className="poll poll__btn--wrapper">
                        {this.buttonVote}
                        {!this.state.loading ? this.linkShowResults() : this.loadingIndicator}
                      </div>
                    </>
                    )}
              </div>
              )}
        </>
        )
  }
}

export default PollQuestions
