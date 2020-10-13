////////////// function for ads-content start ////////////////

function slide_with_time() {
    let i = 1;
    setInterval(() => {
    document.getElementById(`i${i++}`).checked = true;
    // i=(i%3)+1
    if (i > 3) {
    i = 1;
    }
    }, 5000)
    }
    slide_with_time()
    
    ////////////// function for ads-content end ////////////////
    
    ////////////// function for carousel -cards end ////////////////
    
    document.querySelectorAll('.container-cards-slides .prev').forEach(item => {
    // console.log(item)
    item.addEventListener('click', (element) => {
    console.log(element.srcElement.parentNode)
    element.srcElement.parentNode.children[0].scrollBy(-window.innerWidth / 1.3, 0)
    });
    });
    document.querySelectorAll('.container-cards-slides .next').forEach(item => {
    // console.log(item)
    item.addEventListener('click', (element) => {
    console.log(element.srcElement.parentNode)
    element.srcElement.parentNode.children[0].scrollBy(window.innerWidth / 1.3, 0)
    });
    });
    
    ////////////// function for carousel -cards start ////////////////