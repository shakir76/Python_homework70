async function makeRequest(url, method = 'GET') {
    let response = await fetch(url, {method});

    if (response.ok) {
        return await response.json();
    } else {
        let error = new Error(response.statusText);
        error.response = response;
        throw error;
    }
}
async function buttonOnClick(event) {
    event.preventDefault();
    let target = event.target
    let url = target.dataset.new
    let response = await makeRequest(url)
    let like = document.getElementsByClassName('like-count')
    for (a of like) {
        if (a.dataset.new === url) {
            a.innerText = `Лайки: ${response.test}`
        }
    }
    if (response.user === true) {
        target.innerText = "Дизлайк"
    } else {
        target.innerText = "Лайк"
    }
}


function getArticles() {
    let buttons = document.getElementsByClassName('news')
    for (button of buttons) {
        button.addEventListener('click', buttonOnClick)
    }
}

window.addEventListener('load', getArticles)