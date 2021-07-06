import React from 'react'
import Slider from 'react-slick'

const SimpleSlider = (props) => {
  const settings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1
  }

  const sliderData = props.sliderData

  return (
    <div>
      <Slider {...settings}>
        {sliderData.map((slide, index) => {
          return (
            <div className="react-slider" key={index}>
              {props.sliderText}
            </div>
          )
        })}
      </Slider>
    </div>
  )
}

export default SimpleSlider
