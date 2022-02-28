import React from 'react'

export const PillBtn = (props) => {
  const {
    removeItemStr,
    onClickRemove,
    choiceBtnID,
    choiceString,
    choiceCount
  } = props

  return (
    <>
      <button
        className="btn btn--transparent btn--small"
        onClick={onClickRemove}
        type="button"
        aria-describedby={choiceBtnID}
      >{choiceString} {choiceCount} <i className="fa fa-times" aria-hidden="true" />
      </button>
      <span id={choiceBtnID} className="visually-hidden">{removeItemStr}</span>
    </>
  )
}
