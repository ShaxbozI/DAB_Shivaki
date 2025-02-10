document.addEventListener('DOMContentLoaded', ()=>{

    const navDropdown = document.querySelector('#navbarNavDropdown .dropdown-toggle')
    const dropdownItems = document.querySelectorAll('#navbarNavDropdown .dropdown-item') 

    dropdownItems.forEach((item)=>{
        if(item.classList.contains('active')){
            navDropdown.classList.add('active')
            navDropdown.classList.add('fw-bold')
        }
    })


















    const ratingLabel = document.querySelectorAll('.rating label')
    const ratingFormInput = document.querySelector('.stars_given input')

    ratingLabel.forEach((label, id)=>{
        label.addEventListener('click', ()=>{
            if(id+1 == 5){
                ratingFormInput.value = 1
            } else if(id+1 == 4){
                ratingFormInput.value = 2
            } else if(id+1 == 3){
                ratingFormInput.value = 3
            } else if(id+1 == 2){
                ratingFormInput.value = 4
            } else if(id+1 == 1){
                ratingFormInput.value = 5
            }
        })
    })

 
})