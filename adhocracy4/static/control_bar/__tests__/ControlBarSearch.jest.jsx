import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'
import { ControlBarSearch } from '../ControlBarSearch'

test('ControlBarSearch changing searchterm', () => {
  render(
    <ControlBarSearch term="example" placeholder="Search for Proposals" />
  )
  const searchInput = screen.getByPlaceholderText('Search for Proposals')
  expect(searchInput.value).toBe('example')
  fireEvent.change(searchInput, { target: { value: 'changed example' } })
  expect(searchInput.value).toBe('changed example')
})

test('ControlBarSearch submit search', () => {
  const onSearchFn = jest.fn()
  render(<ControlBarSearch term="example" onSearch={onSearchFn} />)
  const searchForm = window.document.querySelector('form')
  fireEvent.submit(searchForm)
  expect(onSearchFn).toHaveBeenCalled()
})
