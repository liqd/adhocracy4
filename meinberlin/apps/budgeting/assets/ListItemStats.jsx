import React from 'react'
import django from 'django'
import { wrapSpaces } from './helpers'

export const ListItemStats = (props) => {
  return (
    <div className="list-item__stats">
      <span className="rating">
        <span
          className="rating-button rating-up is-read-only"
          title={django.gettext('Positive Ratings')}
        >
          <i
            className="fa fa-chevron-up"
            aria-label={django.gettext('Positive Ratings')}
          />
          {wrapSpaces(props.positiveCount)}
        </span>
        <span
          className="rating-button rating-down is-read-only"
          title={django.gettext('Negative Ratings')}
        >
          <i
            className="fa fa-chevron-down"
            aria-label={django.gettext('Negative Ratings')}
          />
          {wrapSpaces(props.negativeCount)}
        </span>
      </span>
      <span
        title={django.gettext('Comments')}
        className="list-item__comments"
      >
        <i
          className="far fa-comment"
          aria-label={django.gettext('Comments')}
        />
        {wrapSpaces(props.commentCount)}
      </span>
    </div>
  )
}
