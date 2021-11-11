import React, { useEffect, useState } from 'react'
import { BudgetingProposalListItem } from './BudgetingProposalListItem'

export const BudgetingProposalList = (props) => {
  const [proposals, setProposals] = useState([])
  useEffect(() => {
    fetch(props.proposals_api_url)
      .then(resp => resp.json())
      .then(json => setProposals(json))
  }, [])
  return (
    <div className="l-wrapper">
      <div className="l-center-8">
        <ul className="u-list-reset">
          {proposals.map((proposal, idx) =>
            <BudgetingProposalListItem
              key={`budgeting-proposal-${idx}`}
              proposal={proposal}
            />)}
        </ul>
      </div>
    </div>
  )
}
