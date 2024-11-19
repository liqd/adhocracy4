import api from '../../../static/api'

/**
 * @param {number} number - the rating value, can be -1, 0 or 1
 * @param {string} objectId - the object to be rated
 * @param {string} contentTypeId - the content type id of the object

 * @returns {Promise<Array>} - an array with the rating data (number of negative
 *    and positive ratings) and the user rating data (value and id and userHasRating)
 *    and the complete response data from the API.
 */
export async function createRating (number, objectId, contentTypeId) {
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
    // if the server responds with a 400 and an array with a single integer
    // the user has voted in the meantime. This handles the case and instead
    // uses the returned ID to modify the rating.
    if (error.status === 400 &&
        error.responseJSON.length === 1 &&
        Number.isInteger(parseInt(error.responseJSON[0]))
    ) {
      const userRatingId = parseInt(error.responseJSON[0])
      const [ratings, userState, data] = (await modifyRating(number, userRatingId))[0]
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
  }
}

/**
 * @param {number} number - the rating value, can be -1, 0 or 1
 * @param {number} id - the id of the users rating
 * @param {string} objectId - the object to be rated
 * @param {string} contentTypeId - the content type id of the object

 * @returns {Promise<Array>} - an array with the rating data (number of negative
 * and positive ratings) and the user rating data (value)
 * and the complete response data from the API.
 */
export async function modifyRating (number, id, objectId, contentTypeId) {
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
 * @param {number} number - the rating value, can be -1, 0 or 1
 * @param {string} objectId - the object to be rated
 * @param {string} contentTypeId - the content type id of the object
 * @param {number} [id] - the id of the users rating

 * @returns {Promise<Array>} - an array with the rating data (number of negative
 * and positive ratings) and the user rating data (value)
 * and the complete response data from the API.
 */
export async function createOrModifyRating (number, objectId, contentTypeId, id) {
  if (id) {
    return await modifyRating(number, id, objectId, contentTypeId)
  } else {
    return await createRating(number, objectId, contentTypeId)
  }
}
