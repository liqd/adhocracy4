import api from '../../../static/api'
import type { RatingResponse } from '../../../static/api/types'

export interface RatingCounts {
  positive: number
  negative: number
}

export interface UserRatingData {
  userRating?: number | null
  userHasRating: boolean
  userRatingId?: number | null
}

export type CreateRatingResult = [RatingCounts, UserRatingData, RatingResponse]

interface ApiError {
  status: number
  responseJSON: unknown[]
}

/**
 * @param number - the rating value, can be -1, 0 or 1
 * @param objectId - the object to be rated
 * @param contentTypeId - the content type id of the object
 * @returns an array with the rating data (number of negative
 *    and positive ratings) and the user rating data (value and id and userHasRating)
 *    and the complete response data from the API.
 */
export async function createRating (number: number, objectId?: string | number, contentTypeId?: string | number): Promise<CreateRatingResult> {
  try {
    const data = await api.rating.add({
      urlReplaces: {
        objectPk: objectId,
        contentTypeId
      },
      value: number
    })

    return [{
      positive: data.meta_info.positive_ratings_on_same_object,
      negative: data.meta_info.negative_ratings_on_same_object
    }, {
      userRating: data.meta_info.user_rating_on_same_object_value,
      userHasRating: true,
      userRatingId: data.id
    }, data]
  } catch (error) {
    const e = error as ApiError
    // if the server responds with a 400 and an array with a single integer
    // the user has voted in the meantime. This handles the case and instead
    // uses the returned ID to modify the rating.
    if (e.status === 400 &&
        e.responseJSON.length === 1 &&
        Number.isInteger(parseInt(e.responseJSON[0] as string, 10))
    ) {
      const userRatingId = parseInt(e.responseJSON[0] as string, 10)
      const [ratings, userState, data] = await modifyRating(number, userRatingId)
      return [
        ratings,
        {
          ...userState,
          userHasRating: true,
          userRatingId
        },
        data
      ]
    }
    throw error
  }
}

/**
 * @param number - the rating value, can be -1, 0 or 1
 * @param id - the id of the users rating
 * @param objectId - the object to be rated
 * @param contentTypeId - the content type id of the object
 * @returns an array with the rating data (number of negative
 * and positive ratings) and the user rating data (value)
 * and the complete response data from the API.
 */
export async function modifyRating (number: number, id: number | null | undefined, objectId?: string | number, contentTypeId?: string | number): Promise<CreateRatingResult> {
  const data = await api.rating.change({
    urlReplaces: {
      objectPk: objectId,
      contentTypeId
    },
    value: number
  }, id)
  return [
    {
      positive: data.meta_info.positive_ratings_on_same_object,
      negative: data.meta_info.negative_ratings_on_same_object
    },
    {
      userRating: data.meta_info.user_rating_on_same_object_value,
      userHasRating: number !== 0
    },
    data
  ]
}

/**
 * Helper function to easily create OR modify a rating
 *
 * @param number - the rating value, can be -1, 0 or 1
 * @param objectId - the object to be rated
 * @param contentTypeId - the content type id of the object
 * @param id - the id of the users rating
 * @returns an array with the rating data (number of negative
 * and positive ratings) and the user rating data (value)
 * and the complete response data from the API.
 */
export async function createOrModifyRating (number: number, objectId?: string | number, contentTypeId?: string | number, id?: number | null): Promise<CreateRatingResult> {
  if (id) {
    return await modifyRating(number, id, objectId, contentTypeId)
  } else {
    return await createRating(number, objectId, contentTypeId)
  }
}
