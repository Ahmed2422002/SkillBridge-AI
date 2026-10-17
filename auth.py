import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  FaGoogle,
  FaLinkedin,
  FaGithub,
  FaEye,
  FaEyeSlash,
} from "react-icons/fa";
import { FiUser, FiMail, FiLock } from "react-icons/fi";
import { postJSON, saveToken } from "../utils/api"; // تأكد من صحة مسار الاستيراد

// كومبوننت واحد يغطي واجهة تسجيل الطالب:
// mode="signup" -> (Create Your Account)
// mode="login"  -> (Welcome Back)
// يستخدم في الراوتر على المسارات /signup/student و /login/student

export default function AuthPage({ mode }) {
  const navigate = useNavigate();
  const isSignUp = mode === "signup";
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // يمسح الخطأ لما يتبدل بين Login و Sign Up
  useEffect(() => { setError(""); }, [mode]);

  const [showPassword, setShowPassword] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);
  const [remember, setRemember] = useState(false);
  const [form, setForm] = useState({
    fullName: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (isSignUp && form.password !== form.confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    setLoading(true);
    try {
      const data = isSignUp
        ? await postJSON("/auth/register", { // تم التعديل إلى register
            fullName: form.fullName,
            email: form.email,
            password: form.password,
          })
        : await postJSON("/auth/login", { // مسار تسجيل الدخول صحيح
            email: form.email,
            password: form.password,
          });

      if (data.access_token) saveToken(data.access_token, isSignUp ? true : remember); // ملاحظة: تأكد من اسم المتغير اللي يرجع من الباك اند (token أو access_token)
      navigate("/onboarding");
    } catch (err) {
      setError(err.message || "فشل الاتصال بالسيرفر");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page d-flex flex-column min-vh-100 bg-light">
      {/* Navbar */}
      <nav className="navbar navbar-light bg-white border-bottom px-4 py-3">
        <div className="container d-flex justify-content-end align-items-center gap-3">
          <span
            role="button"
            className="text-dark text-decoration-none fw-semibold"
            onClick={() => navigate("/login")}
          >
            Login
          </span>
          <button
            className="btn btn-dark rounded-pill px-4"
            onClick={() => navigate("/signup")}
          >
            Sign Up
          </button>
        </div>
      </nav>

      {/* Main content */}
      <div className="flex-grow-1 d-flex align-items-center justify-content-center py-5">
        <div
          className="card border-0 shadow-sm rounded-4 p-4 p-md-5"
          style={{ maxWidth: "550px", width: "100%" }}
        >
          <div className="text-center mb-4">
            <h2 className="fw-bold">
              {isSignUp ? "Create Your Account" : "Welcome Back"}
            </h2>
            <p className="text-muted">
              {isSignUp
                ? "Start your AI-powered learning journey"
                : "Continue your AI-powered learning journey"}
            </p>
          </div>

          {/* Sign Up / Login Toggle */}
          <div className="bg-light rounded-pill p-1 d-flex mb-4">
            <button
              type="button"
              className={`btn flex-fill rounded-pill ${
                isSignUp ? "bg-white shadow-sm text-dark" : "text-muted"
              }`}
              onClick={() => navigate("/signup/student")}
            >
              Sign Up
            </button>
            <button
              type="button"
              className={`btn flex-fill rounded-pill ${
                !isSignUp ? "bg-white shadow-sm text-dark" : "text-muted"
              }`}
              onClick={() => navigate("/login/student")}
            >
              Login
            </button>
          </div>

          <form onSubmit={handleSubmit}>
            {isSignUp && (
              <div className="mb-3 position-relative">
                <span className="position-absolute top-50 start-0 translate-middle-y ms-3 text-muted">
                  <FiUser />
                </span>
                <input
                  type="text"
                  name="fullName"
                  className="form-control rounded-3 ps-5 py-2"
                  placeholder="Full Name"
                  value={form.fullName}
                  onChange={handleChange}
                  required
                />
              </div>
            )}

            <div className="mb-3 position-relative">
              <span className="position-absolute top-50 start-0 translate-middle-y ms-3 text-muted">
                <FiMail />
              </span>
              <input
                type="email"
                name="email"
                className="form-control rounded-3 ps-5 py-2"
                placeholder="Email"
                value={form.email}
                onChange={handleChange}
                required
              />
            </div>

            <div className="mb-3 position-relative">
              <span className="position-absolute top-50 start-0 translate-middle-y ms-3 text-muted">
                <FiLock />
              </span>
              <input
                type={showPassword ? "text" : "password"}
                name="password"
                className="form-control rounded-3 ps-5 py-2"
                placeholder="Password"
                value={form.password}
                onChange={handleChange}
                required
              />
              <span
                role="button"
                className="position-absolute top-50 end-0 translate-middle-y me-3 text-muted"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? <FaEyeSlash /> : <FaEye />}
              </span>
            </div>

            {isSignUp && (
              <div className="mb-3 position-relative">
                <span className="position-absolute top-50 start-0 translate-middle-y ms-3 text-muted">
                  <FiLock />
                </span>
                <input
                  type={showConfirm ? "text" : "password"}
                  name="confirmPassword"
                  className="form-control rounded-3 ps-5 py-2"
                  placeholder="Confirm Password"
                  value={form.confirmPassword}
                  onChange={handleChange}
                  required
                />
                <span
                  role="button"
                  className="position-absolute top-50 end-0 translate-middle-y me-3 text-muted"
                  onClick={() => setShowConfirm(!showConfirm)}
                >
                  {showConfirm ? <FaEyeSlash /> : <FaEye />}
                </span>
              </div>
            )}

            {!isSignUp && (
              <div className="d-flex justify-content-between align-items-center mb-4">
                <div className="form-check">
                  <input
                    type="checkbox"
                    className="form-check-input"
                    id="rememberMe"
                    checked={remember}
                    onChange={(e) => setRemember(e.target.checked)}
                  />
                  <label className="form-check-label text-muted" htmlFor="rememberMe">
                    Remember me
                  </label>
                </div>
                <span
                  role="button"
                  className="fw-semibold text-decoration-none"
                  style={{ color: "#0f8f8a" }}
                >
                  Forgot Password?
                </span>
              </div>
            )}

            {error && <div className="alert alert-danger py-2">{error}</div>}

            <button
              type="submit"
              disabled={loading}
              className="btn w-100 text-white rounded-pill py-2 mb-4"
              style={{ backgroundColor: "#22D3C5" }}
            >
              {loading ? "Please wait..." : isSignUp ? "Sign Up" : "Log In"}
            </button>
          </form>

          <div className="d-flex align-items-center gap-3 mb-4">
            <hr className="flex-grow-1" />
            <span className="text-muted small">or continue with</span>
            <hr className="flex-grow-1" />
          </div>

          <div className="d-flex gap-2 mb-4">
            <button className="btn btn-outline-secondary flex-fill rounded-3 py-2">
              <FaGoogle color="#DB4437" /> Google
            </button>
            <button className="btn btn-outline-secondary flex-fill rounded-3 py-2">
              <FaLinkedin color="#0A66C2" /> LinkedIn
            </button>
            <button className="btn btn-outline-secondary flex-fill rounded-3 py-2">
              <FaGithub /> GitHub
            </button>
          </div>

          <p className="text-center small text-muted mb-0">
            By {isSignUp ? "signing up" : "logging in"}, you agree to our{" "}
            <span role="button" style={{ color: "#0f8f8a" }}>
              Terms of Service
            </span>{" "}
            and{" "}
            <span role="button" style={{ color: "#0f8f8a" }}>
              Privacy Policy
            </span>
          </p>
        </div>
      </div>
    </div>
  );
}
