import React from 'react'
import { render, screen } from '@testing-library/react'
import { FilterBarListMapSwitch } from '../FilterBarListMapSwitch'

test('Buttonlink to map with href', () => {
  render(<FilterBarListMapSwitch query="&ordering=-created" />)
  const linkToMap = screen.getByRole('link')
  expect(linkToMap.href).toMatch(/(\?mode=map&ordering=-created)/i)
})
