import React from 'react'
import django from 'django'
import { toLocaleDate } from './helpers'
import VoteButton from './VoteButton'
import { ListItemBadges } from './ListItemBadges'
import { ListItemStats } from './ListItemStats'

const updatedOnStr = django.gettext('updated on')
const createdOnStr = django.gettext('created on')
const BADGES_LIMIT = 3

export const BudgetingProposalListItem = (props) => {
  const { proposal, permissions, tokenvoteApiUrl } = props
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

  const normalizeBadgesData = () => {
    const tmpList = []
    if (proposal.moderator_feedback) {
      tmpList.push({ type: 'modFeedback', value: proposal.moderator_feedback })
    }
    if (proposal.budget) {
      tmpList.push({ type: 'budget', value: proposal.budget })
    }
    if (proposal.point_label) {
      tmpList.push({ type: 'pointLabel', value: proposal.point_label })
    }
    if (proposal.category) {
      tmpList.push({ type: 'category', value: proposal.category })
    }
    if (proposal.labels && proposal.labels.length !== 0) {
      for (let i = 0; i < proposal.labels.length; i++) {
        tmpList.push({ type: 'label', value: proposal.labels[i] })
      }
    }
    return tmpList
  }

  const badges = normalizeBadgesData()
  const numOfMoreBadges = badges.length > BADGES_LIMIT
    ? badges.length - BADGES_LIMIT
    : -1

  return (
    <li className="list-item">
      <ListItemStats
        permissions={permissions}
        positiveCount={proposal.positive_rating_count}
        negativeCount={proposal.negative_rating_count}
        commentCount={proposal.comment_count}
      />
      <h2 className="list-item__title">
        <a href={proposal.url}>{proposal.name}</a>
      </h2>
      <ListItemBadges
        badges={badges.slice(0, BADGES_LIMIT)}
        numOfMoreBadges={numOfMoreBadges}
        proposalUrl={proposal.url}
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
