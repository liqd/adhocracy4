import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'
import '@testing-library/jest-dom'
import Comment from '../comment'

describe('Comment Component', () => {
  const defaultProps = {
    user_name: 'Participant 1',
    created: 'May 21, 2024, 11:44 a.m.',
    modified: null,
    children: 'This is a test comment.',
    id: 1,
    index: 0,
    positiveRatings: 10,
    negativeRatings: 2,
    user_info: { is_users_own_comment: false },
    userRatng: null,
    userRatingId: null,
    child_comments: [],
    onCommentDelete: jest.fn(),
    onCommentSubmit: jest.fn(),
    onCommentModify: jest.fn(),
    onReplyErrorClick: jest.fn(),
    onEditErrorClick: jest.fn(),
    anchoredCommentId: null,
    anchoredCommentParentId: null,
    has_comment_commenting_permission: true,
    hasCommentingPermission: true,
    wouldHaveCommentingPermission: true,
    projectIsPublic: true,
    content_type: 107,
    comment_content_type: 108,
    useTermsOfUse: false,
    agreedTermsOfUse: false,
    orgTermsUrl: '',
    setCommentError: jest.fn(),
    setCommentEditError: jest.fn()
  }
  const childComment = {
    ai_report: null,
    authorIsModerator: false,
    child_comments: [],
    comment: 'This is a test child comment.',
    comment_categories: null,
    comment_content_type: 108,
    content_type: 107,
    created: '2024-08-07T12:34:56Z',
    displayNotification: false,
    editError: null,
    errorMessage: null,
    moderator_feedback: null,
    modified: undefined,
    object_pk: 1,
    has_comment_commenting_permission: true,
    id: 2,
    index: 0,
    is_deleted: false,
    is_removed: false,
    is_cenesored: false,
    is_blocked: false,
    is_moderator_marked: false,
    ratings: {
      positiveRatings: 0,
      negativeRatings: 0,
      userRating: null,
      userRatingId: null
    },
    replyError: null,
    user_info: {
      is_users_own_comment: false,
      authenticated_user_pk: 0,
      has_viewing_permission: true,
      has_rating_permission: true,
      has_changing_permission: false,
      has_deleting_permission: false,
      has_moderating_permission: false,
      has_comment_commenting_permission: true
    },
    user_name: 'Participant 2',
    user_pk: 1,
    user_profile_url: 'https://liqd.net/profile_url',
    user_image: null,
    user_image_fallback: 'https://liqd.net/profile_image'
  }

  test('renders comment with creator and comment text', () => {
    const tree = render(<Comment {...defaultProps} />)
    expect(tree).toMatchSnapshot()

    expect(screen.getByText(/Participant 1/)).toBeInTheDocument()
    expect(screen.getByText(/This is a test comment./)).toBeInTheDocument()
  })

  test('renders comment with share button', () => {
    render(<Comment {...defaultProps} />)

    expect(screen.getByText(/Share$/)).toBeInTheDocument()
  })

  test('renders comment with creation date', () => {
    render(<Comment {...defaultProps} />)

    expect(screen.getByText(/May 21, 2024, 11:44 a.m./)).toBeInTheDocument()
  })

  test('renders comment with modified date', () => {
    render(<Comment {...defaultProps} modified="May 22, 2024, 11:44 a.m./" />)

    expect(
      screen.queryByText(/May 21, 2024, 11:44 a.m./)
    ).not.toBeInTheDocument()
    expect(screen.getByText(/Latest edit on May 22, 2024, 11:44 a.m./)).toBeInTheDocument()
  })

  test('renders comment with moderator badge', () => {
    const tree = render(<Comment {...defaultProps} authorIsModerator />)
    expect(tree).toMatchSnapshot()

    expect(screen.getByText(/Moderator/)).toBeInTheDocument()
  })

  test('renders deleted comment without child comments correctly', () => {
    render(<Comment {...defaultProps} is_deleted />)

    const creator = screen.getByText(/Participant 1/)
    expect(creator.closest('div')).toHaveClass('a4-comments__deleted-author')
    expect(screen.queryByText(/Share$/)).not.toBeInTheDocument()
    expect(screen.queryByText(/Reply/)).not.toBeInTheDocument()
    expect(screen.queryByText(/reply./)).not.toBeInTheDocument()
  })

  test('renders comment without child comments', () => {
    render(<Comment {...defaultProps} />)

    expect(screen.getByText(/Reply/)).toBeInTheDocument()
    expect(screen.queryByText(/reply./)).not.toBeInTheDocument()
  })

  test('renders comment with child comment', () => {
    render(<Comment {...defaultProps} child_comments={[childComment]} />)

    expect(screen.getByText(/1 reply/)).toBeInTheDocument()
    expect(screen.queryByText(/Reply./)).not.toBeInTheDocument()
  })

  test('toggling reply button toggles child comment', () => {
    render(<Comment {...defaultProps} child_comments={[childComment]} />)

    expect(screen.getByText(/1 reply/)).toBeInTheDocument()
    expect(
      screen.queryByText(/This is a test child comment./)
    ).not.toBeInTheDocument()

    const replyButton = screen.getByRole('button', {
      name: '%s replies1 reply'
    })
    fireEvent.click(replyButton)
    expect(
      screen.getByText(/This is a test child comment./)
    ).toBeInTheDocument()
    fireEvent.click(replyButton)
    expect(
      screen.queryByText(/This is a test child comment./)
    ).not.toBeInTheDocument()
  })

  test('displays ratings correctly', () => {
    render(<Comment {...defaultProps} />)

    expect(screen.getByText('10')).toBeInTheDocument()
    expect(screen.getByText('2')).toBeInTheDocument()
  })

  test('displays user rating correctly', () => {
    render(<Comment {...defaultProps} userRating={1} userRatingsId={0} />)

    const positiveRatings = screen.getByText('10')
    expect(positiveRatings).toBeInTheDocument()
    expect(positiveRatings).toHaveClass('is-selected')
    const negativeRatings = screen.getByText('2')
    expect(negativeRatings).toBeInTheDocument()
    expect(negativeRatings).not.toHaveClass('is-selected')
  })
})
