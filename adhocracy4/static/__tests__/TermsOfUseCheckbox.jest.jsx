import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'
import { TermsOfUseCheckbox } from '../TermsOfUseCheckbox'

test('One TermsOfUseCheckbox is showing', () => {
  render(<TermsOfUseCheckbox id="test-checkbox" />)
  const component = screen.getByLabelText('Yes, I have read and agree to this organisation\'s %(linkStart)s terms of use %(linkEnd)s.')
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
