import React from 'react'
import django from 'django'

export const ListItemStats = (props) => {
  const { permissions } = props

  const positiveRatingsStr = django.gettext('Positive Ratings')
  const negativeRatingsStr = django.gettext('Negative Ratings')
  const supportStr = django.gettext('Support')
  const commentsStr = django.gettext('Comments')
  const votesStr = django.gettext('Total votes')
  const supportText = django.ngettext(
    'person supports this proposal.',
    'persons support this proposal.',
    props.positiveCount
  )

  return (
    <div className="list-item__stats">
      {/* ratings visible to admins in 1 and 2 phase budgeting due to `has_perm`  */}
      {permissions.view_rate_count && (
        <>
          <span
            className="list-item__icon"
            title={positiveRatingsStr}
          >
            <i
              className="fa fa-thumbs-up u-icon-spacing"
              aria-hidden="true"
            />
            {props.positiveCount}
            <span className="visually-hidden">{positiveRatingsStr}</span>
          </span>
          <span
            className="list-item__icon"
            title={negativeRatingsStr}
          >
            <i
              className="fa fa-thumbs-down u-icon-spacing"
              aria-hidden="true"
            />
            {props.negativeCount}
            <span className="visually-hidden">{negativeRatingsStr}</span>
          </span>
        </>
      )}

      {permissions.view_support_count && (
        <span
          className="list-item__icon u-success"
          title={supportStr}
        >
          <i
            className="far fa-thumbs-up u-icon-spacing"
            aria-hidden="true"
          />
          {props.positiveCount}
          <span className="visually-hidden">
            {supportText}
          </span>
        </span>
      )}
      {permissions.view_vote_count && (
        <span
          className="list-item__icon u-primary"
          title={votesStr}
        >
          <i
            className="fa-regular fa-square-check u-icon-spacing"
            aria-hidden="true"
          />
          {props.voteCount}
          <span className="visually-hidden">{votesStr}</span>
        </span>
      )}
      {permissions.view_comment_count && (
        <span
          title={commentsStr}
          className="list-item__icon"
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
