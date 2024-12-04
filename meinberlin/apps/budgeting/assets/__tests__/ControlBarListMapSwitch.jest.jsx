import React from 'react'
import { render, screen } from '@testing-library/react'
import { ControlBarListMapSwitch } from '../ControlBarListMapSwitch'
import { BrowserRouter } from 'react-router'

test('Buttonlink to map with href', () => {
  render(
    <BrowserRouter>
      <ControlBarListMapSwitch query="&ordering=-created" />
    </BrowserRouter>
  )
  const buttonToMap = screen.getByRole('button')
  expect(buttonToMap).toBeTruthy()
})
