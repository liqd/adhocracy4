import React from 'react'
import { render } from '@testing-library/react'
import ChapterNav from '../ChapterNav'

test('Chapter Nav with items', () => {
  const mockedChapter = {
    id: 'chapter_key',
    name: 'chapter_name',
    paragraphs: []
  }
  const tree = render(
    <ChapterNav activeChapter={mockedChapter} chapters={[mockedChapter]} />
  )
  const chapterNavItem = tree.container.querySelector('li')
  expect(chapterNavItem).toBeTruthy()
})
