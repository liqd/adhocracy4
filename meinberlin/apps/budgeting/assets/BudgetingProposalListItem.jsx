import React from 'react'
import django from 'django'
import { toLocaleDate } from './helpers'
import CheckboxButton from '../../contrib/assets/CheckboxButton'
import { ListItemBadges } from './ListItemBadges'
import { ListItemStats } from './ListItemStats'

export const BudgetingProposalListItem = (props) => {
  const { proposal, isVotingPhase } = props
  const safeLocale = proposal.locale ? proposal.locale : undefined
  return (
    <li className="list-item no-hover">
      {!isVotingPhase &&
        <ListItemStats
          positiveCount={proposal.positive_rating_count}
          negativeCount={proposal.negative_rating_count}
          commentCount={proposal.comment_count}
        />}
      <h3 className="list-item__title">
        <a href={proposal.url}>
          {proposal.name}
        </a>
      </h3>
      <ListItemBadges
        category={proposal.category}
        budget={proposal.budget}
        pointLabel={proposal.point_label}
        moderatorFeedback={proposal.moderator_feedback}
        moderatorChoices={proposal.moderator_feedback_choices}
      />
      <div className="list-item__vote">
        <div>
          <span className="list-item__author">
            {proposal.creator}
          </span>
          {toLocaleDate(proposal.created, safeLocale)}
        </div>
        {isVotingPhase &&
          <CheckboxButton
            onText={django.gettext('Voted')}
            offText={django.gettext('Give my vote')}
            onClass="btn"
            offClass="btn btn--light"
            uniqueID={proposal.pk}
          />}
      </div>
    </li>
  )
}
