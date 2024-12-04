import React from 'react'
import django from 'django'
import Modal from 'adhocracy4/adhocracy4/static/Modal'
import { useSearchParams } from 'react-router'

export const EndSessionLink = (props) => {
  const translations = {
    finished: django.gettext('Are you finished?'),
    endSession: django.gettext('End session'),
    modalDescription: django.gettext('To save your votes you do not need to do anything else. End the session to enter a new code. If you want to change the votes you have already cast, you can re-enter your code as long as the voting phase is running. '),
    modalBodyQuestion: django.gettext('Do you want to end the session?'),
    modalCancel: django.gettext('Cancel')
  }
  const [queryParams, setQueryParams] = useSearchParams()

  const modalPartials = {
    title: translations.endSession,
    description: translations.modalDescription,
    abort: translations.modalCancel
  }

  const handleEndSession = () => {
    // remove own_votes from url parameters when session is ended
    queryParams.delete('own_votes')
    setQueryParams(queryParams)

    const endSessionUrl = props.endSessionUrl
    fetch(endSessionUrl)
      .then(() => window.location.reload(true))
      .catch(error => console.log(error))
  }

  return (
    <>
      <div className="u-spacer-bottom u-align-center">
        <span>{translations.finished} </span>
        <button
          id="session-modal-toggle"
          type="button"
          className="btn--link"
          data-bs-toggle="modal"
          data-bs-target="#end-session_modal"
        >
          {translations.endSession}
          {props.end_session_url}
        </button>
      </div>
      <Modal
        name="end-session_modal"
        abort={translations.modalCancel}
        action={translations.endSession}
        partials={modalPartials}
        handleSubmit={handleEndSession}
      />
    </>
  )
}
