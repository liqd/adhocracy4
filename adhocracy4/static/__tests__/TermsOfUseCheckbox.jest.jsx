import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'
import { TermsOfUseCheckbox } from '../TermsOfUseCheckbox'
import django from 'django'

test('One TermsOfUseCheckbox is showing', () => {
  render(<TermsOfUseCheckbox id="test-checkbox" />)
  const component = screen.getByLabelText(django.interpolate(), /mock text/)
  expect(component).toBeTruthy()
})

test('One TermsOfUseCheckbox is checked', () => {
  const onChangeFn = jest.fn()
  const tree = render(
    <TermsOfUseCheckbox
      id="test-checkbox"
      onChange={onChangeFn}
    />)
  const checkbox = tree.container.querySelector('input')
  fireEvent.click(checkbox)
  expect(onChangeFn).toHaveBeenCalledTimes(1)
})
