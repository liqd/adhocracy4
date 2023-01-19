import React from 'react'
import django from 'django'

export const ListItemStats = (props) => {
  const { permissions } = props

  const positiveRatingsStr = django.gettext('Positive Ratings')
  const negativeRatingsStr = django.gettext('Negative Ratings')
  const supportStr = django.gettext('Support')
  const commentsStr = django.gettext('Comments')
  const supportText = django.ngettext(
    'person supports this proposal.',
    'persons support this proposal.',
    props.positiveCount
  )

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
              aria-hidden="true"
            />
            {props.positiveCount}
            <span className="visually-hidden">{positiveRatingsStr}</span>
          </span>
          <span
            className="rating-button rating-down is-read-only"
            title={negativeRatingsStr}
          >
            <i
              className="fa fa-chevron-down"
              aria-hidden="true"
            />
            {props.negativeCount}
            <span className="visually-hidden">{negativeRatingsStr}</span>
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
              aria-hidden="true"
            />
            {props.positiveCount}
            <span className="visually-hidden">
              {supportText}
            </span>
          </span>
        </span>
      )}
      {permissions.view_comment_count && (
        <span
          title={commentsStr}
          className="list-item__comments"
        >
          <i
            className="far fa-comment u-icon-spacing"
            aria-hidden="true"
          />
          {props.commentCount}
          <span className="visually-hidden">{commentsStr}</span>
        </span>
      )}
    </div>
  )
}
