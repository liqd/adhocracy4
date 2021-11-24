import React from 'react'
import { intComma } from './helpers'
import { SpacedSpan } from './SpacedSpan'

export const ListItemBadges = (props) => {
  const getModeratorChoice = () => {
    return props.moderatorChoices.find(choice => {
      return choice[0] === props.moderatorFeedback
    })
  }

  return (
    <div className="list-item__labels">
      {props.category &&
        <SpacedSpan className="label label--big">
          {props.category.name}
        </SpacedSpan>}
      {props.pointLabel &&
        <SpacedSpan className="label label--big">
          <i className="fas fa-map-marker-alt" aria-hidden="true" />
          {props.pointLabel}
        </SpacedSpan>}
      {props.budget > 0 &&
        <SpacedSpan className="label label--big">
          {intComma(props.budget)}€
        </SpacedSpan>}
      {props.moderatorFeedback &&
        <SpacedSpan
          className={
            'label' +
            ' label--big' +
            ' label--' + props.moderatorFeedback.toLowerCase() +
            ' list-item__label--moderator-feedback'
            }
        >
          {getModeratorChoice()[1]}
        </SpacedSpan>}
    </div>
  )
}
