import React from 'react'
import { toDate } from './helpers'

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
        <button className="btn btn--light">
          meine Stimme abgeben
        </button>
      </div>
    </li>
  )
}
