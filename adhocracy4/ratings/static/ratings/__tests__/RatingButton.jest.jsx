import React from 'react'
import { fireEvent, render, screen } from '@testing-library/react'
import RatingButton from '../RatingButton'

const props = {
  rating: -1,
  active: false,
  onClick: jest.fn(),
  authenticatedAs: 'someone',
  isReadOnly: false,
  children: <span>Children</span>
}

describe('RatingButton', () => {
  beforeEach(() => {
    props.onClick.mockClear()
  })

  test('component renders', () => {
    render(<RatingButton {...props} />)

    const button = screen.getByRole('button')
    expect(button).toBeInTheDocument()

    const children = screen.getByText('Children')
    expect(children).toBeInTheDocument()
  })

  test('updates on click', () => {
    render(<RatingButton {...props} />)

    const button = screen.getByRole('button')
    fireEvent.click(button)

    expect(props.onClick).toHaveBeenCalledTimes(1)
  })
})
