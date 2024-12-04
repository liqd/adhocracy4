import React from 'react'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { EndSessionLink } from '../EndSessionLink'
import { BrowserRouter } from 'react-router'

test('End session - check: modal rendered', async () => {
  render(
    <BrowserRouter>
      <EndSessionLink />
    </BrowserRouter>
  )

  const modalBtn = screen.getByRole('button', { name: 'End session' })
  const modalRender = screen.queryByRole('dialog')
  expect(modalRender).toBeNull()
  fireEvent.click(modalBtn)

  await waitFor(() => {
    const modalRender = screen.findByRole('dialog', { hidden: false })
    expect(modalRender).toBeTruthy()
  })
})

test('End session - check: end session url fetch failed, tests hidden btn click, not in rendered modal', async () => {
  // overwrite global.fetch with mock function
  global.fetch = jest.fn().mockRejectedValue('testing: expected network error')

  render(
    <BrowserRouter>
      <EndSessionLink />
    </BrowserRouter>
  )
  // get second instance of End session btn
  const endSessionBtn = screen.getAllByRole('button', { name: 'End session', hidden: true })[1]
  fireEvent.click(endSessionBtn)

  expect(global.fetch).toHaveBeenCalledTimes(1)
  const noUrl = screen.queryAllByText('mock text')
  expect(noUrl).toBeTruthy()

  // reverse overwrite of global.fetch
  await global.fetch.mockClear()
})
