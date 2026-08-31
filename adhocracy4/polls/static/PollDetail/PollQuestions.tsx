/* eslint-disable @typescript-eslint/no-unused-expressions */
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
import type { Poll, PollQuestion, PollVotePayload } from '../../../static/api/types'

const captchaWidgets: Record<string, any> = {
  captcheck: Captcha
}

function getCaptchaWidget (type: string) {
  return captchaWidgets[type] || Captcha
}

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

interface PollQuestionsProps {
  pollId: number
  captchaUrl?: string
  captchaType?: string
  questionImagesEnabled?: boolean
}

interface PollQuestionsState {
  questions: PollQuestion[]
  captcha: string
  showResults: boolean
  allowUnregisteredUsers: boolean
  alert: any
  hasVotes: boolean
  errors: Record<string, any>
  loading: boolean
  loadingPage: boolean
  refreshCaptcha: boolean
  result: PollQuestion[]
  hasUserVote: boolean
  useTermsOfUse: boolean
  agreedTermsOfUse: boolean
  checkedTermsOfUse: boolean
  orgTermsUrl: string
}

export default class PollQuestions extends React.Component<PollQuestionsProps, PollQuestionsState> {
  linkToPoll: React.ReactElement
  linkChangeVote: React.ReactElement
  loadingIndicator: React.ReactElement
  buttonVote: React.ReactElement | undefined

  constructor (props: PollQuestionsProps) {
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
      refreshCaptcha: true,
      result: [],
      hasUserVote: false,
      useTermsOfUse: false,
      agreedTermsOfUse: false,
      checkedTermsOfUse: false,
      orgTermsUrl: ''
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

  setModified (questionId: number | string, value: boolean) {
    const currentQuestion = this.state.questions.find(
      (question) => question.id === questionId
    )
    this.setState({ hasVotes: value })
    if (currentQuestion) {
      currentQuestion.modified = value
    }
  }

  handleVoteSingle (questionId: number | string, choiceId: number) {
    this.setState((prevState: PollQuestionsState) => {
      const currentQuestion = prevState.questions.find(
        (question) => question.id === questionId
      )
      if (currentQuestion) {
        currentQuestion.userChoices = [choiceId]
      }
      return prevState
    })
    this.setModified(questionId, true)
  }

  handleVoteMulti (questionId: number | string, choiceId: number) {
    this.setState((prevState: PollQuestionsState) => {
      const currentQuestion = prevState.questions.find(
        (question) => question.id === questionId
      )
      if (currentQuestion) {
        const toRemove = currentQuestion.userChoices.findIndex(
          (userChoice: number) => userChoice === choiceId
        )
        toRemove !== -1 && currentQuestion.userChoices.splice(toRemove, 1)
        toRemove !== -1 || currentQuestion.userChoices.push(choiceId)
      }
      return prevState
    })
    this.setModified(questionId, true)
  }

  handleVoteOther (questionId: number | string, otherAnswer: string, otherChoice: any) {
    this.setState((prevState: PollQuestionsState) => {
      const currentQuestion = prevState.questions.find(
        (question) => question.id === questionId
      )
      otherChoice && delete this.state.errors[otherChoice.id]
      if (currentQuestion) {
        currentQuestion.other_choice_answer = otherAnswer
      }
      return prevState
    })
    this.setModified(questionId, true)
  }

  handleVoteOpen (questionId: number | string, openAnswer: string) {
    this.setState((prevState: PollQuestionsState) => {
      const currentQuestion = prevState.questions.find(
        (question) => question.id === questionId
      )
      if (currentQuestion) {
        currentQuestion.open_answer = openAnswer
      }
      return prevState
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

  addValidationError (choiceId: number) {
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

  removeValidationError (choiceId: number) {
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

  sendRequest (data: PollVotePayload) {
    api.poll
      .vote(data)
      .then((poll: Poll) => {
        this.setState(() => {
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

  handleSubmit (e: React.SyntheticEvent) {
    e.preventDefault()

    this.setState({
      loading: true,
      checkedTermsOfUse: false
    })

    const modifiedAnswers = this.state.questions.filter(
      (question) => question.modified
    )

    const validatedQuestions = modifiedAnswers.filter((question: any) => {
      if (!question.is_open) {
        const otherChoice = question.choices.find(
          (choice: any) => choice.is_other_choice
        )
        const otherChoiceSelected =
          otherChoice &&
          question.userChoices.filter(
            (userChoice: number) => userChoice === otherChoice.id
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

    const voteData: Record<number, PollVotePayload['votes'][number]> = {}
    for (const question of validatedQuestions) {
      voteData[question.id] = {
        choices: question.userChoices,
        other_choice_answer: question.other_choice_answer || '',
        open_answer: question.open_answer || ''
      }
    }
    const data: PollVotePayload = {
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
    api.poll.get(this.props.pollId).done((poll: Poll) => {
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

    const CaptchaWidget = getCaptchaWidget(this.props.captchaType || '')

    return this.state.loadingPage
      ? (
          this.loadingIndicator
        )
      : (
        <div className="poll-questions-container">
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
                          questionImagesEnabled={this.props.questionImagesEnabled}
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
                          questionImagesEnabled={this.props.questionImagesEnabled}
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
                            onChange={(val: boolean) => this.setState({ checkedTermsOfUse: val })}
                            orgTermsUrl={this.state.orgTermsUrl}
                          />
                        </div>
                      )}

                      {/* Captcha Section */}
                      {this.state.allowUnregisteredUsers &&
                        this.state.questions.length > 0 &&
                        !this.state.questions[0].authenticated && (
                          <CaptchaWidget
                            onChange={(val: string) => this.setState({ captcha: val })}
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
        </div>
        )
  }
}