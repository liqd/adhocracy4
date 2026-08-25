import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'
import { Select } from '../Select'

describe('Select', () => {
  test('is displaying with choices', () => {
    render(
      <Select
        choices={[
          ['1', 'choice1'],
          ['2', 'choice2']
        ]}
        label="My Label"
      />
    )
    const choice1Element = screen.getByText(/(choice1)/)
    const label = screen.getByText(/My Label/)
    expect(choice1Element).toBeTruthy()
    expect(label).toBeTruthy()
  })

  test('Label is linked with select', () => {
    render(
      <Select
        choices={[
          ['1', 'choice1'],
          ['2', 'choice2']
        ]}
        id="TestId"
        label="My Label"
      />
    )
    const select = screen.getByLabelText(/My Label/)
    expect(select).toBeTruthy()
  })

  test('calls onSelect', () => {
    const onSelect = jest.fn()
    render(
      <Select
        choices={[
          ['1', 'choice1'],
          ['2', 'choice2']
        ]}
        id="TestId"
        label="My Label"
        onSelect={onSelect}
      />
    )
    const select = screen.getByLabelText(/My Label/)
    fireEvent.change(select, { target: { value: '1' } })
    expect(onSelect).toHaveBeenCalled()
  })

  test('creates placeholder', () => {
    render(
      <Select
        choices={[
          ['1', 'choice1'],
          ['2', 'choice2']
        ]}
        id="TestId"
        label="My Label"
        placeholder="My placeholder"
      />
    )
    const choice1Element = screen.getByText(/(My placeholder)/)
    expect(choice1Element).toBeTruthy()
  })
})
