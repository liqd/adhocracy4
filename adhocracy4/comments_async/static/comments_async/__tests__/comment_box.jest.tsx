import React from 'react'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import '@testing-library/jest-dom'
import CommentBox from '../comment_box'
import api from '../../../../static/api'

jest.mock('../../../../static/api')

const mockedApi = api as any

afterEach(() => {
  jest.clearAllMocks()
})

describe('CommentBox Component', () => {
  const defaultProps: any = {
    anchoredCommentId: null,
    id: 0,
    noControlBar: false,
    subjectId: 0,
    subjectType: 108,
    useModeratorMarked: null,
    withCategories: false
  }

  test('renders CommentBox', () => {
    mockedApi.comments.setComments({
      results: []
    })
    render(<CommentBox {...defaultProps} />)
  })

  test('comments are fetched and loading spinners is hidden', () => {
    mockedApi.comments.setComments({ results: [] })
    const tree = render(<CommentBox {...defaultProps} />)
    expect(tree).toMatchSnapshot()

    expect(mockedApi.comments.get).toHaveBeenCalledTimes(1)
    const loading = screen.getByText(/Loading.../)
    expect(loading.closest('div')).toHaveClass('d-none')
  })

  test('more comments are fetched on scroll', async () => {
    const mockFetch = jest.fn().mockResolvedValue({
      json: () => {
        return { results: [] }
      }
    })
    ;(globalThis as any).fetch = mockFetch
    mockedApi.comments.setComments({
      results: [],
      next: 'https://liqd.net/next_comments'
    })
    render(<CommentBox {...defaultProps} />)
    expect(mockedApi.comments.get).toHaveBeenCalledTimes(1)
    const loading = screen.getByText(/Loading.../)
    expect(loading.closest('div')).toHaveClass('d-none')
    fireEvent.scroll(window, { y: 500 })
    await waitFor(() => {
      expect(mockFetch).toHaveBeenCalledTimes(1)
      expect(mockFetch).toHaveBeenCalledWith('https://liqd.net/next_comments')
    })
  })
})
