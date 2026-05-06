ID: TS-3428-US1
As a LEAP Agent/User,
I want the "Application Tracker" entry points to be conditionally visible based on my role and application stage,
So that I only see tracking options that align with my permissions and policy progress.
✅ Acceptance Criteria
BASE URL: https://leapuat.adityabirlasunlifeinsurance.com/uat/#/login
Credentials:Refer from C:\Users\INVEN40415\Saved Games\App-tracker-automation_py\.env
Menu Level: Top-right dropdown displays "Application Tracker" (renamed from "Track Application") only for eligible roles: DSF, FLS, RO, CSE (Sales Mode). Hidden for SP, CSE (Ops), TPD, Banca, HDFC, Axis.
Dashboard View: Row-level "Track" CTA visible for eligible users on Assisted policies only.
Inside Journey (Right Sidebar): "Track" button visible ONLY IF Review & Acceptance (R&A) = Completed. Hidden when Review & Acceptance (R&A) is pending.
BASE_URL=https://leapuat.adityabirlasunlifeinsurance.com/uat/#/login
Inside Journey URL = https://leapuat.adityabirlasunlifeinsurance.com/uat/#/dashboard
Non-Assisted Override: For policies like HDFC Net Banking, Axis Direct, etc., the legacy label "Track Application" remains unchanged. SSO redirect logic does not trigger.
Frontend Enforcement: Eligibility is resolved before render. No interactive element exists for restricted roles. No console warnings or debug outputs leak role logic to end-users.
🔒 Out of Scope: Backend role API calls, token generation, payload schema validation, server-side RBAC checks.
