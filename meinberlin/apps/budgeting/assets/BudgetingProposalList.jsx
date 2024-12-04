import React, { useEffect, useState, useRef } from 'react'
import django from 'django'
import { BudgetingProposalListItem } from './BudgetingProposalListItem'
import { EndSessionLink } from './EndSessionLink'
import { Pagination } from './Pagination'
import { CountDown } from '../../contrib/assets/CountDown'
import { ControlBar } from './ControlBar'
import { useLocation, useSearchParams } from 'react-router'

export const BudgetingProposalList = (props) => {
  const [data, setData] = useState([])
  const [meta, setMeta] = useState()
  const location = useLocation()
  const [queryParams] = useSearchParams()
  const getVoteCountText = (votes) => {
    const countText = django.ngettext('you have 1 vote left.', 'you have %s votes left.', votes)
    return django.interpolate(countText, [votes])
  }

  const translations = {
    list: django.gettext('Proposals list'),
    noResults: django.gettext('Nothing to show')
  }

  const scrolledRef = useRef(false)

  const fetchProposals = () => {
    const url = props.proposals_api_url + location.search
    fetch(url)
      .then(resp => resp.json())
      .then(json => {
        setData(json.results)
        setMeta({
          total_count: json.count,
          current_page: queryParams.get('page') || 1,
          page_count: json.page_count,
          is_paginated: json.page_count > 1,
          previous: json.previous,
          next: json.next,
          filters: json.filters,
          permissions: json.permissions,
          locale: json.locale,
          token_info: json.token_info,
          page_elided_range: json.page_elided_range
        })
      })
      .catch(error => console.log(error))
  }

  const scrollToProposal = () => {
    if (location.hash && !scrolledRef.current) {
      const id = location.hash.replace('#', '')
      const element = document.getElementById(id)
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' })
        scrolledRef.current = true
      }
    }
  }

  useEffect(fetchProposals, [location.search])
  useEffect(scrollToProposal)

  const renderList = (data) => {
    return (
      <>
        <h2 className="visually-hidden">{translations.list}</h2>
        <ul className="u-list-reset">
          {data.map((proposal, idx) =>
            <BudgetingProposalListItem
              key={'budgeting-proposal-' + idx}
              proposal={proposal}
              locale={meta?.locale}
              permissions={meta?.permissions}
              tokenvoteApiUrl={props.tokenvote_api_url}
              onVoteChange={selectedPage => fetchProposals(selectedPage)}
              currentPage={meta?.current_page}
              votesLeft={
                meta?.token_info
                  ? meta?.token_info.votes_left
                  : false
              }
            />)}
        </ul>
        {meta?.is_paginated &&
          <Pagination
            elidedRange={meta.page_elided_range}
            nextPage={meta.next}
            prevPage={meta.previous}
            pageCount={meta.page_count}
          />}
      </>
    )
  }

  return (
    <>
      {(meta?.permissions.has_voting_permission_and_valid_token) &&
        <div className="module-content--light">
          <div className="container">
            <div className="offset-lg-3 col-lg-6">
              <CountDown
                countText={getVoteCountText(meta?.token_info.num_votes_left)}
                activeClass="btn btn--light btn--full u-spacer-bottom btn--huge u-primary"
                inactiveClass="btn btn--full btn--light u-spacer-bottom btn--huge"
                counter={meta?.token_info.num_votes_left}
              />
              <EndSessionLink
                endSessionUrl={props.end_session_url}
              />
            </div>
          </div>
        </div>}
      <ControlBar
        filters={meta?.filters}
        numOfResults={meta?.total_count}
      />
      <div className="module-content--light">
        <div className="container">
          <div className="offset-lg-2 col-lg-8">
            {Object.keys(data).length > 0
              ? renderList(data)
              : translations.noResults}
          </div>
        </div>
      </div>
    </>
  )
}
