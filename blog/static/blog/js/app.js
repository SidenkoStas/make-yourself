document.addEventListener("DOMContentLoaded", function () {
    // Fetch posts from the backend
    fetch("http://0.0.0.0:8000/blog/posts/")
        .then(response => response.json())
        .then(posts => displayPosts(posts))
        .catch(error => console.error("Error fetching posts:", error));

    // Function to display posts in the frontend
    function displayPosts(posts) {
        const postsContainer = document.getElementById("posts-container");

        posts.forEach(post => {
            const postElement = document.createElement("div");
            postElement.classList.add("post");

            const titleElement = document.createElement("h2");
            titleElement.textContent = post.title;

            const contentElement = document.createElement("p");
            contentElement.textContent = post.content;

            postElement.appendChild(titleElement);
            postElement.appendChild(contentElement);

            postsContainer.appendChild(postElement);
        });
    }
});
