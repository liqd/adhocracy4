import React from 'react'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import '@testing-library/jest-dom'
import CommentForm from '../comment_form'

describe('CommentForm Component', () => {
  const defaultProps = {
    agreedTermsOfUse: false,
    useTermsOfUse: false,
    subjectId: 108,
    subjectType: 107,
    hasCommentingPermission: true,
    onCommentSubmit: jest.fn().mockResolvedValue()
  }

  test('renders CommentForm', () => {
    const tree = render(<CommentForm {...defaultProps} />)
    expect(tree).toMatchSnapshot()
  })

  test('submit button cannot be pressed multiple times', async () => {
    render(<CommentForm {...defaultProps} />)

    const textarea = screen.getByLabelText(/Your comment/)
    const submitButton = screen.getByRole('button', { name: 'Post' })
    // button should be enabled before submit
    expect(submitButton).not.toBeDisabled()

    fireEvent.change(textarea, { target: { value: 'this is a new comment' } })
    expect(screen.getByText(/this is a new comment/)).toBeInTheDocument()
    // click button first time
    fireEvent.click(submitButton)
    // button should be disabled
    expect(submitButton).toBeDisabled()
    // click again
    fireEvent.click(submitButton)
    fireEvent.click(submitButton)

    await waitFor(() => {
      // button should be enabled again after submit
      expect(submitButton).not.toBeDisabled()
      // check that form submit has only been triggered once
      expect(defaultProps.onCommentSubmit).toHaveBeenCalledTimes(1)
    })
  })
})
