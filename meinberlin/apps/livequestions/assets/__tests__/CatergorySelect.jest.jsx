import React from 'react'
import { render } from '@testing-library/react'
import SelectCategory from '../CategorySelect'

test('SelectCategory renders correctly', () => {
  const { asFragment } = render(
    <SelectCategory
      name="Category"
      category_dict={{ 123: 'category1', 124: 'category2' }}
    />)
  expect(asFragment()).toMatchSnapshot()
})
