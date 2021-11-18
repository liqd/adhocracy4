import React from 'react'
import { intComma } from './helpers'

export const ListItemBadges = (props) => {
  const getModeratorChoice = () => {
    return props.moderatorChoices.find(choice => {
      return choice[0] === props.moderatorFeedback
    })
  }

  return (
    <div className="list-item__labels">
      {props.category &&
        <span className="label label--big">
          {props.category.name}
        </span>}
      {props.pointLabel &&
        <span class="label label--big">
          <i class="fas fa-map-marker-alt" aria-hidden="true" />
          {props.pointLabel}
        </span>}
      {props.budget > 0 &&
        <span className="label label--big">
          {intComma(props.budget)}€
        </span>}
      {props.moderatorFeedback &&
        <span
          className={
          'label' +
          ' label--big' +
          ' label--' + props.moderatorFeedback.toLowerCase() +
          ' list-item__label--moderator-feedback'
          }
        >
          {getModeratorChoice()[1]}
        </span>}
    </div>
  )
}
