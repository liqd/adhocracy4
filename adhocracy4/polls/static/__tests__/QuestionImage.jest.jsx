import React from 'react'
import { render, screen } from '@testing-library/react'

import QuestionImage from '../PollDetail/QuestionImage'

describe('QuestionImage', () => {
  it('renders nothing without an image URL', () => {
    const { container } = render(<QuestionImage imageUrl={null} alt="Alt" />)
    expect(container).toBeEmptyDOMElement()
  })

  it('renders the image with alt text', () => {
    render(<QuestionImage imageUrl="/media/test.png" alt="Alt" />)
    expect(screen.getByRole('img')).toHaveAttribute('src', '/media/test.png')
    expect(screen.getByRole('img')).toHaveAttribute('alt', 'Alt')
  })
})
