import React from 'react'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import '@testing-library/jest-dom'
import CommentBox from '../comment_box'
import api from '../../../../static/api'

jest.mock('../../../../static/api')

afterEach(() => {
  jest.clearAllMocks()
})

describe('CommentBox Component', () => {
  const defaultProps = {
    anchoredCommentId: null,
    id: 0,
    noControlBar: false,
    subjectId: 0,
    subjectType: 108,
    useModeratorMarked: null,
    withCategories: false
  }

  test('renders CommentBox', () => {
    api.comments.setComments({
      results: []
    })
    render(<CommentBox {...defaultProps} />)
  })

  test('comments are fetched and loading spinners is hidden', () => {
    api.comments.setComments({ results: [] })
    const tree = render(<CommentBox {...defaultProps} />)
    expect(tree).toMatchSnapshot()

    expect(api.comments.get).toHaveBeenCalledTimes(1)
    const loading = screen.getByText(/Loading.../)
    expect(loading.closest('div')).toHaveClass('d-none')
  })

  test('more comments are fetched on scroll', async () => {
    global.fetch = jest.fn().mockResolvedValue({
      json: () => {
        return { results: [] }
      }
    })
    api.comments.setComments({
      results: [],
      next: 'https://liqd.net/next_comments'
    })
    render(<CommentBox {...defaultProps} />)
    expect(api.comments.get).toHaveBeenCalledTimes(1)
    const loading = screen.getByText(/Loading.../)
    expect(loading.closest('div')).toHaveClass('d-none')
    fireEvent.scroll(window, { y: 500 })
    await waitFor(() => {
      expect(fetch).toHaveBeenCalledTimes(1)
      expect(fetch).toHaveBeenCalledWith('https://liqd.net/next_comments')
    })
  })
})
