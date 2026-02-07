# Orbit Deployment Guide

## 1. MongoDB Atlas Setup (5 minutes)

1. Go to https://cloud.mongodb.com and create a free account
2. Create a new project called "orbit"
3. Build a cluster → Select **M0 Free** tier → Choose AWS us-east-1
4. Create a database user (username/password)
5. Network Access → Add IP `0.0.0.0/0` (allow from anywhere, for dev)
6. Click "Connect" → "Drivers" → Copy the connection string
7. Replace `<password>` in the string with your actual password
8. Your URI looks like: `mongodb+srv://user:pass@cluster0.xxxxx.mongodb.net/orbit?retryWrites=true&w=majority`

## 2. Railway Backend Deploy (10 minutes)

1. Go to https://railway.app and sign in with GitHub
2. New Project → Deploy from GitHub Repo (or "Empty Project" → Add Service → GitHub Repo)
3. Point it to your repo, set the root directory to `backend/`
4. Add these environment variables in Railway dashboard:

```
MONGO_URI=mongodb+srv://user:pass@cluster0.xxxxx.mongodb.net/orbit?retryWrites=true&w=majority
SECRET_KEY=<generate-a-strong-random-string>
JWT_SECRET_KEY=<generate-another-strong-random-string>
OPENAI_API_KEY=sk-your-openai-key-here
MATCH_REVEAL_DATE=2026-02-13T20:00:00
```

5. Railway auto-detects Python and deploys
6. Go to Settings → Generate Domain → Copy your URL (e.g. `orbit-api.up.railway.app`)
7. Test: `curl https://your-url.up.railway.app/health`

## 3. Update Frontend API URL

Edit `app/src/services/api.ts` and update the production URL:
```typescript
const API_BASE_URL = __DEV__
  ? 'http://localhost:5000'
  : 'https://your-url.up.railway.app';
```

## 4. iOS Build via EAS (20-30 minutes)

### Prerequisites
- Friend's Apple Developer account credentials
- Expo account (create at https://expo.dev)
- EAS CLI: `npm install -g eas-cli`

### Steps

```bash
cd app

# Login to Expo
eas login

# Configure the project (link to Expo account)
eas build:configure

# Update eas.json with Apple credentials:
# - appleId: friend's Apple ID email
# - appleTeamId: from developer.apple.com → Membership

# Build for iOS (TestFlight)
eas build --platform ios --profile production

# This will:
# 1. Ask for Apple Developer credentials
# 2. Create provisioning profiles automatically
# 3. Build the .ipa in the cloud
# 4. Give you a download link when done (~15-20 min)
```

## 5. TestFlight Upload

### Option A: Via EAS Submit (easiest)
```bash
eas submit --platform ios --latest
```

### Option B: Via Transporter App
1. Download "Transporter" from Mac App Store
2. Download the .ipa from EAS build link
3. Open Transporter → Sign in with friend's Apple ID
4. Drag the .ipa file → Click "Deliver"
5. Wait 5-10 minutes for processing

### After Upload
1. Go to https://appstoreconnect.apple.com
2. My Apps → Orbit → TestFlight tab
3. The build should appear (may need to answer export compliance = No encryption)
4. Add External Testers group → Add emails or create a public link
5. Share the TestFlight link with Rollins students!

## 6. Running the Matching Algorithm

When you're ready to generate matches (e.g., on Feb 13):

```bash
curl -X POST https://your-url.up.railway.app/matches/generate \
  -H "Content-Type: application/json" \
  -d '{"admin_secret": "your-SECRET_KEY-value"}'
```

This will pair all onboarded users and generate cosmic descriptions.

## Local Development

### Backend
```bash
cd backend
python3 run.py
# Runs on http://localhost:5000
```

### Frontend
```bash
cd app
npx expo start
# Scan QR code with Expo Go app, or press 'i' for iOS simulator
```
