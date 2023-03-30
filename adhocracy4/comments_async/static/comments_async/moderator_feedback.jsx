import React from 'react'

export const ModeratorFeedback = ({ lastEdit, feedbackText }) => {
  const translated = {
    moderator: 'Moderator'
  }
  return (
    <div className="row">
      <div className="a4-comments__moderator-feedback__container">
        <i className="fas fa-share a4-comments__moderator-feedback__icon" />
        <div className="a4-comments__moderator-feedback__content">
          <div className="a4-comments__moderator-feedback__moderator">
            {translated.moderator}
          </div>
          <div className="a4-comments__moderator-feedback__date">
            {lastEdit}
          </div>
          <p className="a4-comments__moderator-feedback__text">
            {feedbackText}
          </p>
        </div>
      </div>
    </div>
  )
}
