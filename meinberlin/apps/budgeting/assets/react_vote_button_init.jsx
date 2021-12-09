import React from 'react'
import ReactDOM from 'react-dom'
import { widget as ReactWidget } from 'adhocracy4'
import { VoteButton } from './VoteButton.jsx'

function init () {
  ReactWidget.initialise('mb', 'vote_button',
    function (el) {
      const props = el.getAttribute('data-attributes')
      ReactDOM.render(<VoteButton {...props} />, el)
    }
  )
}

document.addEventListener('DOMContentLoaded', init, false)
document.addEventListener('a4.embed.ready', init, false)
