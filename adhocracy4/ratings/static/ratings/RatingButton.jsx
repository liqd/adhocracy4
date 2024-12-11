import React from 'react'
import django from 'django'

const translations = {
  upvote: django.gettext('Click to like'),
  downvote: django.gettext('Click to dislike')
}

const RatingButton = ({
  rating,
  active,
  onClick,
  authenticatedAs,
  isReadOnly,
  children
}) => {
  const onClickWrapper = () => {
    onClick(active ? 0 : rating)
  }

  const type = rating === -1 ? 'down' : 'up'
  const cssClasses = active
    ? 'rating-button rating-' + type + ' is-selected'
    : 'rating-button rating-' + type

  return (
    <button
      aria-pressed={active}
      className={cssClasses}
      disabled={authenticatedAs !== null && isReadOnly}
      onClick={onClickWrapper}
      type="button"
    >
      {children}
      <span className="a4-sr-only">{type === 'up' ? translations.upvote : translations.downvote}</span>
    </button>
  )
}

export default RatingButton
