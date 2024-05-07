let header;
let loginForm;
let registerForm;
let postsList;
let userProfile;
let newPost;
let newPostContent;
let pagination;
let csrf;

document.addEventListener('DOMContentLoaded', (event) => {
    header = document.querySelector('#header');
    loginForm = document.querySelector('#login');
    registerForm = document.querySelector('#register');
    postsList = document.querySelector('#posts');
    userProfile = document.querySelector('#user-profile');
    newPost = document.querySelector('#new-post');
    newPostContent = document.querySelector('#new-post-content');
    pagination = document.querySelector('#pagination');
    csrf = document.querySelector('input[name="csrfmiddlewaretoken"]');
    getPosts('all', 1)
})

function getPosts(type, page) {
    clearAll();
    changeHeader(type);

    fetch(`posts/${type}/${page}`)
    .then(response => response.json())
    .then(response => {

        if (type === 'all' && response.authenticated) {
        newPost.style.display = 'block';
        }

        renderPosts(response, type, page)
    });
}

function getProfile(userId) {
    clearAll();

    fetch(`user/${userId}`)
        .then(response => response.json())
        .then(response => {
            userProfile.innerHTML = `
<p>${response.username}</p>
<p>Followers: ${response.followers}</p>
<p>Following: ${response.following}</p>
<p id="follow"></p>
`;

            if (response.followable) {
                const followButton = document.createElement('button');
                followButton.classList.add('follow-button');
                followButton.textContent = 'Follow';

                followButton.addEventListener('click', () => {
                    fetch(`user/follow/${userId}`)
                        .then(response => getProfile(userId));
                })

                userProfile.querySelector('#follow').appendChild(followButton);
            } else if (response.unfollowable) {
                const unfollowButton = document.createElement('button');
                unfollowButton.classList.add('unfollow-button');
                unfollowButton.textContent = 'Unfollow';

                unfollowButton.addEventListener('click', () => {
                    fetch(`user/follow/${userId}`)
                        .then(response => getProfile(userId));
                })

                userProfile.querySelector('#follow').appendChild(unfollowButton);
            }
            userProfile.style.display = 'block';
            renderPosts(response)
        })
}

function createPost() {
    const content = newPostContent.value;
    console.log(csrf.value)

    fetch("posts/new", {
    method: 'POST',
    headers: {
        'X-CSRFToken': csrf.value,
    },
    body: JSON.stringify({
        content: content,
    })})
        .then(response => getPosts('all', 1));
}

function editPost(postId) {
    const post = document.querySelector(`[data-postId="${postId}"]`);

    const postContentArea = post.querySelector(`.content`);
    const postContent = postContentArea.innerHTML;
    const postEditArea = document.createElement('textarea');
    postEditArea.classList.add('post-area');
    postEditArea.value = postContent;

    postContentArea.innerHTML = '';
    postContentArea.appendChild(postEditArea);
    post.querySelector('#edit-button').style.display = 'none';

    const saveButton = document.createElement('button');
    saveButton.textContent = 'Save';
    saveButton.classList.add('save-button');
    saveButton.addEventListener('click', event => {
        const newPostContent = postEditArea.value;

        fetch(`posts/edit/${postId}`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrf.value,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                content: newPostContent,
                test: "xd"
            })})
        .then(response => {
            postContentArea.innerHTML = `<p id="content">${newPostContent}</p>`;
            post.querySelector('#edit-button').style.display = 'block';
        });
    });

    postContentArea.appendChild(saveButton);
}

function likePost(postId) {
    fetch(`posts/like/${postId}`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrf.value,
                'Content-Type': 'application/json'
            }})
        .then(response => response.json())
        .then(response => {
            const post = document.querySelector(`[data-postId="${postId}"]`);
            const likesButton = post.querySelector('.likes-button');
            const previousLikes = parseInt(likesButton.textContent.substring(2));
            likesButton.textContent = '❤️';

            if (response.liked) {
                likesButton.textContent = '❤️ ' + (previousLikes + 1);
                likesButton.classList.add('liked-post');
            } else {
                likesButton.classList.remove('liked-post');
                likesButton.textContent = '❤️ ' + (previousLikes - 1);
            }
        })
}

function renderPosts(response, type, page) {
    let posts = response.posts

    posts.forEach(post => {
                const postElement = document.createElement('div');
                postElement.classList.add('post');
                postElement.setAttribute(`data-postId`, post.id);

                postElement.innerHTML = `
<h6><a class="user-link" href="" onclick="getProfile(${post.author_id}); return false;">${post.author}</a></h6>
<p class="edit"></p>
<p class="content">${post.content}</p>
<p class="timestamp">${post.timestamp}</p>
<button class="likes-button">❤️ ${post.likes}</button>
`;

                if (post.is_editable) {
                    postElement.querySelector('.edit').innerHTML = `<button class="edit-button" id="edit-button" onclick="editPost(${post.id})">Edit</button>`
                }

                if (!response.authenticated) {
                    postElement.querySelector('.likes-button').style.pointerEvents = 'none';
                } else {
                    postElement.querySelector('.likes-button').addEventListener('click', () => likePost(post.id));
                }

                if (post.is_liked) {
                    postElement.querySelector('.likes-button').classList.add('liked-post');
                }

                postsList.appendChild(postElement);
            })

            if (response.hasPrevious) {
                const previousButton = document.createElement('button');
                previousButton.innerHTML = '⬅️';
                previousButton.addEventListener('click', event => {
                    getPosts(type, page - 1)
                })

                pagination.appendChild(previousButton)
            }

            if (response.hasNext) {
                const nextButton = document.createElement('button');
                nextButton.innerHTML = '➡️';
                nextButton.addEventListener('click', event => {
                    getPosts(type, page + 1)
                })

                pagination.appendChild(nextButton)
            }
}

function changeHeader(type) {
    if (type === 'all') {
        header.textContent = 'All Posts';
    } else if (type === 'followed') {
        header.textContent = 'Posts from Followed Users';
    } else {
        header.textContent = type;
    }
}

function clearAll() {
    header.textContent = '';
    loginForm.style.display = 'none';
    registerForm.style.display = 'none';
    userProfile.style.display = 'none';
    newPost.style.display = 'none';
    newPostContent.value = '';
    postsList.innerHTML = '';
    pagination.innerHTML = '';
}

function login() {
    clearAll();
    changeHeader('Login');
    loginForm.style.display = 'block';
}

function register() {
    clearAll();
    changeHeader('Register');
    registerForm.style.display = 'block';
}
