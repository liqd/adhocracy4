import React from 'react'
import django from 'django'
import { toLocaleDate } from './helpers'
import CheckboxButton from '../../contrib/assets/CheckboxButton'
import { ListItemBadges } from './ListItemBadges'
import { ListItemStats } from './ListItemStats'

export const BudgetingProposalListItem = (props) => {
  const { proposal: p, isVotingPhase } = props
  const safeLocale = p.locale ? p.locale : undefined
  const date = p.modified
    ? `${django.gettext('modified on')} ${toLocaleDate(p.modified, safeLocale)}`
    : `${django.gettext('created on')} ${toLocaleDate(p.created, safeLocale)}`

  return (
    <li className="list-item no-hover">
      {!isVotingPhase &&
        <ListItemStats
          positiveCount={p.positive_rating_count}
          negativeCount={p.negative_rating_count}
          commentCount={p.comment_count}
        />}
      <h3 className="list-item__title">
        <a href={p.url}>
          {p.name}
        </a>
      </h3>
      <ListItemBadges
        category={p.category}
        budget={p.budget}
        pointLabel={p.point_label}
        moderatorFeedback={p.moderator_feedback}
        moderatorChoices={p.moderator_feedback_choices}
      />
      <div className="list-item__vote">
        <div>
          <span className="list-item__author">
            {p.creator}
          </span>
          {date}
        </div>
        {isVotingPhase &&
          <CheckboxButton
            onText={django.gettext('Voted')}
            offText={django.gettext('Give my vote')}
            onClass="btn"
            offClass="btn btn--light"
            uniqueID={p.pk}
          />}
      </div>
    </li>
  )
}
