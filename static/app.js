const recipeInfo = $('#recipe-info')
const addLikeBtn = $('.fav')
recipeInfo.on('click', '.fav', handleFavorite)

async function handleFavorite(e) {
	e.preventDefault()
	// e.stopPropagation()
	const id = $(e.target).parent().data('id')
	console.log(id)

	if (e.target.classList.contains('fas')) {
		await axios.delete(`/api/favorite/${id}`)
		$(e.target).toggleClass('fas fa-heart')
		$(e.target).toggleClass('far fa-heart')
		// $(e.target).remove()    // .hide()
		console.log('Delete Unfavorite Recipe')
	} else {
		try {
			await axios.post(`/api/favorite/${id}`, (data = { id: id }))
			$(e.target).toggleClass('fas fa-heart')
			$(e.target).toggleClass('far fa-heart')
			console.log('Add Favorite Recipe')
		} catch (err) {
			console.log('Login Required', err)
		}
	}
}

// $('.fav').click(deleteFav)
// async function deleteFav() {
//   const id = $(this).data('id')
//   await axios.delete(`/api/favorite/${id}`)
//   $(this).parent().remove()
// }

$(handleFavorite);
