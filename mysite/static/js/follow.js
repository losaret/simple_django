// static/js/follow.js
document.addEventListener('DOMContentLoaded', function() {
    const followBtn = document.querySelector('.follow-btn');
    
    if (followBtn) {
        followBtn.addEventListener('click', function() {
            const username = this.dataset.username;
            const action = this.dataset.action;
            const url = `/accounts/follow/${username}/`;
            
            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Type': 'application/json',
                },
                credentials: 'same-origin',
            })
            .then(response => response.json())
            .then(data => {
                if (data.is_following) {
                    // Обновляем кнопку
                    followBtn.textContent = 'Отписаться';
                    followBtn.dataset.action = 'unfollow';
                    followBtn.classList.add('following');
                } else {
                    followBtn.textContent = 'Подписаться';
                    followBtn.dataset.action = 'follow';
                    followBtn.classList.remove('following');
                }
                
                // Обновляем счетчик
                document.querySelector('.followers-count').textContent = data.followers_count;
            })
            .catch(error => console.error('Error:', error));
        });
    }
});

// Вспомогательная функция для получения CSRF-токена
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}