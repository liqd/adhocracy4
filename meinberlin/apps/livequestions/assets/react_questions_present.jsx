import PresentBox from './PresentBox'
import React from 'react'
import ReactDOM from 'react-dom'

export function renderData (el) {
  const props = JSON.parse(el.getAttribute('data-attributes'))
  ReactDOM.render(<PresentBox {...props} />, el)
}
