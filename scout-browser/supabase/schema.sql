-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Users & Preferences (Personalization Agent)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT UNIQUE NOT NULL,
    alias_domain TEXT NOT NULL DEFAULT 'myscout.id',
    approved_preferences JSONB DEFAULT '{"budgets": {}, "preferred_sources": [], "interests": []}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Shared Deletion Map (Privacy Agent - Job D)
CREATE TABLE apps_deletion_map (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    app_name TEXT UNIQUE NOT NULL,
    domain TEXT UNIQUE NOT NULL,
    category TEXT NOT NULL,
    deletion_url TEXT,
    menu_steps JSONB DEFAULT '[]'::jsonb,
    grievance_email TEXT,
    grace_period_days INT DEFAULT 30,
    success_count INT DEFAULT 0,
    failed_flagged BOOLEAN DEFAULT FALSE,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. User Accounts & Risk Ranking (Privacy Agent - Job C)
CREATE TABLE accounts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    app_id UUID REFERENCES apps_deletion_map(id),
    app_name TEXT NOT NULL,
    domain TEXT NOT NULL,
    category TEXT NOT NULL,
    browser_profile_id TEXT,
    risk_score INT DEFAULT 50,
    has_wallet_balance BOOLEAN DEFAULT FALSE,
    has_active_orders BOOLEAN DEFAULT FALSE,
    has_active_sub BOOLEAN DEFAULT FALSE,
    status TEXT DEFAULT 'active',
    deletion_proof_url TEXT,
    deletion_proof_text TEXT,
    last_used_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Alias Shield (Privacy Agent - Job A)
CREATE TABLE aliases (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    alias_email TEXT UNIQUE NOT NULL,
    assigned_app_name TEXT NOT NULL,
    assigned_domain TEXT NOT NULL,
    known_partner_domains TEXT[] DEFAULT '{}',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. Inbound Emails & Leak Detection (Privacy Agent - Job B)
CREATE TABLE inbound_emails (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    alias_id UUID REFERENCES aliases(id) ON DELETE CASCADE,
    from_email TEXT NOT NULL,
    from_domain TEXT NOT NULL,
    subject TEXT,
    snippet TEXT,
    received_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE leaks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    alias_id UUID REFERENCES aliases(id),
    leaked_from_app TEXT NOT NULL,
    leaked_from_domain TEXT NOT NULL,
    unauthorised_sender_email TEXT NOT NULL,
    unauthorised_sender_domain TEXT NOT NULL,
    sender_investigation_summary TEXT,
    complaint_draft TEXT,
    alias_disabled BOOLEAN DEFAULT TRUE,
    deletion_requested BOOLEAN DEFAULT FALSE,
    detected_at TIMESTAMPTZ DEFAULT NOW()
);

-- 6. Tasks & Human-in-the-Loop Approvals
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    prompt TEXT NOT NULL,
    intent TEXT NOT NULL,
    agents_invoked TEXT[] NOT NULL,
    status TEXT DEFAULT 'running',
    streaming_url TEXT,
    pending_action JSONB,
    result JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 7. Monitors (Monitor Agent - On Request Only)
CREATE TABLE monitors (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    target_url TEXT NOT NULL,
    condition_description TEXT NOT NULL,
    expires_at TIMESTAMPTZ NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    last_checked_at TIMESTAMPTZ,
    triggered_alert JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
