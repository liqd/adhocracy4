import { BudgetingProposalList } from './BudgetingProposalList.jsx'
import React from 'react'
import ReactDOM from 'react-dom'

export function renderProposals (el) {
  const props = JSON.parse(el.getAttribute('data-attributes'))
  ReactDOM.render(<BudgetingProposalList {...props} />, el)
}
