import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'

jest.mock('django', () => ({
  gettext: (text) => text
}))

import Uppy from '@uppy/core'
import QuestionImageUploadButton from '../PollDashboard/QuestionImageUploadButton'

const getUppy = () => Uppy.mock.results[Uppy.mock.results.length - 1].value

describe('QuestionImageUploadButton', () => {
  const defaults = {
    id: 'q_1',
    onImageChange: jest.fn(),
    helpText: 'some hint',
    altText: '',
    onAltTextChange: jest.fn()
  }

  beforeEach(() => {
    Uppy.mockClear()
  })

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
    expect(getUppy().getPlugin('Dashboard').openModal).toHaveBeenCalled()
  })

  it('starts the upload when the image editor completes', () => {
    render(<QuestionImageUploadButton {...defaults} question={{ image_url: null }} />)
    const uppy = getUppy()
    const upload = jest.spyOn(uppy, 'upload')

    uppy.emit('file-editor:complete')

    expect(upload).toHaveBeenCalled()
  })

  it('stops the image editor when the upload is canceled', () => {
    render(<QuestionImageUploadButton {...defaults} question={{ image_url: null }} />)
    const uppy = getUppy()

    uppy.emit('file-editor:cancel')

    expect(uppy.getPlugin('ImageEditor').stop).toHaveBeenCalled()
  })
})
