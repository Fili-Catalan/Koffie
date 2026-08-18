# Software Requirements Specification
## Productivity Accountability App — v1

**Version:** 1.0
**Date:** 2026-05-19
**Author:** Fili Catalan
**Status:** Complete

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Functional Requirements](#2-functional-requirements)
3. [Non-Functional Requirements](#3-non-functional-requirements)
4. [Out of Scope](#4-out-of-scope)
5. [Acceptance Criteria](#5-acceptance-criteria)

---

## 1. Introduction

### 1.1 Purpose

This document defines the software requirements for a cross-platform productivity accountability application. It serves as the authoritative reference for all design, implementation, and testing decisions throughout the development lifecycle.

### 1.2 Product Overview

The application adds a social accountability layer to personal productivity sessions. It tracks how much time a user spends on unproductive activity during a self-defined work session — using context-aware, AI-powered classification rather than a simple domain blocklist. If a user's unproductive time exceeds a set threshold, their selected accountability friends are notified and can intervene via voice or text chat in real time.

The core differentiator from existing productivity tools is intent-based classification: the system evaluates whether a user's activity aligns with their stated session objectives, rather than flagging entire platforms as productive or unproductive. A user watching a Khan Academy video on YouTube during a math study session is classified as productive; the same user watching unrelated entertainment on YouTube is classified as unproductive.

### 1.3 Target Platforms — v1

- macOS (desktop — primary tracking platform)
- Windows (desktop — primary tracking platform)
- Linux (desktop — primary tracking platform)
- Android (mobile — social and notification layer)

### 1.4 Definitions

| Term | Definition |
|---|---|
| Session | A defined interval of time during which a user commits to working on a set of objectives |
| Threshold | The maximum amount of unproductive time permitted within a session before an accountability intervention is triggered |
| Accountability friend | A friend selected by the user to receive notifications and intervene if the threshold is breached |
| Classification | The AI-powered process of determining whether a user's current activity is productive or unproductive relative to their session objectives |
| Unclassified time | Time during which classification could not be performed due to a service outage. Does not count toward unproductive time. |
| Sessions forfeited | A lifetime stat tracking how many sessions were terminated due to three threshold violations |

---

## 2. Functional Requirements

### 2.1 Authentication

- As a user, I log into the app using a username and password authentication page.

### 2.2 Account Management

- As a user, I can reset my password.
- As a user, I can delete my account and all associated data.
- As a user, I can change my username.
- As a user, I can set an avatar image. *(deferred — see Section 4)*

### 2.3 Metrics

- As a user, I can view a metrics tab showing how much time I have spent being unproductive across days, weeks, months, and years.
- As a user, I can see the percentage of objectives I have completed, filterable by day, week, month, and year.
- As a user, I can break down my objective completion percentage by collaborator — seeing which friends I am more or less productive with — filterable by day, week, month, and year.
- As a user, I can compare my unproductive time totals by collaborator, filterable by day, week, month, and year.
- As a user, I can view objective completion and unproductive time broken down by objective category, filterable by day, week, month, and year.
- As a user, I can see my sessions forfeited lifetime stat in the metrics tab, filterable by day, week, month, and year.
- As a user, I can export my data as a CSV file containing raw session and metrics records.
- As a user, I can export my data as a PDF containing data visualizations summarizing my session history and metrics.
- As a user, I can view a personal activity log showing what was classified as productive or unproductive in each session. This log is stored on my device only and is never synced to the server.

### 2.4 Friends

- As a user, I can search for other users by username.
- As a user, I can send a friend request to another user. The recipient must accept the request before we can collaborate.
- As a user, I can accept or decline incoming friend requests.

### 2.5 Solo Session

- As a user, I can start a solo session by setting a duration, an unproductive time threshold, a list of objectives with categories, and selecting accountability friends. Once set up, I press Start to begin the session.
- When adding an objective, I press the '+' button, enter the objective text, and the app suggests a category. I can accept the suggestion or create a custom category. A category is required for every objective.
- The session ends when the timer reaches zero.
- I can end the session early by tapping the three dots menu in the upper right corner and selecting End Session.
- Sessions cannot be paused.

**Accountability — Solo:**

- If my unproductive time reaches the threshold, a notification is sent to my selected accountability friends within 2 seconds, and a voice chat and text chat become immediately available for them to use.
- Friends can speak to me via voice chat or send text messages. There is no accept or decline prompt — the chat is available to them immediately.
- Text messages from friends appear as large, semi-transparent overlay text on my screen. The overlay disappears only when I enter the chat room.
- Once the chat concludes, I press Resume Session to continue. The threshold is permanently reduced by half for the remainder of the session.
- If I breach the threshold a second time, the same intervention sequence is triggered and the threshold is halved again upon resuming.
- If I breach the threshold a third time, the session ends immediately. The following is logged: completed objectives remain as-is; unproductive time is recorded as the full session duration; a session terminated flag is added to the record; the sessions forfeited lifetime stat is incremented; all accountability friends receive a final notification that the session ended due to repeated threshold violations.
- If my accountability friends are offline when I breach the threshold, they receive a push notification and are taken directly to the chat when they tap it. The same threshold penalties apply regardless of friend availability. I am not notified that my friends are offline.
- If a friend taps a threshold breach notification after my session has already ended, they are taken to the app home screen and shown a dialog informing them the session has ended.

**End of Session Logging:**

- When the session ends by any means (timer, manual end, or third threshold breach), the following is logged: objectives completed count, objectives uncompleted count, completion ratio, and total unproductive time.

### 2.6 Group Session

- As a user, I can start a group session by selecting friends to invite. Invitees can accept or decline.
- While waiting for members to join, a pre-session voice chat is active in the lobby for deliberation.
- The session creator sets a shared duration and unproductive time threshold that applies to all members.
- Each member individually sets their own objectives for the session.
- Members press a Ready button to indicate they are ready to start. If a member changes their objectives after pressing Ready, their Ready status resets and they must press it again.
- Once all members are Ready, the Start button becomes available to the session creator.
- If the session creator leaves or disconnects before pressing Start, the Start button transfers to the member who joined the lobby earliest after the creator. That member is notified via a dialog.
- Sessions cannot be paused.

**Poke Feature:**

- During a session, a member can Poke another member to initiate a voice chat for collaboration. The poke appears as a notification in the upper right corner of the recipient's screen.
- The recipient can accept or decline the poke. If they decline, an optional text box appears for them to explain why.
- A member can poke multiple friends simultaneously.
- The poke voice chat includes camera sharing, screen sharing, and a whiteboard tool.

**Accountability — Group:**

- When a member breaches the shared threshold, a notification appears in the upper right corner of every other member's screen. The notification identifies who breached the threshold and lists any members already speaking or texting with them.
- Members can choose to Respond or Ignore the notification.
- If no member responds within 2 minutes, two available members are selected at random and connected to the shared accountability chat. Availability means the member is not currently in a poke call or other collaboration within the session.
- If every member is unavailable when the 2-minute timeout expires, a large semi-transparent overlay alert appears on all members' screens. If no one responds after this alert, the appropriate penalties are applied and all members continue their session.
- There is one shared chat and voice channel per accountability intervention. Any responding member joins this same channel.
- Text messages during an intervention appear as large semi-transparent overlay text, identical to solo session behavior. The overlay disappears when the user enters the chat room.
- A third threshold breach ends that member's individual session with the same stat consequences as a solo session. The group session continues for all remaining members.

**Leaving and Ending:**

- A member can leave the session by tapping the three dots menu and selecting Leave Session. The session continues for remaining members.
- The creator leaving an active session does not end the session.
- The session ends when the last remaining member leaves or when the timer reaches zero.
- There is no mechanism for one member to end the session for everyone. Each member must leave individually.
- End of session logging is identical to solo sessions and is recorded individually for each member. Collaborator-specific metrics are updated for all members.

**Visibility:**

- Throughout the session, all members can see each other's real-time unproductive time totals and objectives completed counts.

### 2.7 Unproductivity Measurement

- The app tracks what sites and applications the user is actively using during a session.
- The system evaluates whether the user's activity aligns with their stated session objectives using AI-powered classification. Activity that aligns with one or more objectives is classified as productive. Activity that does not align with any objective is classified as unproductive.
- The system is context-aware. A user watching educational content on YouTube during a math study session is classified as productive. The same user switching to unrelated entertainment on YouTube is classified as unproductive.
- For reading or article content, the foreground window is tracked. For video, both foreground and background video that is actively playing is tracked.
- **Known complexity:** Distinguishing productive from unproductive use of the same platform based on content intent is technically complex and is expected to require significant implementation time.

### 2.8 Admin Dashboard

The admin dashboard is a web interface served by the Flask backend, separate from the Flutter application. Access is restricted to admin accounts only.

**User Management:**

- As an admin, I can view a searchable, filterable list of all registered users.
- As an admin, I can view an individual user's account details and session history.
- As an admin, I can suspend a user's account, preventing them from logging in while preserving their data. Suspensions are reversible.
- As an admin, I can permanently ban a user's account.
- As an admin, I can delete a user's account and all associated data permanently.
- As an admin, I can force a password reset on any user's account.

**System Health:**

- As an admin, I can view a real-time dashboard showing: current system uptime status, error rate over the last 24 hours and 7 days broken down by error type, number of active sessions, LLM classification API status, classification request queue length and average wait time, and database health status.

**Usage Analytics:**

- As an admin, I can view the following metrics over selectable time ranges: total registered users and growth over time, daily/weekly/monthly active users, sessions created broken down by solo vs. group, platform distribution (macOS, Windows, Linux, Android), average session duration, threshold breach rates, and sessions forfeited count.

---

## 3. Non-Functional Requirements

### 3.1 Performance

**NFR-PERF-001**
**Statement:** When the user switches to a new active window or application, the system must begin classifying that activity within 1 second of the switch.
**Rationale:** Ensures the classification pipeline stays current with the user's actual behavior so that unproductive time is not missed between switches.

**NFR-PERF-002**
**Statement:** Each individual activity classification must complete within 10 seconds of being submitted to the classification service.
**Rationale:** Bounds the maximum lag between a user engaging in an activity and that activity being reflected in their unproductive time total.

**NFR-PERF-003**
**Statement:** The system must track the foreground window/application continuously. For video content, the system must track both foreground and background video that is actively playing.
**Rationale:** Users may consume video passively in a background tab while working in the foreground. Both contexts contribute to productive or unproductive time.

**NFR-PERF-004**
**Statement:** After each activity is classified, the session's running unproductive time total must be updated within 500ms.
**Rationale:** Keeps the threshold check current so breach detection is not delayed by slow aggregation.

**NFR-PERF-005**
**Statement:** Upon detecting a threshold breach, the system must deliver a push notification to all selected accountability friends within 2 seconds.
**Rationale:** Accountability depends on friends being notified promptly — a delayed alert reduces the effectiveness of the intervention.

**NFR-PERF-006**
**Statement:** Voice communication channels must maintain a one-way audio delay of under 150ms.
**Rationale:** One-way delays exceeding 150ms are perceptible to users and degrade conversation quality. 150ms is the industry standard threshold for acceptable voice call latency.

**NFR-PERF-007**
**Statement:** The metrics tab must fully load and render all data within 3 seconds on a standard broadband connection.
**Rationale:** Pages that take longer than 3 seconds to load measurably increase user abandonment.

**Known Future Consideration:** Continuous per-activity classification (NFR-PERF-001/002) is used for the prototype. In a production deployment with significant user load, this approach should be revisited in favor of a batched or hybrid classification model to manage LLM API costs.

---

### 3.2 Security

**NFR-SEC-001**
**Statement:** All communication between the client and the backend must use HTTPS/TLS. Unencrypted HTTP traffic must be rejected.
**Rationale:** Protects all data in transit from interception.

**NFR-SEC-002**
**Statement:** User passwords must be hashed using bcrypt before storage. Raw passwords must never be stored or logged anywhere in the system.
**Rationale:** Ensures that a database breach does not expose user passwords.

**NFR-SEC-003**
**Statement:** JWT access tokens must expire after no longer than 1 hour. The client must silently refresh the access token using the refresh token before expiry.
**Rationale:** Limits the window of exposure if an access token is compromised.

**NFR-SEC-004**
**Statement:** Refresh tokens must expire after 7 days of inactivity. After expiry the user must re-authenticate.
**Rationale:** Balances security with usability given that conversations and activity data on the app may contain sensitive personal information.

**NFR-SEC-005**
**Statement:** Login attempts must be rate-limited. After 5 consecutive failed attempts, the account must be temporarily locked for 15 minutes.
**Rationale:** Prevents brute force attacks against user accounts.

**NFR-SEC-006**
**Statement:** Every API endpoint must validate the user's JWT before returning any data. A user must never be able to access another user's data by manipulating a request.
**Rationale:** Enforces authorization at every boundary — authentication alone is not sufficient.

**NFR-SEC-007**
**Statement:** The server must only store activity classification results and timestamps. Raw activity detail — window titles, URLs, video titles — must never be transmitted to or stored on the server.
**Rationale:** Minimizes the sensitivity of a potential server breach and respects user privacy by keeping detailed behavioral data off the server.

**NFR-SEC-008**
**Statement:** The personal activity log — the record of what was classified as productive or unproductive during a session — must be stored on the user's device only and never synced to the server.
**Rationale:** Gives users confidence that the detailed record of their computer activity is under their sole control.

**NFR-SEC-009**
**Statement:** During a session, members may only see each other's unproductive time totals. Underlying activity detail is never visible to other session members.
**Rationale:** Preserves individual privacy within collaborative sessions.

**NFR-SEC-010 — Future Consideration**
**Statement:** End-to-end encryption for messages is not implemented in v1. All messages are encrypted in transit via TLS and encrypted at rest on the server. E2E encryption must be implemented before the app is released to the general public.
**Rationale:** Messages between users may contain sensitive personal conversations. E2E is the appropriate long-term solution but requires significant additional engineering investment.

---

### 3.3 Privacy

**NFR-PRIV-001**
**Statement:** The system must only collect data that is directly necessary for the app's functionality. No additional behavioral, demographic, or usage telemetry may be collected without explicit user consent.
**Rationale:** Data minimization is a core principle of GDPR and good privacy practice.

**NFR-PRIV-002**
**Statement:** Server-side user data — session records, metrics, objectives, and classification results — must be retained until the user explicitly deletes their account. No automatic expiry is applied.
**Rationale:** Historical metrics are core to the app's value. Retention until deletion is appropriate given the non-sensitive nature of the stored data relative to what is kept off-server.

**NFR-PRIV-003**
**Statement:** When a user deletes their account, all associated data must be permanently purged from the server within 30 days. This includes session records, metrics, objectives, friendship associations, and any messages stored server-side. The deletion must be total — no orphaned records may remain.
**Rationale:** GDPR and CCPA both require the right to erasure. Partial deletion that leaves orphaned records is non-compliant.

**NFR-PRIV-004**
**Statement:** Before sending activity descriptions to the third-party classification API, the system must strip all identifying information — including full URLs, usernames, account-specific query parameters, and any personally identifiable strings. Only the content descriptor (e.g., application name and content title) may be transmitted.
**Rationale:** Activity descriptions are sent to a third-party LLM API for classification. Stripping identifying data limits personal information exposure to that third party.

**NFR-PRIV-005**
**Statement:** On first launch, the user must be presented with a consent screen that clearly discloses: what data is collected, that activity descriptions are sent to a third-party API for classification, and that a full privacy policy is available. The user must affirmatively accept before using the app.
**Rationale:** Informed consent is required under GDPR. Users have a right to know their activity descriptions leave the device before agreeing to use the app.

**NFR-PRIV-006**
**Statement:** Users must be able to export all server-side data associated with their account. Export formats must include CSV tables for raw session and metrics data, and PDF reports with data visualizations for human-readable summaries.
**Rationale:** GDPR grants users the right to data portability.

**NFR-PRIV-007**
**Statement:** The app must be designed for compliance with GDPR and CCPA. This includes: a published privacy policy, the right to data deletion (NFR-PRIV-003), the right to data export (NFR-PRIV-006), disclosure of third-party data processors, and a database structure that supports complete per-user data deletion.
**Rationale:** The app targets wide public adoption. GDPR applies to any user in the EU; CCPA applies to California residents. Designing for compliance from the start is significantly less costly than retrofitting it later.

---

### 3.4 Reliability

**NFR-REL-001**
**Statement:** The backend must maintain 99.5% uptime, permitting no more than approximately 43 hours of unplanned downtime per year.
**Rationale:** Sets a concrete availability target appropriate for a growing product in early adoption.

**NFR-REL-002**
**Statement:** If the backend becomes unreachable during an active session, the session must continue uninterrupted on the device. The timer, activity tracking, and classification pipeline must all operate locally. Session data must be queued on-device and synced to the server automatically when connectivity is restored.
**V1 scope note:** Full offline-first session continuity is the target architecture. If this proves out of scope for v1, the fallback behavior is: the session ends immediately, all data logged up to the point of disconnection is saved locally and synced when connectivity is restored, and the user is notified of the disconnection.
**Rationale:** A network interruption should not invalidate a user's work session.

**NFR-REL-003**
**Statement:** When the LLM classification service is unavailable, the system must skip classification for affected activities and log that time as unclassified. Unclassified time must not count toward the user's unproductive time total. Once the service is restored, classification of new activities resumes normally.
**Rationale:** Users must not be penalized for system failures outside their control.

**NFR-REL-004**
**Statement:** All failed requests to external services — the LLM API, push notification service, and voice service — must be automatically retried up to 3 times with exponential backoff before surfacing an error to the user or triggering a fallback behavior.
**Rationale:** Transient network failures are common. Retrying with backoff resolves the majority of them without user-facing impact.

**NFR-REL-005**
**Statement:** If the voice or text chat service fails during an active accountability intervention, the app must display an error message to all participants and attempt to reconnect automatically. If reconnection fails after 3 attempts, the intervention is considered concluded and the session resumes normally without penalty to the user.
**Rationale:** A voice service failure during an intervention should not leave the session in a broken state or penalize the user for a system error.

**NFR-REL-006**
**Statement:** Session data — objectives, classification results, timestamps, and unproductive time totals — must be persisted to local device storage continuously throughout the session, not only at session end. In the event of an app crash, the session record up to the last persisted state must be recoverable.
**Rationale:** Prevents total data loss from an app crash.

**NFR-REL-007**
**Statement:** The backend must perform automated database backups at minimum once every 24 hours. Backups must be stored in a separate location from the primary database. The system must be restorable from a backup within 4 hours of a failure event.
**Rationale:** Protects against data loss from database corruption or infrastructure failure.

**NFR-REL-008**
**Statement:** All server-side errors must be logged with sufficient detail — timestamp, endpoint, error type, and stack trace — to allow diagnosis and resolution. Logs must be retained for a minimum of 90 days.
**Rationale:** Without structured error logging, production failures cannot be reliably diagnosed or tracked over time.

**Architectural note:** NFR-REL-002 (offline-first session continuity) requires the device to have a local database capable of persisting and running a full session independently. This is a foundational design decision that must be addressed early in system design.

---

### 3.5 Scalability

**NFR-SCALE-001**
**Statement:** The system must support a minimum of 1,000 concurrent users at v1 launch without degradation in response times. The architecture must be designed to scale to 10,000 concurrent users without requiring structural redesign.
**Rationale:** Sets a concrete target for infrastructure planning at launch and establishes that scalability is a design constraint, not an afterthought.

**NFR-SCALE-002**
**Statement:** The backend must be stateless. No session or user-specific state may be stored in server memory between requests. All persistent state must live in the database or a dedicated state store. This enables horizontal scaling by allowing multiple identical server instances to run behind a load balancer.
**Rationale:** Stateless backends can be scaled horizontally by adding server instances without routing or state-sharing complexity.

**NFR-SCALE-003**
**Statement:** All database queries for metrics, session history, and user lookups must use appropriate indexes. Query performance must not degrade materially as the dataset grows from 1,000 to 10,000 users and their accumulated session history.
**Rationale:** Unindexed queries that perform acceptably at small scale frequently become bottlenecks at production scale.

**NFR-SCALE-004**
**Statement:** All LLM classification requests must be routed through a managed request queue. The queue must process requests at a controlled rate that stays within the LLM provider's rate limits. During traffic spikes, requests must wait in the queue rather than be dropped or rejected.
**Rationale:** Unqueued classification requests from concurrent users will exceed LLM API rate limits during spikes, causing classification failures.

**NFR-SCALE-005**
**Statement:** During peak queue load, individual classification requests may take longer than the 10-second target defined in NFR-PERF-002. This is an accepted tradeoff. Queue wait time plus classification time must not exceed 30 seconds under normal operating conditions.
**Rationale:** Documents the known performance tradeoff introduced by the request queue so it is an explicit design decision rather than an undiscovered failure mode.

**NFR-SCALE-006**
**Statement:** Real-time group session state — live unproductive time updates and objective completions — is delivered via WebSocket connections. The system must be designed to handle the stateful nature of WebSocket connections at the target scale of 1,000 concurrent users, with a documented plan for scaling to 10,000.
**Rationale:** WebSocket connections are stateful and do not scale the same way as stateless REST endpoints. This must be treated as a distinct scaling challenge in system design.

**NFR-SCALE-007**
**Statement:** The backend must implement per-user API rate limiting. Individual users must not be able to generate request volumes that degrade system performance for other users.
**Rationale:** Protects shared infrastructure from abuse or misbehaving clients.

---

### 3.6 Compatibility

**NFR-COMPAT-001**
**Statement:** The desktop application must support macOS 13 (Ventura) and all subsequent versions.
**Rationale:** macOS 13 covers the vast majority of active Mac users and provides the modern Accessibility APIs required for activity tracking.

**NFR-COMPAT-002**
**Statement:** The desktop application must support Windows 10 (build 1903 and above) and Windows 11.
**Rationale:** Windows 10 retains a large installed base despite reaching end of life in October 2025. Supporting both versions maximizes reach. Note: Windows 10 no longer receives Microsoft security updates — this is a conscious tradeoff accepted to capture the broader Windows user base.

**NFR-COMPAT-003**
**Statement:** The mobile application must support Android 10 (API level 29) and all subsequent versions.
**Rationale:** Android 10 covers approximately 95% of active Android devices and introduced the modern permission model required for notification and usage tracking features.

**NFR-COMPAT-004 — Future**
**Statement:** iOS support is deferred to a future version. When implemented, the minimum supported version must be iOS 16.
**Rationale:** iOS imposes significant restrictions on third-party activity tracking that make the core tracking feature largely unimplementable.

**NFR-COMPAT-005**
**Statement:** The application must conform to WCAG 2.1 Level AA across all supported platforms. This includes but is not limited to: a minimum color contrast ratio of 4.5:1 for normal text, full keyboard navigability, visible focus indicators, descriptive labels on all interactive elements, and compatibility with platform screen readers (VoiceOver on macOS, TalkBack on Android).
**Rationale:** WCAG 2.1 AA is the industry standard for digital accessibility and the threshold for compliance with the ADA and the European Accessibility Act.

**NFR-COMPAT-006**
**Statement:** The application must render correctly across a range of screen sizes and resolutions, including standard and high-DPI (Retina on macOS, high-DPI on Windows) displays. Layouts must be responsive and must not break or clip content when text is scaled up to 200%.
**Rationale:** Users work across a variety of monitor sizes and display densities. The 200% text scaling requirement is also a WCAG 2.1 AA criterion.

**NFR-COMPAT-007 — Future**
**Statement:** A browser extension for Chrome and Firefox is deferred to v2. In v1, web-based activity tracking relies on OS-level active window title reading. The extension will provide more granular URL and page title access when implemented.
**Rationale:** A browser extension is a separate codebase from the Flutter application. Deferring it keeps v1 scope manageable.

**NFR-COMPAT-008**
**Statement:** The desktop application must support the following Linux distributions: Ubuntu 20.04 LTS and above, Fedora 36 and above, and any distribution running GTK 3.16+ with AT-SPI2 accessibility support.
**Rationale:** Flutter's Linux target requires GTK 3.16+. AT-SPI2 is the Linux accessibility bus required for active window title reading. Ubuntu and Fedora represent the largest share of desktop Linux users.

---

## 4. Out of Scope

The following features are explicitly not included in v1. Their absence is a deliberate scope decision, not an oversight.

| # | Feature | Deferred To |
|---|---|---|
| 1 | iOS support | Future version |
| 2 | User-facing web app | v2 |
| 3 | Browser extension (Chrome/Firefox) | v2 |
| 4 | End-to-end encryption for messages | Before wide public release |
| 5 | Avatar images | Future version |
| 6 | Biometric authentication | Future version |
| 7 | Third-party integrations (Google Calendar, Notion, Todoist, etc.) | Future version |
| 8 | AI-generated session recommendations | Future version |
| 9 | Monetization features | Future version |

---

## 5. Acceptance Criteria

### 5.1 Authentication & Account Management

**AC-AUTH-001: Successful login**
Given a user has a registered account
When they enter the correct username and password and submit
Then they are authenticated, issued a JWT access token and refresh token, and taken to the app home screen

**AC-AUTH-002: Failed login — wrong credentials**
Given a user has a registered account
When they enter an incorrect username or password
Then they are shown an error message stating the credentials are invalid and they remain on the login screen

**AC-AUTH-003: Account lockout after repeated failures**
Given a user has entered incorrect credentials 5 consecutive times
When they attempt to log in again within the lockout window
Then the account is temporarily locked for 15 minutes and they are shown a message informing them of the lockout

**AC-AUTH-004: Access token expiry and silent refresh**
Given a user is logged in and their access token has expired
When they perform any action that requires authentication
Then the app silently uses the refresh token to obtain a new access token without interrupting the user

**AC-AUTH-005: Refresh token expiry**
Given a user's refresh token has expired after 7 days of inactivity
When they open the app or attempt any authenticated action
Then they are redirected to the login screen and must re-authenticate

**AC-ACCT-001: Password reset**
Given a user has forgotten their password
When they request a password reset and follow the reset flow
Then they are able to set a new password and log in successfully with the new password. The old password must no longer work after the reset is complete.

**AC-ACCT-002: Username change**
Given a logged-in user navigates to account settings
When they enter a new username and confirm
Then their username is updated across the app immediately. If the requested username is already taken, they are shown an error and the change is not applied.

**AC-ACCT-003: Account deletion**
Given a logged-in user requests account deletion
When they confirm the deletion
Then their account, all session records, metrics, objectives, friendship associations, and messages are permanently deleted from the server within 30 days. They are logged out immediately and cannot log back in.

**AC-ACCT-004: First launch consent screen**
Given a user is launching the app for the first time
When the app opens
Then they are presented with a consent screen disclosing what data is collected and that activity descriptions are sent to a third-party API for classification. They must affirmatively accept before accessing the app.

---

### 5.2 Metrics

**AC-METRICS-001: Metrics tab load time**
Given a logged-in user navigates to the metrics tab
When the tab is opened
Then all data is fully loaded and rendered within 3 seconds on a standard broadband connection

**AC-METRICS-002: Objectives completed percentage**
Given a logged-in user is on the metrics tab
When they view their objectives completion rate
Then they can see the percentage of objectives completed, filterable by day, week, month, and year

**AC-METRICS-003: Objectives completion breakdown by collaborator**
Given a logged-in user has completed sessions with other users
When they view the objectives completion breakdown by collaborator
Then they can see the percentage of objectives completed for each friend they have worked with, filterable by day, week, month, and year

**AC-METRICS-004: Unproductive time comparison by collaborator**
Given a logged-in user has completed sessions with other users
When they view the unproductive time breakdown by collaborator
Then they can see the total unproductive time logged when working with each friend, filterable by day, week, month, and year

**AC-METRICS-005: Objectives and unproductive time breakdown by category**
Given a logged-in user has completed sessions with categorized objectives
When they view the category breakdown
Then they can see the percentage of objectives completed and total unproductive time for each objective category, filterable by day, week, month, and year

**AC-METRICS-006: Sessions forfeited stat**
Given a logged-in user has had one or more sessions terminated due to three threshold violations
When they view the metrics tab
Then they can see their total sessions forfeited count, filterable by day, week, month, and year

**AC-METRICS-007: No data state**
Given a logged-in user has not yet completed any sessions
When they navigate to the metrics tab
Then they are shown an empty state message indicating no data is available yet rather than empty charts or errors

**AC-METRICS-008: CSV data export**
Given a logged-in user requests a data export
When they select the CSV export option
Then a CSV file is generated and downloaded containing all their session records and metrics data in a structured, machine-readable format

**AC-METRICS-009: PDF data export**
Given a logged-in user requests a data export
When they select the PDF export option
Then a PDF is generated and downloaded containing data visualizations summarizing their session history and metrics in a human-readable format

**AC-METRICS-010: Personal activity log**
Given a user has completed a session on their device
When they view their personal activity log
Then they can see a per-session breakdown of activities classified as productive and unproductive during that session. This data is stored on the device only and is not accessible from any other device or from the server.

---

### 5.3 Friends

**AC-FRIENDS-001: Search for users**
Given a logged-in user navigates to the search screen
When they enter a username into the search field
Then a list of matching users is displayed. If no users match the search term, an empty state message is shown indicating no results were found.

**AC-FRIENDS-002: Send a friend request**
Given a logged-in user has found another user via search
When they send a friend request to that user
Then the request is delivered to the recipient and the sender sees a pending status on that user's profile. The two users are not yet able to collaborate until the request is accepted.

**AC-FRIENDS-003: Accept a friend request**
Given a logged-in user has received a friend request
When they accept the request
Then both users are connected as friends and can collaborate on sessions, select each other as accountability partners, and appear in each other's collaborator metrics.

**AC-FRIENDS-004: Decline a friend request**
Given a logged-in user has received a friend request
When they decline the request
Then the request is removed and no friendship is created. The user who sent the request is not notified that it was declined.

**AC-FRIENDS-005: Duplicate friend request**
Given a logged-in user has already sent a friend request to another user that is still pending
When they view that user's profile
Then the send request option is not available and the pending status is shown instead. They cannot send a duplicate request.

**AC-FRIENDS-006: Request to existing friend**
Given a logged-in user is already friends with another user
When they view that user's profile
Then no friend request option is shown. The profile reflects the existing friendship status.

**AC-FRIENDS-007: Incoming request from someone you already requested**
Given user A has sent a friend request to user B
When user B sends a friend request to user A before accepting
Then the system automatically treats this as a mutual acceptance and both users become friends immediately.

---

### 5.4 Solo Session

**AC-SOLO-001: Session setup — valid inputs**
Given a logged-in user navigates to start a solo session
When they enter a valid session duration, unproductive time threshold, at least one objective, and select at least one accountability friend, then press Start
Then the session begins, the timer starts counting down, and activity tracking begins immediately

**AC-SOLO-002: Session setup — missing required fields**
Given a logged-in user is setting up a solo session
When they attempt to press Start without entering a duration, threshold, or at least one objective
Then the session does not start and they are shown an error indicating which required fields are missing

**AC-SOLO-003: Objective entry and category suggestion**
Given a user is adding an objective during session setup
When they press the '+' button, enter the objective text, and submit
Then the app suggests a category for that objective in a pop-up. If the user presses Accept, the suggested category is applied. If they press Create Category and enter a custom name, the custom category is applied instead.

**AC-SOLO-004: Objective entry — category required**
Given a user is adding an objective during session setup
When they attempt to confirm the objective without accepting or creating a category
Then the objective is not added and they are prompted to select or create a category before proceeding

**AC-SOLO-005: Session timer**
Given an active solo session
When the timer is running
Then it counts down accurately from the set duration and is visible to the user at all times during the session

**AC-SOLO-006: No pause functionality**
Given an active solo session
When a user attempts to pause the session
Then no pause option is available. The session continues running uninterrupted.

**AC-SOLO-007: Objective completion**
Given an active solo session
When a user checks off an objective
Then the objective is marked as completed and the completion is recorded with a timestamp

**AC-SOLO-008: First threshold breach — notification sent**
Given an active solo session where the user's unproductive time has reached the set threshold
When the threshold is breached
Then a notification is sent to all selected accountability friends within 2 seconds and a voice chat and text chat become immediately available for friends to use

**AC-SOLO-009: First threshold breach — accountability friend texts**
Given a threshold breach has occurred and an accountability friend sends a text message
When the message is sent
Then the message appears as large, semi-transparent overlay text on the user's screen. The overlay persists until the user enters the chat room.

**AC-SOLO-010: First threshold breach — accountability friend calls**
Given a threshold breach has occurred and an accountability friend joins the voice chat
When the friend begins the voice call
Then the voice chat becomes active immediately with no accept or decline prompt required from the user

**AC-SOLO-011: Overlay dismissal**
Given large transparent text is overlaying the user's screen
When the user enters the chat room
Then the overlay text disappears and the user is in the chat interface

**AC-SOLO-012: Resume session after first breach**
Given the user has concluded the accountability chat
When they press Resume Session
Then the session resumes, the unproductive time threshold is permanently reduced by half for the remainder of the session, and the timer continues from where it left off

**AC-SOLO-013: Second threshold breach**
Given the user has already breached the threshold once and resumed the session
When their unproductive time reaches the halved threshold
Then the same accountability intervention sequence is triggered. Upon resuming, the threshold is reduced by half again.

**AC-SOLO-014: Third threshold breach — session terminated**
Given the user has already breached the threshold twice
When their unproductive time reaches the threshold a third time
Then the session is immediately terminated and the following is logged: completed objectives remain as-is, unproductive time is recorded as the full session duration, a session terminated flag is added to the session record, and the sessions forfeited lifetime stat is incremented. All selected accountability friends receive a final notification that the session ended due to repeated threshold violations.

**AC-SOLO-015: Threshold breach with offline friends**
Given a threshold breach has occurred and all selected accountability friends are offline
When the breach is detected
Then notifications are sent to the offline friends. The same threshold penalties apply to the user regardless of friend availability. The user is not notified that their friends are offline.

**AC-SOLO-016: Friend opens expired notification after session ends**
Given a session has ended and an offline friend later taps the threshold breach notification
When they tap the notification
Then they are taken to the app home screen and shown a dialog informing them that the session has already ended

**AC-SOLO-017: Natural session end**
Given an active solo session
When the timer reaches zero
Then the session ends automatically and the following is logged: objectives completed count, objectives uncompleted count, completion ratio, and total unproductive time

**AC-SOLO-018: Manual session end**
Given an active solo session
When the user taps the three dots menu and selects End Session
Then the session ends immediately and the same logging as a natural session end is applied up to the point of termination

**AC-SOLO-019: Session log accuracy**
Given a session has ended by any means
When the session record is saved
Then the logged data accurately reflects the actual objectives completed, time elapsed, and unproductive time accumulated up to the point the session ended

---

### 5.5 Group Session

**AC-GROUP-001: Creating a group session and sending invites**
Given a logged-in user initiates a group session
When they select friends to invite and send the invites
Then each selected friend receives an in-app notification with the option to join or decline. The session lobby opens immediately for the creator while waiting for responses.

**AC-GROUP-002: Joining a group session**
Given a user has received a group session invite
When they accept the invite
Then they are taken to the session lobby and joined to the pre-session voice chat. Their joined status is visible to all other lobby members.

**AC-GROUP-003: Declining a group session invite**
Given a user has received a group session invite
When they decline
Then they are not added to the session and the session creator is not notified of the decline.

**AC-GROUP-004: Pre-session voice chat**
Given at least one member has joined the lobby
When they are waiting for the session to start
Then a voice chat is active and available for all lobby members to use for deliberation

**AC-GROUP-005: Setting session duration and threshold**
Given members are in the lobby
When the group agrees on a duration and unproductive time threshold
Then these values are entered by the session creator and applied uniformly to all members for the session

**AC-GROUP-006: Individual objective entry**
Given a member is in the lobby
When they add objectives using the same '+' button flow as solo sessions
Then their objectives are saved individually and are not shared with or visible to other members during setup. Category suggestion and creation works identically to solo sessions.

**AC-GROUP-007: Ready button**
Given a member has finished entering their objectives
When they press the Ready button
Then their status is updated to Ready and is visible to all lobby members including the session creator

**AC-GROUP-008: Ready button resets on objective change**
Given a member has already pressed Ready
When they make any change to their objectives
Then their Ready status is reset and they must press Ready again before the Start button becomes available

**AC-GROUP-009: Start button availability**
Given all members in the lobby have pressed Ready
When the last member's status updates to Ready
Then the Start button becomes available to the session creator only

**AC-GROUP-010: Creator leaves lobby before Start**
Given the session creator leaves the lobby or disconnects before pressing Start
When this occurs
Then the Start button is transferred to the member who joined the lobby earliest after the creator. That member receives a dialog notifying them that the creator has left and they are now responsible for starting the session.

**AC-GROUP-011: Session start**
Given all members are Ready and the creator presses Start
When the session begins
Then the timer starts for all members simultaneously, activity tracking begins for each member individually, and the pre-session voice chat ends

**AC-GROUP-012: Visibility of member data**
Given an active group session
When a member views the session screen
Then they can see the unproductive time total and objectives completed count for every member in the session in real time

**AC-GROUP-013: No pause functionality**
Given an active group session
When a member attempts to pause the session
Then no pause option is available. The session continues running for all members uninterrupted.

**AC-GROUP-014: Sending a poke**
Given an active group session
When a member pokes another member
Then the recipient receives a notification pop-up in the upper right corner of their screen with the option to join or decline

**AC-GROUP-015: Accepting a poke**
Given a member has received a poke notification
When they accept
Then a voice chat opens between the two members with camera, screen share, and whiteboard tools available

**AC-GROUP-016: Declining a poke**
Given a member has received a poke notification
When they decline
Then the poke is dismissed. An optional text box appears for them to provide a reason for declining. The sender is notified of the decline.

**AC-GROUP-017: Poking multiple members**
Given an active group session
When a member sends pokes to multiple friends simultaneously
Then each recipient receives their own poke notification independently and can accept or decline individually

**AC-GROUP-018: Threshold breach notification to all members**
Given a member's unproductive time reaches the shared session threshold
When the breach is detected
Then a notification appears in the upper right corner of every other member's screen. The notification identifies who breached the threshold and lists any members already speaking or texting with them.

**AC-GROUP-019: Respond or ignore**
Given a threshold breach notification has appeared
When a member chooses to respond
Then they are connected to the shared accountability chat or voice channel for that member. When a member chooses to ignore, the notification is dismissed for them only.

**AC-GROUP-020: Two-minute response timeout**
Given a threshold breach notification has been sent to all members
When no member has chosen to respond within 2 minutes
Then two available members are selected at random and connected to the shared accountability chat with the member who breached the threshold. Availability means the member is not currently in a poke call or other collaboration within the session.

**AC-GROUP-021: All members unavailable**
Given a threshold breach has occurred and every member is in an existing call or collaboration
When the 2-minute timeout expires with no available members to assign
Then a large semi-transparent overlay alert appears on all members' screens informing them that someone has breached the threshold and has not been spoken to. If no member responds after this alert, the appropriate threshold penalties are applied to the member who breached and all members continue their session.

**AC-GROUP-022: Shared accountability chat**
Given one or more members are responding to a threshold breach
When they engage with the breaching member
Then there is one shared chat and voice channel for that intervention. Any member who chooses to respond joins this same channel.

**AC-GROUP-023: Text overlay in group accountability**
Given a member in an active group session receives a text message during an accountability intervention
When the message is sent
Then it appears as large semi-transparent overlay text on their screen, identical to the solo session behavior. The overlay disappears only when the user enters the chat room.

**AC-GROUP-024: Third breach in group session**
Given a member has already breached the threshold twice in a group session
When they breach the threshold a third time
Then that member's individual session ends immediately with the same stat consequences as a solo session third breach. The group session continues unaffected for all remaining members.

**AC-GROUP-025: Leaving a session**
Given an active group session
When a member taps the three dots menu and selects Leave Session
Then they are removed from the session. The session continues for all remaining members.

**AC-GROUP-026: Creator leaving an active session**
Given the session creator leaves an active group session
When this occurs
Then the session continues for all remaining members without interruption.

**AC-GROUP-027: Session end — last member leaves**
Given an active group session where all but one member have left
When the last remaining member leaves the session
Then the session ends and logging is triggered for all members

**AC-GROUP-028: Session end — timer reaches zero**
Given an active group session
When the timer reaches zero
Then the session ends simultaneously for all members and logging is triggered

**AC-GROUP-029: No forced end mechanism**
Given an active group session that needs to end early
When members want to end the session
Then each member must individually press Leave Session. There is no mechanism for one member to end the session for everyone else.

**AC-GROUP-030: End of session logging**
Given a group session has ended by any means
When the session record is saved
Then each member's data is logged individually: objectives completed, objectives uncompleted, completion ratio, and total unproductive time. This data feeds into each member's individual metrics and their collaborator-specific metrics.

---

### 5.6 Unproductivity Measurement

**AC-TRACK-001: Tracking begins and ends with session**
Given a session has started
When activity tracking initializes
Then the system immediately begins monitoring the user's active window and application. When the session ends by any means, tracking stops immediately.

**AC-TRACK-002: Foreground activity tracking**
Given an active session
When the user switches to a different application or window
Then the system detects the switch within 1 second and submits the new activity for classification

**AC-TRACK-003: Background video tracking**
Given an active session
When a video is actively playing in a background window or tab
Then that video is tracked alongside the foreground activity and submitted for classification independently

**AC-TRACK-004: Identifying information stripped before classification**
Given an activity is being submitted for classification
When the system prepares the classification request
Then all identifying information — full URLs, usernames, account-specific query parameters, and personally identifiable strings — is stripped before the request is sent to the LLM API. Only the application name and content descriptor are transmitted.

**AC-TRACK-005: Classification against session objectives**
Given an activity has been submitted for classification
When the LLM evaluates it
Then it is assessed against the user's specific session objectives. Activity that aligns with one or more objectives is classified as productive. Activity that does not align with any objective is classified as unproductive.

**AC-TRACK-006: Context-aware classification**
Given a user has a financial literacy objective and is watching a relevant educational video on YouTube
When the activity is classified
Then it is classified as productive because the content aligns with the stated objective, regardless of the platform being used

**AC-TRACK-007: Context shift detection**
Given a user has a financial literacy objective and switches from watching relevant educational content to watching unrelated entertainment content on the same platform
When the new activity is classified
Then it is classified as unproductive because the content no longer aligns with the session objectives

**AC-TRACK-008: Classification completes within time limit**
Given an activity has been submitted for classification
When the classification request is processed
Then the result is returned within 10 seconds under normal operating conditions. During peak queue load the result must be returned within 30 seconds.

**AC-TRACK-009: Unproductive time total update**
Given an activity has been classified as unproductive
When the classification result is received
Then the session's running unproductive time total is updated within 500ms to reflect the additional unproductive time accumulated

**AC-TRACK-010: Productive activity does not increment unproductive total**
Given an activity has been classified as productive
When the classification result is received
Then the unproductive time total remains unchanged

**AC-TRACK-011: LLM service unavailable — unclassified time**
Given the LLM classification service is unavailable during an active session
When activities occur that cannot be classified
Then the time during the outage is logged as unclassified. Unclassified time does not count toward the user's unproductive time total. Classification resumes normally once the service is restored.

**AC-TRACK-012: Threshold monitoring**
Given an active session with a running unproductive time total
When the total reaches the set threshold
Then the threshold breach is detected immediately and the accountability notification sequence is triggered within 2 seconds

---

### 5.7 Admin Dashboard

**AC-ADMIN-001: Admin-only access**
Given a user attempts to access the admin dashboard
When their credentials are verified
Then access is granted only if their account has admin privileges. Any attempt to access the dashboard with a standard user account is rejected with an unauthorized error.

**AC-ADMIN-002: View all registered users**
Given an admin is on the user management screen
When the screen loads
Then a list of all registered users is displayed with search and filter functionality. The list must load within 3 seconds.

**AC-ADMIN-003: View individual user details**
Given an admin is viewing the user list
When they select an individual user
Then they can view that user's account details and session history

**AC-ADMIN-004: Suspend an account**
Given an admin selects a user and chooses to suspend their account
When they confirm the suspension
Then the user is immediately prevented from logging in. Their data is preserved. The suspension is reversible — the admin can unsuspend the account and restore login access at any time.

**AC-ADMIN-005: Ban an account**
Given an admin selects a user and chooses to ban their account
When they confirm the ban
Then the user is immediately and permanently prevented from logging in. The ban cannot be reversed through normal admin actions.

**AC-ADMIN-006: Delete an account**
Given an admin selects a user and chooses to delete their account
When they confirm the deletion — which must require a secondary confirmation given the irreversibility of the action
Then the account and all associated data is permanently deleted from the server within 30 days, identical to the user-initiated deletion process. This action cannot be undone.

**AC-ADMIN-007: Force password reset**
Given an admin selects a user and forces a password reset
When the action is confirmed
Then the user's current password is invalidated immediately. On their next login attempt they are required to set a new password before accessing the app.

**AC-ADMIN-008: Admin cannot delete their own account via the dashboard**
Given an admin is viewing their own account in the user management screen
When they attempt to delete it
Then the action is blocked and an error message is shown indicating that an admin account cannot be self-deleted through the dashboard.

**AC-ADMIN-009: Uptime status**
Given an admin navigates to the system health screen
When the screen loads
Then the current system uptime status is displayed and updates in real time

**AC-ADMIN-010: Error rate display**
Given an admin views the system health screen
When error rate data is displayed
Then they can see the error rate for the last 24 hours and last 7 days, broken down by error type — server-side errors, client errors, and failed external API calls

**AC-ADMIN-011: Active session count**
Given an admin views the system health screen
When the screen loads
Then the current number of active sessions is displayed and updates in real time

**AC-ADMIN-012: LLM API status**
Given an admin views the system health screen
When the screen loads
Then the current status of the LLM classification API is displayed as one of: operational, degraded, or down

**AC-ADMIN-013: Classification queue status**
Given an admin views the system health screen
When the screen loads
Then the current classification request queue length and average wait time are displayed and update in real time

**AC-ADMIN-014: Database health**
Given an admin views the system health screen
When the screen loads
Then the current database health status is displayed

**AC-ADMIN-015: User growth**
Given an admin navigates to the usage analytics screen
When they view user growth data
Then they can see total registered users and growth over time, filterable by day, week, and month

**AC-ADMIN-016: Active users**
Given an admin views usage analytics
When they view active user data
Then they can see daily, weekly, and monthly active user counts over selectable time ranges

**AC-ADMIN-017: Session analytics**
Given an admin views usage analytics
When they view session data
Then they can see the total number of sessions created broken down by solo vs. group, filterable by day, week, and month

**AC-ADMIN-018: Platform breakdown**
Given an admin views usage analytics
When they view platform data
Then they can see the distribution of active users across macOS, Windows, Linux, and Android

**AC-ADMIN-019: Session performance metrics**
Given an admin views usage analytics
When they view session performance data
Then they can see average session duration, threshold breach rates, and total sessions forfeited count over selectable time ranges
