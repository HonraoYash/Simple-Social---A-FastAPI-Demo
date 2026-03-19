import streamlit as st
import requests
import base64
import urllib.parse

st.set_page_config(page_title="Simple Social", layout="wide")

API_BASE_URL = "http://localhost:8000"


def inject_styles():
    st.markdown(
        """
        <style>
            :root {
                --bg-1: #0b1020;
                --bg-2: #121a33;
                --card: rgba(255, 255, 255, 0.05);
                --card-border: rgba(255, 255, 255, 0.12);
                --text-main: #edf2ff;
                --text-muted: #a8b3cf;
                --accent: #7c8cff;
                --danger: #ff6b81;
                --success: #42d392;
            }

            .stApp {
                background:
                    radial-gradient(circle at 10% 10%, rgba(124, 140, 255, 0.18), transparent 35%),
                    radial-gradient(circle at 90% 0%, rgba(66, 211, 146, 0.15), transparent 40%),
                    linear-gradient(180deg, var(--bg-1), var(--bg-2));
            }

            .main .block-container {
                max-width: 1050px;
                padding-top: 2rem;
                padding-bottom: 2.5rem;
            }

            .hero-card,
            .glass-card,
            .post-card,
            .metric-chip {
                background: var(--card);
                border: 1px solid var(--card-border);
                border-radius: 16px;
                box-shadow: 0 16px 36px rgba(0, 0, 0, 0.25);
                backdrop-filter: blur(8px);
            }

            .hero-card {
                padding: 1.6rem 1.8rem;
                margin-bottom: 1rem;
            }

            .hero-title {
                color: var(--text-main);
                font-size: 2rem;
                font-weight: 800;
                margin-bottom: 0.35rem;
                letter-spacing: 0.3px;
            }

            .hero-subtitle,
            .muted {
                color: var(--text-muted);
                font-size: 0.95rem;
                margin-bottom: 0;
            }

            .glass-card {
                padding: 1.2rem 1.25rem;
                margin-bottom: 0.95rem;
            }

            .post-card {
                padding: 0.9rem 1rem 1rem;
                margin-bottom: 1rem;
            }

            .post-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 0.5rem;
            }

            .post-author {
                color: var(--text-main);
                font-weight: 700;
                margin-right: 0.5rem;
            }

            .post-date {
                color: var(--text-muted);
                font-size: 0.85rem;
            }

            .metric-chip {
                padding: 0.55rem 0.85rem;
                border-radius: 12px;
                text-align: center;
                color: var(--text-main);
                margin-bottom: 0.8rem;
            }

            .metric-label {
                font-size: 0.72rem;
                color: var(--text-muted);
                text-transform: uppercase;
                letter-spacing: 0.9px;
            }

            .metric-value {
                font-size: 1.15rem;
                font-weight: 700;
            }

            .stTextInput > div > div > input,
            .stTextArea textarea,
            .stFileUploader section {
                border-radius: 12px !important;
                border: 1px solid var(--card-border) !important;
                background: rgba(16, 24, 46, 0.72) !important;
                color: var(--text-main) !important;
            }

            .stButton > button {
                border-radius: 11px !important;
                border: 1px solid var(--card-border) !important;
                font-weight: 600 !important;
            }

            section[data-testid="stSidebar"] {
                background: rgba(8, 14, 30, 0.96);
                border-right: 1px solid var(--card-border);
            }

            section[data-testid="stSidebar"] * {
                color: var(--text-main);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Initialize session state
if 'token' not in st.session_state:
    st.session_state.token = None
if 'user' not in st.session_state:
    st.session_state.user = None


def get_headers():
    """Get authorization headers with token"""
    if st.session_state.token:
        return {"Authorization": f"Bearer {st.session_state.token}"}
    return {}


def login_page():
    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-title">Simple Social</div>
            <p class="hero-subtitle">A modern media feed for sharing moments with style.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.2, 1], gap="large")
    with left:
        st.markdown(
            """
            <div class="glass-card">
                <h3 style="margin-top:0;">Welcome Back</h3>
                <p class="muted">Sign in or create an account to continue.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        email = st.text_input("Email", placeholder="you@example.com")
        password = st.text_input("Password", type="password", placeholder="Enter secure password")

        if email and password:
            col1, col2 = st.columns(2, gap="small")

            with col1:
                if st.button("Login", type="primary", use_container_width=True):
                    login_data = {"username": email, "password": password}
                    response = requests.post(f"{API_BASE_URL}/auth/jwt/login", data=login_data)

                    if response.status_code == 200:
                        token_data = response.json()
                        st.session_state.token = token_data["access_token"]

                        user_response = requests.get(f"{API_BASE_URL}/users/me", headers=get_headers())
                        if user_response.status_code == 200:
                            st.session_state.user = user_response.json()
                            st.rerun()
                        else:
                            st.error("Logged in, but failed to fetch user profile.")
                    else:
                        st.error("Invalid email or password.")

            with col2:
                if st.button("Create Account", use_container_width=True):
                    signup_data = {"email": email, "password": password}
                    response = requests.post(f"{API_BASE_URL}/auth/register", json=signup_data)

                    if response.status_code == 201:
                        st.success("Account created. You can login now.")
                    else:
                        error_detail = response.json().get("detail", "Registration failed")
                        st.error(f"Registration failed: {error_detail}")
        else:
            st.info("Enter your email and password to continue.")

    with right:
        st.markdown(
            """
            <div class="glass-card">
                <h4 style="margin-top:0;">Why you'll like it</h4>
                <p class="muted">Fast uploads, clean feed cards, and secure auth with your FastAPI backend.</p>
            </div>
            <div class="glass-card">
                <h4 style="margin-top:0;">Tips</h4>
                <p class="muted">Use clear captions and upload high quality images/videos for a better feed experience.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def upload_page():
    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-title">Create a Post</div>
            <p class="hero-subtitle">Share your photo or video with the community.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Choose media",
        type=['png', 'jpg', 'jpeg', 'mp4', 'avi', 'mov', 'mkv', 'webm']
    )
    caption = st.text_area("Caption", placeholder="What story are you sharing today?")

    if uploaded_file and st.button("Share Post", type="primary", use_container_width=True):
        with st.spinner("Uploading..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            data = {"caption": caption}
            response = requests.post(f"{API_BASE_URL}/upload", files=files, data=data, headers=get_headers())

            if response.status_code == 200:
                st.success("Post published successfully.")
                st.rerun()
            else:
                st.error("Upload failed. Please try again.")
    st.markdown('</div>', unsafe_allow_html=True)


def encode_text_for_overlay(text):
    """Encode text for ImageKit overlay - base64 then URL encode"""
    if not text:
        return ""
    # Base64 encode the text
    base64_text = base64.b64encode(text.encode('utf-8')).decode('utf-8')
    # URL encode the result
    return urllib.parse.quote(base64_text)


def create_transformed_url(original_url, transformation_params, caption=None):
    if caption:
        encoded_caption = encode_text_for_overlay(caption)
        # Add text overlay at bottom with semi-transparent background
        text_overlay = f"l-text,ie-{encoded_caption},ly-N20,lx-20,fs-100,co-white,bg-000000A0,l-end"
        transformation_params = text_overlay

    if not transformation_params:
        return original_url

    parts = original_url.split("/")

    imagekit_id = parts[3]
    file_path = "/".join(parts[4:])
    base_url = "/".join(parts[:4])
    return f"{base_url}/tr:{transformation_params}/{file_path}"


def feed_page():
    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-title">Community Feed</div>
            <p class="hero-subtitle">Explore recent posts and moments from everyone.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    response = requests.get(f"{API_BASE_URL}/feed", headers=get_headers())
    if response.status_code == 200:
        posts = response.json()["posts"]

        m1, m2, m3 = st.columns(3, gap="small")
        with m1:
            st.markdown(
                f"""
                <div class="metric-chip">
                    <div class="metric-label">Total Posts</div>
                    <div class="metric-value">{len(posts)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with m2:
            media_count = sum(1 for p in posts if p.get("file_type") == "image")
            st.markdown(
                f"""
                <div class="metric-chip">
                    <div class="metric-label">Images</div>
                    <div class="metric-value">{media_count}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with m3:
            st.markdown(
                f"""
                <div class="metric-chip">
                    <div class="metric-label">Videos</div>
                    <div class="metric-value">{len(posts) - media_count}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        if not posts:
            st.info("No posts yet! Be the first to share something.")
            return

        for post in posts:
            st.markdown('<div class="post-card">', unsafe_allow_html=True)

            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(
                    f"""
                    <div class="post-header">
                        <div>
                            <span class="post-author">{post['email']}</span>
                            <span class="post-date">• {post['created_at'][:10]}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with col2:
                if post.get('is_owner', False):
                    if st.button("Delete", key=f"delete_{post['id']}", help="Delete post", use_container_width=True):
                        response = requests.delete(f"{API_BASE_URL}/posts/{post['id']}", headers=get_headers())
                        if response.status_code == 200:
                            st.success("Post deleted.")
                            st.rerun()
                        else:
                            st.error("Failed to delete post.")

            caption = post.get('caption', '')
            if post['file_type'] == 'image':
                uniform_url = create_transformed_url(post['url'], "", caption)
                st.image(uniform_url, use_container_width=True)
            else:
                uniform_video_url = create_transformed_url(post['url'], "w-400,h-200,cm-pad_resize,bg-blurred")
                st.video(uniform_video_url)
                if caption:
                    st.caption(caption)

            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("Failed to load feed.")


# Main app logic
inject_styles()

if st.session_state.user is None:
    login_page()
else:
    st.sidebar.markdown("## Simple Social")
    st.sidebar.markdown(f"Logged in as: `{st.session_state.user['email']}`")
    st.sidebar.markdown("---")

    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.user = None
        st.session_state.token = None
        st.rerun()

    page = st.sidebar.radio("Navigation", ["🏠 Feed", "📸 Upload"], label_visibility="visible")

    if page == "🏠 Feed":
        feed_page()
    else:
        upload_page()