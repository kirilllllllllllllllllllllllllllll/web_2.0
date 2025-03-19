const page = 'posts'

const likes = document.querySelectorAll('.post_like')
const posts = document.querySelector('.posts')

if (localStorage.getItem("currentPage") == page) {
  posts.scroll(0, localStorage.getItem('postsY'))
}
localStorage.setItem('currentPage', page)

likes.forEach(elem => {
    elem.addEventListener('click', (event)=> {
      localStorage.setItem('postsY', posts.scrollTop)
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
    }
});

