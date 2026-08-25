declare module 'react-slick' {
  import * as React from 'react'
  export interface SliderProps {
    arrows?: boolean
    speed?: number
    slidesToShow?: number
    slidesToScroll?: number
    className?: string
    infinite?: boolean
    centerMode?: boolean
    centerPadding?: string
    prevArrow?: React.ReactElement
    nextArrow?: React.ReactElement
    children?: React.ReactNode
    [key: string]: any
  }
  export default class Slider extends React.Component<SliderProps> {}
}