import StatisticsBox from './StatisticsBox'
import React from 'react'
import { createRoot } from 'react-dom/client'

export function renderData (el) {
  const props = JSON.parse(el.getAttribute('data-attributes'))
  const root = createRoot(el)
  root.render(<StatisticsBox {...props} />, el)
}
