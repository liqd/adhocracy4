import React, { useState, useEffect } from 'react'
import { PollQuestion } from './PollQuestion'
import Alert from '../../static/Alert'
import django from 'django'

const api = require('adhocracy4').api
const config = require('adhocracy4').config

export const PollQuestions = (props) => {
  const [questions, setQuestions] = useState([])
  const [showResults, setShowResults] = useState(false)
  // votes: [
  //   {questionId: 1, choices: [], other_choice_answer: [], open_answer: []}
  //   {questionId: 2, choices: [], other_choice_answer: [], open_answer: []}
  // ]
  const [votes] = useState([])
  // const [vote, setVote] = useState()
  const [alert, setAlert] = useState()

  const handleVoteSingle = (questionId, voteData) => {
    let vote = votes.find(v => v.questionId === questionId)
    !vote && (vote = {
      urlReplaces: { questionId },
      choices: [parseInt(voteData)],
      other_choice_answer: [],
      open_answer: []
    })
    console.log(vote)
  }

  const handleVoteMulti = (questionId, voteData) => {
    console.log(questionId, voteData)
  }

  const handleVoteOther = (questionId, voteData) => {
    console.log(questionId, voteData)
  }

  const handleToggleResultsPage = () => setShowResults(!showResults)
  const hasAnyVotes = () => votes.length > 0
  const isReadOnly = () => questions.length > 0 && questions[0].isReadOnly
  const removeAlert = () => setAlert(null)

  const getVoteButton = () => {
    const isAuthenticated = questions.length > 0 && questions[0].authenticated

    if (isAuthenticated) {
      const disabled = !hasAnyVotes // also in case no changes yet!
      return (
        <button
          type="submit"
          className="btn btn--primary u-spacer-right"
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

  const handleSubmit = (e) => {
    // e.preventDefault()

    // console.log(e)
    // setAlert({
    //   type: 'success',
    //   message: django.gettext('The poll has been updated.')
    // })

    // const result = api.poll.vote(data, props.pollId)
    //   .done((response) => {
    //     return response
    //     // setAlert({
    //     //   type: 'success',
    //     //   message: django.gettext('The poll has been updated.')
    //     // })
    //     // setErrors([])
    //     // if (props.reloadOnSuccess) {
    //     //   dashboard.updateDashboard()
    //     // }
    //   })
    //   .fail((xhr, status, err) => {
    //     // if (xhr.responseJSON && 'questions' in xhr.responseJSON) {
    //     //   setErrors(xhr.responseJSON.questions)
    //     // }

    //     setAlert({
    //       type: 'danger',
    //       message: django.gettext('The poll could not be updated.')
    //     })
    //   })
    // console.log(result)
  }

  // const removeAlert = () => {
  //   this.setState({
  //     alert: null
  //   })
  // }

  // const getHelpTextAnswer = () => {
  //   const total = this.state.question.totalVoteCount
  //   const totalMulti = this.state.question.totalVoteCountMulti

  //   let helpTextAnswer
  //   let helpTextAnswerPlural
  //   if (this.state.question.multiple_choice) {
  //     if (total === 1 && totalMulti === 1) {
  //       helpTextAnswerPlural = django.gettext('%s participant gave 1 answer.')
  //     } else if (total === 1 && totalMulti > 1) {
  //       helpTextAnswerPlural = django.gettext('%s participant gave %s answers.', total)
  //     } else {
  //       helpTextAnswerPlural = django.ngettext('%s participant gave %s answers.', '%s participants gave %s answers.', total)
  //     }
  //     helpTextAnswer = helpTextAnswerPlural + django.gettext(' For multiple choice questions the percentages may add up to more than 100%.')
  //   } else {
  //     helpTextAnswer = django.ngettext('1 person has answered.', '%s people have answered.', total)
  //   }
  //   return django.interpolate(helpTextAnswer, [total, totalMulti])
  // }

  // Creating all types of buttons and links
  const buttonVote = getVoteButton()
  const linkShowResults = (
    <button type="button" className="btn btn--link" onClick={handleToggleResultsPage}>
      {django.gettext('Show preliminary results')}
    </button>
  )

  const linkToPoll = (
    <button type="button" className="btn btn--link" onClick={handleToggleResultsPage}>
      {django.gettext('To poll')}
    </button>
  )
  const linkChangeVote = (
    <button type="button" className="btn btn--link" onClick={handleToggleResultsPage}>
      {django.gettext('Change vote')}
    </button>)

  useEffect(() => {
    api.poll.get(props.pollId)
      .done(r => setQuestions(r.questions))
  }, [])

  const pollScreen = (
    <div className="pollquestionlist-container">
      <form onSubmit={(e) => handleSubmit(e)}>
        {questions.map((q, idx) => (
          <PollQuestion
            key={idx}
            question={q}
            onSingleChange={(questionId, voteData) => handleVoteSingle(questionId, voteData)}
            onMultiChange={(questionId, voteData) => handleVoteMulti(questionId, voteData)}
            onOtherChange={(questionId, voteData) => handleVoteOther(questionId, voteData)}
          />
        ))}
        <Alert onClick={() => removeAlert()} {...alert} />
        {!isReadOnly() && (
          <div className="poll__actions">
            {buttonVote}{linkShowResults}
          </div>
        )}
      </form>
    </div>
  )

  const resultsScreen = (
    <div className="pollquestionlist-container">
      Results Screen
      <div className="poll__actions">
        {hasAnyVotes() ? linkChangeVote : linkToPoll}
      </div>
    </div>
  )

  return showResults ? resultsScreen : pollScreen
}

// handleSubmit (event) {
//   event.preventDefault()

//   if (this.state.question.isReadOnly) {
//     return false
//   }

//   const newChoices = this.state.selectedChoices

//   const submitData = {
//     choices: newChoices,
//     urlReplaces: { questionId: this.state.question.id }
//   }

//   api.poll.vote(submitData)
//     .done((data) => {
//       this.setState({
//         showResult: true,
//         selectedChoices: data.question.userChoices,
//         question: data.question,
//         alert: {
//           type: 'success',
//           message: django.gettext('Vote counted')
//         }
//       })
//     })
//     .fail((xhr, status, err) => {
//       this.setState({
//         showResult: false,
//         selectedChoices: newChoices,
//         alert: {
//           type: 'danger',
//           message: django.gettext('Vote has not been counted due to a server error.')
//         }
//       })
//     })
// }
