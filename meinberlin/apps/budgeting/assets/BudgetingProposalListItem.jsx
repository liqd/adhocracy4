import React from 'react'
import django from 'django'
import { toDate } from './helpers'
import SwitchButton from '../../contrib/assets/SwitchButton'

export const BudgetingProposalListItem = (props) => {
  const { proposal } = props
  return (
    <li className="list-item no-hover">
      <h3 className="list-item__title">
        <a href={proposal.url}>
          {proposal.name}
        </a>
      </h3>
      <div className="list-item__labels">
        {proposal.category &&
          <span className="label label--big">
            {proposal.category.name}
          </span>}
        {proposal.budget > 0 &&
          <span className="label label--big">
            {proposal.budget} €
          </span>}
      </div>
      <div className="list-item__vote">
        <div>
          <span className="list-item__author">
            {proposal.creator}
          </span>
          {toDate(proposal.created)}
        </div>
        <SwitchButton
          onText={django.gettext('Voted')}
          offText={django.gettext('Give my vote')}
          onClass="btn"
          offClass="btn btn--light"
          uniqueID={proposal.pk}
        />
      </div>
    </li>
  )
}
