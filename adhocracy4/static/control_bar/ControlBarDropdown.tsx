import React from 'react'
import { Select } from '../../forms/static/Select'

type Choice = [string, string]

// FIXME: maybe more elegant way?
// this is only relevant for the first page load,
// where the url does not contain all default query params.
// case 1: if there is a current, get the name of the current
// case 2: if there is a default, get its verbose name
// case 3a: if there is no default and choices has '', get the name of ''
// case 3b: otherwise get name of first choice
const getDefaultName = (f: any, curr: string) => {
  let filterChoice: Choice
  if (f.choices.some((c: Choice) => c[0] === curr)) {
    filterChoice = f.choices.filter((c: Choice) => c[0] === curr)[0]
  } else if (f.default) {
    filterChoice = f.choices.filter((c: Choice) => c[0] === f.default)[0]
  } else {
    const emptyStringIndex = f.choices.findIndex((choice: any) => choice === '')
    filterChoice =
      emptyStringIndex > -1 ? f.choices[emptyStringIndex] : f.choices[0]
  }
  return filterChoice[0]
}

interface ControlBarDropdownProps {
  filter: {
    label: string
    choices: Array<[string, string] | string[]>
    default?: string
  }
  filterId?: string
  current?: string
  onSelectFilter?: (choice: [string, string]) => void
}

export const ControlBarDropdown = (props: ControlBarDropdownProps) => {
  const { filter } = props

  const onSelectFilter = (filterChoice: [string, string]) => {
    if (props.onSelectFilter) props.onSelectFilter(filterChoice)
  }

  return (
    <div className="a4-control-bar__sorting">
      <Select
        label={filter.label}
        choices={filter.choices as Choice[]}
        onSelect={(choice) => onSelectFilter(choice as [string, string])}
        id={props.filterId}
        value={getDefaultName(filter, props.current as string)}
      />
    </div>
  )
}
