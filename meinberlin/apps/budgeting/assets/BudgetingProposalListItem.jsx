import React from 'react'
import django from 'django'
import { toLocaleDate } from '../../contrib/assets/helpers'
import VoteButton from './VoteButton'
import { ListItemBadges } from './ListItemBadges'
import { ListItemStats } from './ListItemStats'

const updatedOnStr = django.gettext('updated on')
const createdOnStr = django.gettext('created on')

export const BudgetingProposalListItem = (props) => {
  const { proposal, permissions, tokenvoteApiUrl } = props
  const safeLocale = props.locale ? props.locale : undefined
  const date = proposal.modified
    ? updatedOnStr + ' ' + toLocaleDate(
      proposal.modified,
      safeLocale
    )
    : createdOnStr + ' ' + toLocaleDate(
      proposal.created,
      safeLocale
    )

  return (
    <li id={'proposal_' + proposal.pk} className="list-item">
      <h2 className="list-item__title">
        <a href={proposal.url}>{proposal.name}</a>
      </h2>
      <ListItemStats
        permissions={permissions}
        positiveCount={proposal.positive_rating_count}
        negativeCount={proposal.negative_rating_count}
        commentCount={proposal.comment_count}
        voteCount={proposal.vote_count}
      />
      <ListItemBadges
        badges={proposal.item_badges_for_list}
        numOfMoreBadges={proposal.additional_item_badges_for_list_count}
        proposalUrl={proposal.url}
      />
      <div className="list-item__vote">
        <div>
          <span className="list-item__author test">{proposal.creator}</span>
          {date + ' - ' + proposal.reference_number}
        </div>
        {permissions.has_voting_permission_and_valid_token && proposal.vote_allowed && (
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
