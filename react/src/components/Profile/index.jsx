import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getProfile } from '../../api/profile';
import './Profile.css';

const Profile = () => {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const loadProfile = async () => {
      try {
        const token = localStorage.getItem('token');
        
        if (!token) {
          navigate('/login');
          return;
        }

        const data = await getProfile(token);
        setProfile(data);
        setLoading(false);
      } catch (err) {
        console.error('Error loading profile:', err);
        setError(err.response?.data?.error || 'Ошибка загрузки профиля');
        setLoading(false);
        
        if (err.response?.status === 401) {
          localStorage.removeItem('token');
          navigate('/login');
        }
      }
    };

    loadProfile();
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  const handleGoToChat = () => {
    navigate('/');
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('ru-RU', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getInitial = (username) => {
    return username ? username.charAt(0).toUpperCase() : '?';
  };

  if (loading) {
    return (
      <div className="profile-container" data-easytag="id1-react/src/components/Profile/index.jsx">
        <div className="profile-loading">Загрузка профиля...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="profile-container" data-easytag="id1-react/src/components/Profile/index.jsx">
        <div className="profile-error">
          <h2>Ошибка</h2>
          <p>{error}</p>
          <button className="profile-button profile-button-primary" onClick={() => navigate('/login')}>
            Войти
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="profile-container" data-easytag="id1-react/src/components/Profile/index.jsx">
      <div className="profile-card">
        <div className="profile-header">
          <div className="profile-avatar">
            {getInitial(profile?.username)}
          </div>
          <h1>Профиль пользователя</h1>
        </div>

        <div className="profile-info">
          <div className="profile-info-item">
            <div className="profile-info-label">Имя пользователя</div>
            <div className="profile-info-value">{profile?.username}</div>
          </div>

          <div className="profile-info-item">
            <div className="profile-info-label">Дата регистрации</div>
            <div className="profile-info-value">
              {profile?.created_at ? formatDate(profile.created_at) : 'Не указана'}
            </div>
          </div>

          <div className="profile-info-item">
            <div className="profile-info-label">ID пользователя</div>
            <div className="profile-info-value">#{profile?.id}</div>
          </div>
        </div>

        <div className="profile-actions">
          <button className="profile-button profile-button-primary" onClick={handleGoToChat}>
            Перейти в чат
          </button>
          <button className="profile-button profile-button-secondary" onClick={handleLogout}>
            Выйти
          </button>
        </div>
      </div>
    </div>
  );
};

export default Profile;