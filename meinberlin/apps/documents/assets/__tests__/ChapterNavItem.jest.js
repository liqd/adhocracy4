// tools needed for testing
import React from 'react'
import { render } from '@testing-library/react'
import ChapterNavItem from '../ChapterNavItem'

test('ChapterNavItem top renders correctly', () => {
  const { asFragment } = render(
    <ChapterNavItem
      name="Chapter name"
      index={0}
      active
      onMoveUp={null}
    />)
  expect(asFragment()).toMatchSnapshot()
})

test('ChapterNavItem middle renders correctly', () => {
  const { asFragment } = render(
    <ChapterNavItem
      name="Chapter name"
      index={2}
      active={false}
    />)
  expect(asFragment()).toMatchSnapshot()
})

test('ChapterNavItem bottom renders correctly', () => {
  const { asFragment } = render(
    <ChapterNavItem
      name="Chapter name"
      index={3}
      active={false}
      onMoveDown={null}
    />)
  expect(asFragment()).toMatchSnapshot()
})
