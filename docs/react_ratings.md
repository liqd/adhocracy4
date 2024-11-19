# Ratings Component Documentation
This document is there to provide a documentation about the slightly reworked 
ratings component which allows for more customization in other projects


## Code List

* **RatingBox**:
  Main component for displaying Ratings. This is used both in customized rendering
  as well as default rendering (= the rendering that is used in adhocracy4). It
  is also responsible for all the event handler logic.
* **RatingButton**:
  Button component responsible for displaying accessible rating options and 
  passing the selected rating to the parent component.
* **rating_api**:
  API helper for modifying or creating ratings. Functions return an appropriate
  state. 

Patterns used:
- [Render prop](https://react.dev/reference/react/Children#calling-a-render-prop-to-customize-rendering)

## RatingBox

The `RatingBox` component is the main component for ratings. You use this if you
just want the default a4 `RatingBox` but also if you want to customize it. It is
also responsible for redirecting if the user is not authenticated.

### Props

* **positiveRatings**: Number of initial positive ratings
* **negativeRatings**: Number of initial negative ratings
* **userHasRating**: Boolean if the user initially has already rated
* **userRating**: Value of the initial user rating (-1, null or 1)
* **userRatingId**: Id of the user rating object
* **isReadOnly**: Boolean if the rating box should be read only
* **contentType**: ID of the content type to be rated
* **objectId**: ID of the object to be rated
* **authenticatedAs**: Currently authenticated user or null
* **isComment**: Boolean if the rating is for a comment
* **render**: This prop is used to provide custom rendering

### Custom Rendering
If your project needs something that's different than what a4 provides you with
styling-wise, you can use the `render` prop to provide your own rendering. To do
so, you pass a function to the `render` prop. The function will receive the
following props:

* **ratings**: An object with the following keys, representing the number of rates
    * **positive**: Number of positive ratings
    * **negative**: Number of negative ratings
* **userRatingData**: An object with the following keys, representing the user state
    * **userHasRating**: Boolean if the user has already rated
    * **userRating**: Value of the user rating (-1, null or 1)
    * **userRatingId**: Id of the user rating object or null
* **isReadOnly**: Boolean if the rating box should be read only
* **clickHandler**: Add this function to the element that should trigger the rating
    and pass the rating value to it (-1, 0 or 1)

Here an example if you would want to set the number of ratings in parentheses instead:

```jsx
<RatingBox {...otherProps} render={({ ratings, userRatingData, isReadOnly, clickHandler }) => (
  <>
    <button onClick={() => clickHandler(-1)}>dislike ({ratings.negative})</button>
    <button onClick={() => clickHandler(-1)}>like ({ratings.positive})</button>
  </>
)} />
```

## RatingButton

The `RatingButton` component is a button component that is used to display
accessible rating options and pass the selected rating to the provided click handler.

### Props

* **rating**: The value of the rating for this button (-1 or 1)
* **active**: Whether the user has selected this rating
* **onClick**: Function to be called when a rating is selected
* **authenticatedAs**: Currently authenticated user or null
* **isReadOnly**: Boolean if the rating button should be read only
* **children**: The content you want to render inside the button

The last two props are only used to redirect to a specific comment if the user
is not authenticated.

### Styling
You can style the rating buttons with the following classes:

* **rating-button**: The base class for the rating button
* **rating-down**: The class for the down rating button
* **rating-up**: The class for the up rating button
* **is-selected**: The class for the selected rating button
* **.rating-button[disabled]**: The selector for a disabled rating button
  * The button will only be disabled if **both** of the following are true:
    * The user is not authenticated
    * The rating is read only

## RatingApi

This is a set of functions made to help communicating with the ratings api. There
is also a convenience function called createOrModifyRating that allows you to
create or modify a rating in one go.

### createRating
A function that creates a rating, given the following parameters:

* **number**: Value of the rating (-1, 0 or 1)
* **objectId**: ID of the object to be rated
* **contentType**: ID of the content type to be rated

### modifyRating
A function that modifies a rating, given the following parameters:

* **number**: Value of the rating (-1, 0 or 1)
* **id**: ID of the rating to be modified
* **objectId**: ID of the object to be rated
* **contentType**: ID of the content type to be rated

### createOrModifyRating
A convenience function that allows you to create or modify a rating in one go,
given the following parameters:

* **number**: Value of the rating (-1, 0 or 1)
* **objectId**: ID of the object to be rated
* **contentType**: ID of the content type to be rated
* **id (optional)**: ID of the rating to be modified
