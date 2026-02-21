// Mobile menu toggle
const menuToggle = document.getElementById('menuToggle');
const navLinks = document.getElementById('navLinks');

menuToggle?.addEventListener('click', () => {
    navLinks.classList.toggle('active');
});

// Close menu when a link is clicked
document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
        navLinks.classList.remove('active');
    });
});

// Load posts from JSON
async function loadPosts() {
    try {
        const response = await fetch('data/posts.json');
        const posts = await response.json();
        renderPosts(posts);
    } catch (error) {
        console.log('Posts data not found or empty');
        document.getElementById('noPostsMessage').style.display = 'block';
    }
}

function renderPosts(posts) {
    const postsList = document.getElementById('postsList');
    const noPostsMessage = document.getElementById('noPostsMessage');
    
    if (!posts || posts.length === 0) {
        noPostsMessage.style.display = 'block';
        return;
    }
    
    noPostsMessage.style.display = 'none';
    postsList.innerHTML = '';
    
    posts.forEach((post, index) => {
        const postCard = document.createElement('div');
        postCard.className = 'post-card' + (index % 2 === 0 ? ' alt-bg' : '');
        postCard.innerHTML = `
            <div class="post-date">${formatDate(post.date)}</div>
            <h3>${post.title}</h3>
            <p>${post.excerpt}</p>
            ${post.url ? `<a href="${post.url}" class="project-link">Read More →</a>` : ''}
        `;
        postsList.appendChild(postCard);
    });
}

// Load projects from JSON
async function loadProjects() {
    try {
        const response = await fetch('data/projects.json');
        const projects = await response.json();
        renderProjects(projects);
    } catch (error) {
        console.log('Projects data not found or empty');
        document.getElementById('noProjectsMessage').style.display = 'block';
    }
}

function renderProjects(projects) {
    const projectsList = document.getElementById('projectsList');
    const noProjectsMessage = document.getElementById('noProjectsMessage');
    
    if (!projects || projects.length === 0) {
        noProjectsMessage.style.display = 'block';
        return;
    }
    
    noProjectsMessage.style.display = 'none';
    projectsList.innerHTML = '';
    
    projects.forEach(project => {
        const projectCard = document.createElement('div');
        projectCard.className = 'project-card';
        
        const imageHTML = project.image 
            ? `<img src="${project.image}" alt="${project.title}">`
            : `<div>${project.emoji || '🚀'}</div>`;
        
        projectCard.innerHTML = `
            <div class="project-image">${imageHTML}</div>
            <div class="project-content">
                <h3>${project.title}</h3>
                <p>${project.description}</p>
                ${project.tags ? `
                    <div class="project-tags">
                        ${project.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                    </div>
                ` : ''}
                ${project.url ? `<a href="${project.url}" target="_blank" class="project-link">View Project →</a>` : ''}
            </div>
        `;
        projectsList.appendChild(projectCard);
    });
}

// Utility function to format date
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    loadPosts();
    loadProjects();
});
