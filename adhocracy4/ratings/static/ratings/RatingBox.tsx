import React, { useCallback, useMemo, useState } from 'react'
import django from 'django'

import { createOrModifyRating, type RatingCounts, type UserRatingData } from './rating_api'
import RatingButton from './RatingButton'
import config from '../../../static/config'

const translations = {
  likes: django.gettext('Likes'),
  dislikes: django.gettext('Dislikes')
}

export const getRedirectUrl = (id?: any) => config.getLoginUrl() + (id ? encodeURIComponent('?comment=' + id) : '')

interface RatingBoxProps {
  positiveRatings?: number
  negativeRatings?: number
  userHasRating?: boolean
  userRating?: number | null
  userRatingId?: number | null
  isReadOnly?: boolean
  contentType?: string | number
  objectId?: string | number
  authenticatedAs?: string | number | null
  isComment?: boolean
  render?: (renderProps: {
    ratings: RatingCounts
    userRatingData: UserRatingData
    isReadOnly?: boolean
    clickHandler: (value: number) => Promise<void>
  }) => React.ReactNode
}

const RatingBox = ({
  positiveRatings = 0,
  negativeRatings = 0,
  userHasRating = false,
  userRating,
  userRatingId,
  isReadOnly = false,
  contentType,
  objectId,
  authenticatedAs,
  isComment,
  render
}: RatingBoxProps) => {
  const [ratings, setRatings] = useState({ negative: negativeRatings, positive: positiveRatings })
  const [userRatingData, setUserRatingData] = useState<UserRatingData>({ userHasRating, userRating, userRatingId })

  const clickHandler = useCallback(async (number: number): Promise<void> => {
    if (!authenticatedAs) {
      const redirectId = isComment ? objectId : null
      window.location.href = getRedirectUrl(redirectId)
    }

    if (isReadOnly) {
      return
    }

    const [newRatings, newUserRatingData] = await createOrModifyRating(number, objectId, contentType, userRatingData.userRatingId)

    setRatings(newRatings)
    setUserRatingData({ ...userRatingData, ...newUserRatingData })
  }, [authenticatedAs, objectId, contentType, userRatingData, isComment, isReadOnly])

  const customChildren = useMemo(() => {
    if (render && typeof render === 'function') {
      return render({ ratings, userRatingData, isReadOnly, clickHandler })
    }
    return null
  }, [clickHandler, isReadOnly, ratings, render, userRatingData])

  // return either custom html from the render prop or the default
  return customChildren ?? (
    <div className="rating" data-testid="rating-box">
      <RatingButton
        isReadOnly={isReadOnly}
        onClick={clickHandler}
        active={userRatingData.userRating === 1}
        rating={1}
        authenticatedAs={authenticatedAs}
      >
        <i className="fa fa-thumbs-up" aria-hidden="true" />{' '}
        {ratings.positive}{' '}
        <span className="rating__label">{translations.likes}</span>
      </RatingButton>
      <RatingButton
        isReadOnly={isReadOnly}
        onClick={clickHandler}
        active={userRatingData.userRating === -1}
        rating={-1}
        authenticatedAs={authenticatedAs}
      >
        <i className="fa fa-thumbs-down" aria-hidden="true" />{' '}
        {ratings.negative}{' '}
        <span className="rating__label">{translations.dislikes}</span>
      </RatingButton>
    </div>
  )
}

export default RatingBox
