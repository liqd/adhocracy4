import React, { useState, useEffect } from 'react'
import PollQuestion from './PollQuestion'

const api = require('adhocracy4').api

export const PollQuestions = (props) => {
  const [questions, setQuestions] = useState([])

  useEffect(() => {
    api.poll.get(props.pollId)
      .done(r => setQuestions(r.questions))
  }, [])

  return (
    <div className="pollquestionlist-container">
      {questions.map((q, idx) => <PollQuestion key={idx} question={q} />)}
    </div>
  )
}
