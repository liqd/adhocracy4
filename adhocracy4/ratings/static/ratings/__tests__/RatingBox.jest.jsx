import React from 'react'
import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import RatingBox from '../RatingBox'
import { createOrModifyRating } from '../rating_api'

jest.mock('../../../../static/config', () => {
  return {
    getLoginUrl: jest.fn().mockReturnValue('/login')
  }
})

jest.mock('../rating_api')

const getData = ({ pos = 1, neg = 0, id = 2, userRating = null } = {}) => {
  const mockData = {
    meta_info: {
      positive_ratings_on_same_object: pos,
      negative_ratings_on_same_object: neg,
      user_rating_on_same_object_value: userRating,
      user_rating_on_same_object_id: 2
    },
    id
  }

  return [{
    positive: mockData.meta_info.positive_ratings_on_same_object,
    negative: mockData.meta_info.negative_ratings_on_same_object
  }, {
    userRating,
    userHasRating: userRating !== null,
    userRatingId: userRating !== null ? 2 : null
  }, mockData]
}

const props = {
  positiveRatings: 1,
  negativeRatings: 0,
  userHasRating: false,
  userRating: null,
  userRatingId: null,
  authenticatedAs: 'someone',
  contentType: 14,
  objectId: 10
}

describe('RatingBox', () => {
  const originalWindow = { ...window }
  const originalLocation = window.location

  beforeAll(() => {
    delete window.location
    window.location = { href: '' }
  })

  beforeEach(() => {
    createOrModifyRating.mockClear()
    window.adhocracy4 = { getCurrentPath: jest.fn(() => '') }
    window.location.href = ''
  })

  afterAll(() => {
    window.location = originalLocation
    Object.assign(window, originalWindow)
  })

  test('component renders', () => {
    render(<RatingBox />)
    const ratings = screen.getByTestId('rating-box')
    const buttons = screen.getAllByRole('button')

    expect(ratings).toBeTruthy()
    expect(buttons).toHaveLength(2)
    expect(buttons[0]).toHaveAccessibleName(/like/i)
    expect(buttons[1]).toHaveAccessibleName(/dislike/i)
  })
  test('updates on click', async () => {
    render(<RatingBox {...props} />)
    const button = screen.getByRole('button', { name: /1 like/i })
    expect(screen.getByRole('button', { name: /0 dislike/i })).toBeInTheDocument()

    createOrModifyRating.mockReturnValue(getData({ pos: 2, userRating: 1 }))
    fireEvent.click(button)
    await waitFor(() => expect(createOrModifyRating).toHaveBeenCalledTimes(1))
    expect(createOrModifyRating).toHaveBeenCalledWith(1, 10, 14, null)
    expect(screen.getByRole('button', { name: /0 dislike/i })).toBeInTheDocument()
    expect(button).toHaveAccessibleName(/2 likes/i)
  })
  test('redirects when not logged in', async () => {
    render(<RatingBox {...props} authenticatedAs={null} />)

    const button = screen.getByRole('button', { name: /1 like/i })
    fireEvent.click(button)

    await waitFor(() => expect(window.location.href).toEqual('/login'))
  })

  test('redirects when not logged in and readonly', async () => {
    render(<RatingBox {...props} authenticatedAs={null} isReadOnly />)

    const button = screen.getByRole('button', { name: /1 like/i })
    fireEvent.click(button)

    await waitFor(() => expect(window.location.href).toEqual('/login'))
  })

  test('redirects to login and specific comment in next parameter', async () => {
    const testProps = {
      ...props,
      authenticatedAs: null,
      isReadOnly: true,
      isComment: true,
      objectId: 2
    }

    render(<RatingBox {...testProps} />)

    const button = screen.getByRole('button', { name: /1 like/i })
    expect(button).toBeInTheDocument()
    fireEvent.click(button)

    await waitFor(() => {
      expect(window.location.href).toEqual('/login%3Fcomment%3D2')
    })
  })
})

describe('RatingBox custom render', () => {
  beforeEach(() => {
    createOrModifyRating.mockClear()
  })
  test('component renders with custom children', async () => {
    render(
      <RatingBox
        {...props} render={
        ({ ratings, userRatingData, isReadOnly, clickHandler }) => (
          <>
            <div data-testid="custom-rating-box">
              {JSON.stringify({ ratings, userRatingData, isReadOnly })}
              <button onClick={() => {
                clickHandler(-1)
              }}
              >
                dislike
              </button>
            </div>
          </>
        )
      }
      />
    )

    const ratings = screen.getByTestId('custom-rating-box')
    expect(ratings).toMatchSnapshot()

    const button = screen.getByRole('button', { name: /dislike/ })
    createOrModifyRating.mockReturnValue(getData())
    fireEvent.click(button)
    await waitFor(() => expect(createOrModifyRating).toHaveBeenCalledTimes(1))
    expect(createOrModifyRating).toHaveBeenCalledWith(-1, 10, 14, null)
  })
})
