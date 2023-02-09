import React from 'react'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { EndSessionLink } from '../EndSessionLink'

test('End session - check: modal rendered', async () => {
  const user = userEvent.setup()
  render(<EndSessionLink />)

  const modalBtn = screen.queryAllByText('End session[0]')
  await user.click(modalBtn)

  expect(screen.getByText('To save your votes you do not need to do anything else')).toBeTruthy()
})
