import StatisticsBox from './StatisticsBox'
import React from 'react'
import ReactDOM from 'react-dom'

export function renderData (el) {
  const props = JSON.parse(el.getAttribute('data-attributes'))
  ReactDOM.render(<StatisticsBox {...props} />, el)
}
