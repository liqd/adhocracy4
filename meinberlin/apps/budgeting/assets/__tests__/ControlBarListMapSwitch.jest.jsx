import React from 'react'
import { render, screen } from '@testing-library/react'
import { ControlBarListMapSwitch } from '../ControlBarListMapSwitch'

test('Buttonlink to map with href', () => {
  render(<ControlBarListMapSwitch query="&ordering=-created" />)
  const linkToMap = screen.getByRole('link')
  expect(linkToMap.href).toMatch(/(\?mode=map&ordering=-created)/i)
})
