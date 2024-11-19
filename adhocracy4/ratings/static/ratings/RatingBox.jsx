import React, { useCallback, useMemo, useState } from 'react'
import django from 'django'

import { createOrModifyRating } from './rating_api'
import RatingButton from './RatingButton'
import config from '../../../static/config'

const translations = {
  likes: django.gettext('Likes'),
  dislikes: django.gettext('Dislikes')
}

export const getRedirectUrl = (id) => config.getLoginUrl() + (id ? encodeURIComponent('?comment=' + id) : '')

const RatingBox = ({
  positiveRatings,
  negativeRatings,
  userHasRating,
  userRating,
  userRatingId,
  isReadOnly,
  contentType,
  objectId,
  authenticatedAs,
  isComment,
  render
}) => {
  const [ratings, setRatings] = useState({ negative: negativeRatings, positive: positiveRatings })
  const [userRatingData, setUserRatingData] = useState({ userHasRating, userRating, userRatingId })

  const clickHandler = useCallback(async (number) => {
    if (!authenticatedAs) {
      const redirectId = isComment ? objectId : null
      window.location.href = getRedirectUrl(redirectId)
    }

    if (isReadOnly) {
      return null
    }

    const [ratings, newUserRatingData] = await createOrModifyRating(number, objectId, contentType, userRatingData.userRatingId)

    setRatings(ratings)
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
