import React, { useState, useEffect } from 'react'
import PollQuestion from './PollQuestion'

const api = require('adhocracy4').api

export const PollQuestions = (props) => {
  const [questions, setQuestions] = useState([])

  useEffect(() => {
    api.poll.get(props.moduleId)
      .done(r => setQuestions(r.questions))
  }, [])

  return (
    <div className="pollquestionlist-container">
      Here are the PollQuestion items
      {questions.map((q, idx) => <PollQuestion key={idx} question={q} />)}
    </div>
  )
}
