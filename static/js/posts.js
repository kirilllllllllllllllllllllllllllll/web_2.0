const likes = document.querySelectorAll('.post_like')

likes.forEach(elem => {
    elem.addEventListener('click', (event)=> {
        const classList_ = event.target.classList 
        if (classList_.contains('post_like_liked')) {
            classList_.remove('post_like_liked')
        }
        else {
            classList_.add('post_like_liked')
        }
    })
})

const detailsBlock = document.querySelector('.menu__deatils-block')
const detailsContent = detailsBlock.querySelector('.menu__list')
detailsBlock.addEventListener("toggle", (event) => {
    if (detailsBlock.open) {
      /* the element was toggled open */
      detailsContent.style.animation = 'slide .5s ease-in-out'
    } else {
      /* the element was toggled closed */
      detailsContent.style.animation = 'slide-back .3s ease-in-out'
      console.log(0);
    }
  });