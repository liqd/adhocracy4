// tools needed for testing
import React from 'react'
import { render, screen } from '@testing-library/react'
import ChapterNavItem from '../ChapterNavItem'

test('ChapterNavItem top renders correctly', () => {
  const { asFragment } = render(
    <ChapterNavItem name="Chapter name" index={0} active onMoveUp={null} />
  )
  expect(asFragment()).toMatchSnapshot()
})

test('ChapterNavItem middle renders correctly', () => {
  const { asFragment } = render(
    <ChapterNavItem name="Chapter name" index={2} active={false} />
  )
  expect(asFragment()).toMatchSnapshot()
})

test('ChapterNavItem bottom renders correctly', () => {
  const { asFragment } = render(
    <ChapterNavItem
      name="Chapter name"
      index={3}
      active={false}
      onMoveDown={null}
    />
  )
  expect(asFragment()).toMatchSnapshot()
})

test('ChapterNavItem error case', () => {
  render(
    <ChapterNavItem
      name="Chapter name"
      index={3}
      active={false}
      onMoveDown={null}
      errors={{ paragraphs: ['paragraph1'] }}
    />
  )
  const errorCountElement = screen.queryByText(/\s*\(\s*\d\s*\)/)
  expect(errorCountElement).toBeTruthy()
})
