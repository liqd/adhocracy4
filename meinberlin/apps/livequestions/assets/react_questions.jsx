import QuestionBox from './QuestionBox'
import React from 'react'
import { createRoot } from 'react-dom/client'

export function renderQuestions (el) {
  const props = JSON.parse(el.getAttribute('data-attributes'))
  const root = createRoot(el)
  root.render(
    <React.StrictMode>
      <QuestionBox {...props} />
    </React.StrictMode>
  )
}
