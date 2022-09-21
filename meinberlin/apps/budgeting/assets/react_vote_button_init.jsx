import React from 'react'
import { createRoot } from 'react-dom/client'
import { widget as ReactWidget } from 'adhocracy4'
import VoteButton from './VoteButton.jsx'

function init () {
  ReactWidget.initialise('mb', 'vote_button', function (el) {
    const props = JSON.parse(el.getAttribute('data-attributes'))
    const votesLeft = props.token_info ? props.token_info.votes_left : false
    const root = createRoot(el)
    root.render(
      <React.StrictMode>
        <VoteButton
          objectID={props.objectID}
          tokenvoteApiUrl={props.tokenvote_api_url}
          isChecked={props.session_token_voted}
          disabled={!votesLeft && !props.session_token_voted}
          asWidget
        />
      </React.StrictMode>
    )
  })
}

document.addEventListener('DOMContentLoaded', init, false)
document.addEventListener('a4.embed.ready', init, false)
