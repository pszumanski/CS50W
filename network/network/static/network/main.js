let page = 0;
let header;
let postsList;
let newPostForm;
let newPostContent;
let pagination;

document.addEventListener('DOMContentLoaded', (event) => {
    header = document.querySelector('#header')
    postsList = document.querySelector('#posts');
    newPostForm = document.querySelector('#new-post');
    pagination = document.querySelectorAll('#pagination');
    newPostContent = document.querySelector('#new-post-content');
    getPosts('all')
})

function getPosts(type) {

    changeHeader(type);

    const authenticated = isAuthenticated();
    changeNewPostForm(type, authenticated);

    fetch(`posts/${type}/${page}`)
        .then(response => response.json())
        .then(response => {
            let posts = response.posts.sort((post1, post2) => post1.timestamp - post2.timestamp);

            //TODO: RENDER POSTS

            posts.forEach(post => {
                const postElement = document.createElement('div');
                postElement.classList.add('post');

                postElement.innerHTML = `post${post.id}`;

                postsList.appendChild(postElement);
            })

            if (response.hasNext) {
                //TODO: renderNextButton
            }

            if (page > 0) {
                //TODO: renderPreviousButton
            }
        });
}

function changeHeader(type) {
    if (type === 'all') {
        header.textContent = 'All Posts';
    }
    if (type === 'followed') {
        header.textContent = 'Posts from Followed Users';
    }
}

function changeNewPostForm(type, authenticated) {
    if (type === 'all' && authenticated) {
        newPostForm.style.display = 'block';
    } else {
        newPostForm.style.display = 'none';
    }
}

function getUser(userId) {

}

function isAuthenticated() {
    return fetch('authenticated')
        .then(response => response.json())
        .then(response => response.authenticated);
}

function createPost() {
    const content = newPostContent.value;
    console.log(content)

    fetch("posts/new", {
    method: 'POST',
    body: JSON.stringify({
        content: content
    })});

}
