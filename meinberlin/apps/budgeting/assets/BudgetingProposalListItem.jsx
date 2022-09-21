import React from 'react'
import django from 'django'
import { toLocaleDate } from './helpers'
import VoteButton from './VoteButton'
import { ListItemBadges } from './ListItemBadges'
import { ListItemStats } from './ListItemStats'

const updatedOnStr = django.gettext('updated on')
const createdOnStr = django.gettext('created on')

export const BudgetingProposalListItem = (props) => {
  const { proposal, isVotingPhase, tokenvoteApiUrl } = props
  const safeLocale = props.locale ? props.locale : undefined
  const date = proposal.modified
    ? `${updatedOnStr} ${toLocaleDate(
        proposal.modified,
        safeLocale
      )}`
    : `${createdOnStr} ${toLocaleDate(
        proposal.created,
        safeLocale
      )}`

  return (
    <li className="list-item">
      {!isVotingPhase && (
        <ListItemStats
          positiveCount={proposal.positive_rating_count}
          negativeCount={proposal.negative_rating_count}
          commentCount={proposal.comment_count}
        />
      )}
      <h3 className="list-item__title">
        <a href={proposal.url}>{proposal.name}</a>
      </h3>
      <ListItemBadges
        category={proposal.category}
        budget={proposal.budget}
        pointLabel={proposal.point_label}
        moderatorFeedback={proposal.moderator_feedback}
      />
      <div className="list-item__vote">
        <div>
          <span className="list-item__author">{proposal.creator}</span>
          {date}
          {` - ${proposal.reference_number}`}
        </div>
        {proposal.vote_allowed && (
          <VoteButton
            objectID={proposal.pk}
            tokenvoteApiUrl={tokenvoteApiUrl}
            isChecked={proposal.session_token_voted}
            onVoteChange={props.onVoteChange}
            currentPage={props.currentPage}
            disabled={!props.votesLeft && !proposal.session_token_voted}
          />
        )}
      </div>
    </li>
  )
}
