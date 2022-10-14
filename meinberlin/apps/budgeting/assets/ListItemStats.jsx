import React from 'react'
import django from 'django'
import { wrapSpaces } from './helpers'

const positiveRatingsStr = django.gettext('Positive Ratings')
const negativeRatingsStr = django.gettext('Negative Ratings')
const supportStr = django.gettext('Support')
const commentsStr = django.gettext('Comments')

export const ListItemStats = (props) => {
  const { permissions } = props
  return (
    <div className="list-item__stats">
      {permissions.view_rate_count && (
        <span className="rating">
          <span
            className="rating-button rating-up is-read-only"
            title={positiveRatingsStr}
          >
            <i
              className="fa fa-chevron-up"
              aria-label={positiveRatingsStr}
            />
            {wrapSpaces(props.positiveCount)}
          </span>
          <span
            className="rating-button rating-down is-read-only"
            title={negativeRatingsStr}
          >
            <i
              className="fa fa-chevron-down"
              aria-label={negativeRatingsStr}
            />
            {wrapSpaces(props.negativeCount)}
          </span>
        </span>
      )}

      {permissions.view_support_count && (
        <span className="support">
          <span
            className="rating-button rating-up is-read-only"
            title={supportStr}
          >
            <i
              className="far fa-thumbs-up"
              aria-label={supportStr}
            />
            {wrapSpaces(props.positiveCount)}
          </span>
        </span>
      )}
      {permissions.view_comment_count && (
        <span
          title={commentsStr}
          className="list-item__comments"
        >
          <i
            className="far fa-comment"
            aria-label={commentsStr}
          />
          {wrapSpaces(props.commentCount)}
        </span>
      )}
    </div>
  )
}
