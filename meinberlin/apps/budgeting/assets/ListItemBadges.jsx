import React from 'react'
import { intComma } from './helpers'
import { SpacedSpan } from './SpacedSpan'
import django from 'django'

const translated = {
  more: django.gettext('More')
}

export const ListItemBadges = props => {
  // combine css class names to match different styling, depending
  // on if it is moderator_feedback or on of the others (category, label etc.)
  const getClass = (badge) => {
    const labelClass = 'label label--big'
    if (badge.type !== 'modFeedback') {
      return labelClass
    }
    const modTypeClass = `label--${badge.value[0].toLowerCase()}`
    return `${labelClass} ${modTypeClass}`
  }

  // returning the value.name in case of category or label
  // in case of budget format as intComma
  // in case of modFeedback second item in array
  const getBadgeText = (badge) => {
    if (badge.type === 'pointLabel') {
      return badge.value
    } else if (badge.type === 'budget') {
      return intComma(badge.value) + '€'
    } else if (badge.type === 'modFeedback') {
      return badge.value[1]
    } else if (badge.type === 'category' || badge.type === 'label') {
      return badge.value.name
    }
  }

  // only return icon for pointLabels
  const hasPointLabelIcon = (type) => {
    if (type !== 'pointLabel') {
      return
    }
    return <i className="fas fa-map-marker-alt" aria-hidden="true" />
  }

  return (
    <div className="list-item__labels">
      {props.badges.map((badge, idx) => {
        return (
          <SpacedSpan
            key={`badge_${badge.type}_${idx}`}
            className={getClass(badge)}
          >
            {hasPointLabelIcon(badge.type)}
            {getBadgeText(badge)}
          </SpacedSpan>
        )
      })}
      {props.numOfMoreBadges >= 0 &&
        <SpacedSpan className="label__link label--big">
          <a
            href={props.proposalUrl}
            className="list-item__link"
          >
            {props.numOfMoreBadges + ' ' + translated.more}
          </a>
        </SpacedSpan>}
    </div>
  )
}
