import React from 'react'
import { ControlBarDropdown } from '../../../static/control_bar/ControlBarDropdown'
import { ControlBarSearch } from '../../../static/control_bar/ControlBarSearch'
import django from 'django'

const translated = {
  showFilters: django.gettext('Show more'),
  hideFilters: django.gettext('Show less'),
  ordering: django.gettext('Ordering')
}

interface CommentControlBarProps {
  sorts: Record<string, string>
  search?: string
  sort: string
  handleClickFilter: (choice: string[]) => void
  handleSearch: (search: string) => void
}

export const CommentControlBar = (props: CommentControlBarProps) => {
  const filterArray = Object.keys(props.sorts).map((key) => [key, props.sorts[key]])
  const filter = { choices: filterArray, label: translated.ordering }

  return (
    <div className="a4-comments__comment-control-bar">
      <div className="form-group form-group--inline">
        <div className="form-group">
          <ControlBarSearch
            onSearch={(value: string) => props.handleSearch(value)}
            term={props.search}
            placeholder={undefined}
          />
        </div>
        <div className="form-group">
          <ControlBarDropdown
            key="ordering_dropdown"
            filter={filter}
            current={props.sort}
            filterId="id_ordering"
            onSelectFilter={props.handleClickFilter}
          />
        </div>
      </div>
    </div>
  )
}
