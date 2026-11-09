import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'

jest.mock('django', () => ({
  gettext: (text) => text
}))

const mockOpenModal = jest.fn()
const mockUppy = {
  use: jest.fn(),
  on: jest.fn(),
  getPlugin: jest.fn(() => ({ openModal: mockOpenModal })),
  getFiles: jest.fn(() => []),
  removeFile: jest.fn(),
  upload: jest.fn(() => Promise.resolve()),
  destroy: jest.fn()
}

jest.mock('@uppy/core', () => ({
  __esModule: true,
  default: jest.fn(() => mockUppy)
}))
jest.mock('@uppy/dashboard', () => ({ __esModule: true, default: jest.fn() }))
jest.mock('@uppy/image-editor', () => ({ __esModule: true, default: jest.fn() }))

import QuestionImageUploadButton from '../PollDashboard/QuestionImageUploadButton'

describe('QuestionImageUploadButton', () => {
  const defaults = {
    id: 'q_1',
    onImageChange: jest.fn(),
    helpText: 'some hint',
    altText: '',
    onAltTextChange: jest.fn()
  }

  it('hides the alt text field when no image is uploaded', () => {
    render(<QuestionImageUploadButton {...defaults} question={{ image_url: null }} />)
    expect(screen.queryByLabelText(/Alt text/)).not.toBeInTheDocument()
  })

  it('shows the alt text field as required when an image is uploaded', () => {
    render(
      <QuestionImageUploadButton
        {...defaults}
        question={{ image_url: '/media/question.png' }}
      />
    )
    expect(screen.getByLabelText(/Alt text/)).toBeRequired()
    expect(screen.getByTitle('This field is required')).toBeInTheDocument()
  })

  it('opens the Uppy image editor', () => {
    render(<QuestionImageUploadButton {...defaults} question={{ image_url: null }} />)
    fireEvent.click(screen.getByLabelText('Upload image'))
    expect(mockOpenModal).toHaveBeenCalled()
  })
})
