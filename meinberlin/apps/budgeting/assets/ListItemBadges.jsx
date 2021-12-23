import React from 'react'
import { intComma } from './helpers'
import { SpacedSpan } from './SpacedSpan'

export const ListItemBadges = props => {
  return (
    <div className="list-item__labels">
      {props.category && (
        <SpacedSpan className="label label--big">
          {props.category.name}
        </SpacedSpan>
      )}
      {props.pointLabel && (
        <SpacedSpan className="label label--big">
          <i className="fas fa-map-marker-alt" aria-hidden="true" />
          <SpacedSpan>{props.pointLabel}</SpacedSpan>
        </SpacedSpan>
      )}
      {props.budget > 0 && (
        <SpacedSpan className="label label--big">
          {intComma(props.budget)}€
        </SpacedSpan>
      )}
      {props.moderatorFeedback[0] && (
        <SpacedSpan
          className={
            'label' +
            ' label--big' +
            ' label--' +
            props.moderatorFeedback[0].toLowerCase() +
            ' list-item__label--moderator-feedback'
          }
        >
          {props.moderatorFeedback[1]}
        </SpacedSpan>
      )}
    </div>
  )
}
