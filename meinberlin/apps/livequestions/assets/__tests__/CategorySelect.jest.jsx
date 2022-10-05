import React from 'react'
import { render } from '@testing-library/react'
import jQuery from 'jquery'

import { CategorySelect } from '../CategorySelect'

window.$ = window.jQuery = jQuery

test('CategorySelect renders correctly', () => {
  const { asFragment } = render(
    <CategorySelect
      name="Category"
      category_dict={{ 123: 'category1', 124: 'category2' }}
    />)
  expect(asFragment()).toMatchSnapshot()
})
