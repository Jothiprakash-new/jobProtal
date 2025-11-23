-- db_schema.sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  role VARCHAR(20) NOT NULL, -- 'fresher' | 'experienced' | 'employer' | 'admin'
  profile_status BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE companies (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  industry VARCHAR(100),
  size VARCHAR(50),
  verified BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE job_seekers (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  experience_level VARCHAR(50), -- 'entry' 'mid' 'senior'
  resume_url TEXT,
  skills TEXT,
  education JSONB -- e.g. [{degree, institute, year, gpa}]
);

CREATE TABLE employers (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  company_id INTEGER REFERENCES companies(id),
  position VARCHAR(255)
);

CREATE TABLE jobs (
  id SERIAL PRIMARY KEY,
  company_id INTEGER REFERENCES companies(id),
  title VARCHAR(255),
  description TEXT,
  requirements TEXT,
  location VARCHAR(255),
  location_type VARCHAR(50), -- 'remote' 'onsite' 'hybrid'
  salary_min INTEGER,
  salary_max INTEGER,
  experience_required VARCHAR(50),
  job_type VARCHAR(50), -- 'full-time' 'part-time' 'internship'
  posted_at TIMESTAMP DEFAULT NOW(),
  application_deadline DATE
);

CREATE TABLE applications (
  id SERIAL PRIMARY KEY,
  job_id INTEGER REFERENCES jobs(id),
  seeker_id INTEGER REFERENCES job_seekers(id),
  status VARCHAR(50) DEFAULT 'applied',
  applied_date TIMESTAMP DEFAULT NOW()
);

CREATE TABLE interviews (
  id SERIAL PRIMARY KEY,
  application_id INTEGER REFERENCES applications(id),
  schedule TIMESTAMP,
  feedback TEXT
);
