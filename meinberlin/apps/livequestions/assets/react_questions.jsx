import QuestionBox from './QuestionBox'
import React from 'react'
import ReactDOM from 'react-dom'

export function renderQuestions (el) {
  const props = JSON.parse(el.getAttribute('data-attributes'))
  ReactDOM.render(<QuestionBox {...props} />, el)
}
