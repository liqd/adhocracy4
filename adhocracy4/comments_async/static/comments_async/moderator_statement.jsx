import React from 'react'

export const ModeratorStatement = ({ lastEdit, statement }) => {
  const translated = {
    moderator: 'Moderator'
  }
  return (
    <div className="row">
      <div className="a4-comments__moderator-statement__container">
        <i className="fas fa-share a4-comments__moderator-statement__icon" />
        <div className="a4-comments__moderator-statement__content">
          <div className="a4-comments__moderator-statement__moderator">
            {translated.moderator}
          </div>
          <div className="a4-comments__moderator-statement__date">
            {lastEdit}
          </div>
          <p className="a4-comments__moderator-statement__text">
            {statement}
          </p>
        </div>
      </div>
    </div>
  )
}
