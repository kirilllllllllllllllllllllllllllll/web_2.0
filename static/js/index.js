$(function () {
    $(".advantages__slider").slick({
        arrows: true,
        dots: false,
        adaptiveHeight: false,
        slidesToShow: 1,
        slidesToScroll: 1,
        speed: 1000,
        easing: 'linear',
        infinite: true,
        initialSlide: 1,
        autoplay: false,
        autoplaySpeed: 700,
        pauseOnFocus: true,
        pauseOnHover: true,
        pauseOnDotsHover: true,
        draggable: true,
        swipe: true,
        touchThreshold: 5,
        touchMove: true,
        waitForAnimate: true,
        centerMode: true,
        variableWidth: true,
        rows: 1,
        slidesPerRow: 1,
        vertical: false,
        verticalSwiping: false,
        fade: false,
    })
})
const tabs = document.querySelectorAll('.roles__nav-el')
const tabs__content = document.querySelectorAll('.roles__block')
console.log(tabs__content);

tabs.forEach((tab, index) => {
    tab.addEventListener('click', (e) => {
        tabs.forEach(tab => { tab.classList.remove('roles__nav-el_active') })
        e.target.classList.add('roles__nav-el_active')

        var line = document.querySelector('.line')
        line.style.width = e.target.offsetWidth-70 + "px"
        line.style.left = e.target.offsetLeft+35 + "px"

        tabs__content.forEach(tab__content => { tab__content.style.display = 'none' })
        tabs__content[index].style.display = 'flex'

    })
}) 
