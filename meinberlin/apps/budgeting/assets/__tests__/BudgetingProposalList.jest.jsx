import React from 'react'
import { render } from '@testing-library/react'
import { BudgetingProposalList } from '../BudgetingProposalList'

// const data = {results: [
//   {
//     name: 'myProposal',
//     url: 'www',
//     budget: '80639',
//     creator: 'creator',
//     created: '2021-11-11T15:37:19.490201+01:00'
//   },
//   {
//     name: 'This is a second proposal',
//     url: 'www',
//     budget: '12000',
//     creator: 'creator part 2',
//     created: '2021-10-29T09:33:36.280033+01:00'
//   }
// ]}

// Mocks the fetch request
global.fetch = jest.fn(() =>
  Promise.resolve({
    json: () => Promise.resolve({ data: {} })
  })
)

// FIXME add test for when list is populated when know more about tests
// test('Budgeting Proposal List component renders a list when there are items', () => {
//   const { asFragment } = render(
//     <BudgetingProposalList data={data} />
//   )
//   expect(asFragment()).toMatchSnapshot()
// })

test('Budgeting Proposal List component renders a list when there are no items', () => {
  const { asFragment } = render(
    <BudgetingProposalList />
  )
  expect(asFragment()).toMatchSnapshot()
})
