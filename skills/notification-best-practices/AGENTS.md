# Notification best practices

This skill provides comprehensive guidelines and best practices for designing, writing, and implementing effective notification systems across all channels.

## How to use this skill

When working with this skill, follow these guidelines:

1. Review the relevant rule files for your specific use case
2. Follow the guidelines and best practices outlined in each rule
3. Reference the examples and templates provided
4. Ensure compliance with any requirements mentioned

---




# Channel-specific notification guidelines

## Quick reference table

| Channel | Max Length | Structure | Tone | Images | Links |
|---------|-----------|-----------|------|--------|-------|
| **Email** | Subject: ~60 chars<br>Body: No limit | Subject + Preheader + Greeting + Core message + CTA + Signature | Professional, informative, personalized | Yes (optimize for mobile) | Yes (multiple) |
| **SMS** | 160 chars (GSM7)<br>70 chars (with emoji) | Clear CTA up front + context | Concise, direct, action-oriented | No | Yes (one short link) |
| **In-app** | ~60-80 chars per message | Short headline + body + CTA button | Helpful, contextual, minimal | Yes (small icons) | Yes (CTA buttons) |
| **Push** | iOS: ~178 chars total<br>Android: ~305 chars total | Short hook + 1-line CTA | Urgent, clear, concise | No (small icons only) | Yes (1 link max) |
| **Chat apps** | No limit, keep concise | Contextual header + brief message + optional button | Conversational, friendly, informative | Yes (thumbnails) | Yes (buttons or inline) |

## Email notifications

### Subject lines
**Guidelines:**
- Maximum ~60 characters before truncation
- Front-load the most important information
- Include specific details (names, numbers, items)
- Avoid spam triggers (excessive caps, multiple exclamation points)

**Examples:**
```
📄 Invoice #4521 paid by Acme Corp
👥 3 new candidates applied for Senior Engineer role
💾 Your export of Q4 customer data is ready
```

### Preview text
**Guidelines:**
- Maximum ~90 characters on desktop, ~35 on mobile
- Complement the subject line, don't repeat it
- Include actionable information or next steps
- Write complete thoughts that make sense even if truncated

**Examples:**
```
👀 Review their feedback and approve changes directly from this email
⏳ You have 24 hours left to claim your early bird discount. Register now
💬 Sarah Chen and 2 others are waiting for your input on the roadmap
```

### Email body content
**Guidelines:**
- **Greeting**: Use recipient's name when available
- **Primary message**: State the notification reason in the first sentence
- **Context**: Provide relevant details (but keep it scannable)
- **Call-to-action**: Make buttons/links obvious and descriptive
- **Footer**: Include unsubscribe and preference options

**Example:**
```
Hi {{user.name}},

{{actor.name}} requested access to the {{resource.name}} dashboard.

**Request details:**
- Access level requested: Editor
- Reason: "Need to update Q4 metrics"
- Expires: 7 days from approval

[Approve Request] [Deny Request]

You can manage all pending requests in your [team settings].
```

## Push notifications

### Character limits
**iOS**: 4 lines total (~50 chars for title, ~175 for body)
**Android**: 7 lines total (~65 chars for title, ~240 for body)

**Note**: These limits vary by device model, screen size, and user settings. Use conservative limits to ensure messages display properly across all devices.

### Guidelines
- Lead with the user benefit or required action
- Include specific details (names, amounts, items)
- Ensure the message makes sense without opening the app
- Adhere to character limits by device type

### Examples
```
👍 Expense report approved
Sarah approved your expense report for $234.50

📈 Your weekly report is ready
There was a 15% increase in conversions

🚨 Inventory alert
The Blue Widget stock is below your reorder point (12 units)
```

## SMS notifications

### Character limits
**160 characters** for GSM7 encoding
**70 characters** if any character requires UCS-2 encoding (like emojis)

**Critical**: When an SMS contains even a single character not supported by GSM7, the entire message switches to UCS-2 encoding, reducing the character limit from 160 to 70.

### Guidelines
- Identify your service (if not obvious from sender)
- State the key information
- Include action if needed
- Always provide opt-out instructions for marketing messages
- Adhere to character limits

### Examples
```
🔐 Knock: Your password reset code is 445-892. Valid for 10 minutes.

💰 Payment of $125.00 received from ABC Corp for Invoice #4412. View details: [link]

🎗️ Appointment reminder: Dr. Smith tomorrow (Jan 5) at 2:30 PM. Reply C to confirm.
```

## In-app notifications

### Notification feed
A persistent collection of notifications accessible through a dedicated interface element (bell icon or sidebar).

**Guidelines:**
- Include timestamp (relative when recent: "2 hours ago")
- Support scanning with consistent structure
- Group related notifications when possible
- Mark read/unread states clearly

**Structure:**
```
[Avatar] **Actor** action object
Supplementary details
[Timestamp] [Secondary action]
```

**Examples:**
```
💬 Sarah Chen commented on your design proposal
"Love the new navigation approach!"
2 hours ago • View comment

✅ Team Alpha completed sprint planning
15 story points across 8 tasks
Yesterday at 3:47 PM • View sprint

🆕 3 new applicants for Senior Engineer role
Marcus Liu and 2 others applied
Oct 23 • Review applications
```

### Toast notifications
Brief, temporary messages that appear on screen and disappear automatically.

**Guidelines:**
- ~60-80 chars per message (varies by UI)
- Single, clear message
- Avoid multiple actions
- Auto-dismiss after 5-7 seconds for non-critical messages

**Examples:**
```
👉 "Settings saved successfully"
👉 "Jason Lee started reviewing your pull request"
👉 "Export complete: 2,847 records processed"
```

## Chat app notifications

Used in Slack or Microsoft Teams, blending the richness of email with the immediacy of push.

### Guidelines
- Use `*bold*` for emphasis
- Include `@mentions` when appropriate
- Leverage emojis for visual scanning 🎯
- Use code blocks for technical information
- For Slack, create sections with Block Kit for complex messages

### Examples
```
🚨 **Production alert**
CPU usage exceeded 90% on server `api-prod-02`
Current: 94% | Duration: 5 minutes

🎉 **New customer signup!**

**Company**: Acme Corporation
**Plan**: Enterprise ($499/month)
**Users**: 50 seats

The sales team has been notified. View full details in the customer dashboard.
```

---



# Notification copy best practices

## Core principles

### Be specific and actionable
Users scan notifications in seconds. Lead with essential information and make the required action clear.

**Bad example:**
```
You have a new update in your account
[View update]
```

**Good example:**
```
Sarah Chen commented on your design proposal
[Click here to reply]
[Click here to view project]
```

### Include maximum context
Notifications pull users away from other tasks. Make the interruption worthwhile by providing enough context to help them decide whether to act immediately.

**Bad example:**
```
Your deployment's status changed
```

**Good example:**
```
Deployment #142 status changed from 'pending' to 'failed'
```

### Use active voice
Active voice creates more engaging notifications by putting the actor first and reducing word count. It feels more personal and makes notifications easier to scan and act upon.

**Bad example:**
```
Your report has been viewed by 12 people
```

**Good example:**
```
12 people viewed your report
```

### Use consistent terminology
Match the language in your notifications to your product's UI. If your app calls them "projects," don't suddenly switch to "workspaces" in notifications.

### Format for each channel
Every channel displays notifications differently, from character limits to link formatting. Understand how your messages will appear across each channel before sending.

## Writing guidelines by notification type

### Transactional notifications
Confirm user actions or system events where messaging clarity and accuracy matter most.

**Guidelines:**
- Confirm exactly what happened
- Include relevant identifiers (order numbers, amounts)
- Provide next steps when applicable
- Maintain neutral, professional tone

**Examples:**
```
📦 Your order #4521 has shipped via FedEx. Track package: [link]

✅ Password successfully updated. You'll need to sign in again on other devices.

💾 Export complete: customer_data_2024_q4.csv (45.2 MB) ready for download
```

### System notifications
Communicate technical events or service status where technical accuracy meets user-friendly language.

**Guidelines:**
- Translate technical events into user impact
- Provide clear timelines when possible
- Offer actionable next steps
- Link to detailed information

**Examples:**
```
⏰ Scheduled maintenance tonight 2-4 AM EST. API responses may be slower than normal.

⏳ Your API key expires in 7 days. Generate a new key to prevent service interruption.

🪫 Storage usage at 85% (42.5 GB of 50 GB). Upgrade for uninterrupted service.
```

### Lifecycle messaging
Encourage users to return to your product by balancing value with frequency to avoid notification fatigue.

**Guidelines:**
- Provide clear value proposition
- Use social proof when relevant
- Create urgency appropriately (not artificially)
- Respect user preferences

**Examples:**
```
💬 3 teammates commented on your design.
[See what they're saying]

📋 Your weekly summary: 487 new visitors, 12% increase from last week

✅ Lisa Chen completed the task you assigned: 'Update API documentation'
```

### Promotional messaging
Communicate offers, updates, and new features to drive engagement and adoption.

**Guidelines:**
- Lead with the benefit, not the feature
- Make offers specific and time-bound
- Include clear CTAs that match the message
- Segment based on user behavior and preferences

**Examples:**
```
🤑 Save 30% on annual plans — 3 days left to upgrade

🆕 New: AI-powered insights now analyze your team's productivity patterns

🪫 You've used 80% of your API calls.
[Upgrade to Pro for unlimited access]
```

## Testing checklist

Before shipping any notification:

1. **Read aloud**: Does it sound natural?
2. **Remove context**: Does it make sense without prior knowledge?
3. **Check truncation**: Does the key message survive character limits?
4. **Test personalization**: Do variables render correctly with real data?
5. **Verify links**: Do all CTAs lead to the right place?

## Implementation guidelines

When implementing notifications:
- Define clear categories (transactional, engagement, system)
- Create templates for common notification types
- Set up user preference controls
- Test across all target channels
- Monitor engagement metrics
- Implement batching for high-frequency events
- Plan for internationalization
- Document copy guidelines for your team

---



# Notification system implementation rules

## Core implementation principles

### 1. User-centric design
**Rule**: Always prioritize user value over technical implementation details.

**Application**:
- Lead with benefits, not features
- Respect user preferences and quiet hours
- Implement batching to prevent notification fatigue
- Provide granular control over notification types

### 2. Context is king
**Rule**: Every notification must provide enough context for users to take immediate action.

**Application**:
- Include relevant identifiers (order numbers, user names, amounts)
- Show what changed (from "pending" to "failed")
- Provide action history when relevant
- Link directly to the related object/page

### 3. Multi-channel consistency
**Rule**: Maintain consistent messaging across all channels while respecting channel-specific constraints.

**Application**:
- Use the same terminology across email, push, SMS, and in-app
- Adapt length and format to channel requirements
- Ensure brand voice remains consistent
- Test notifications across all channels before launch

### 4. Progressive disclosure
**Rule**: Start with the minimum information needed, provide paths to learn more.

**Application**:
- Use notification feeds for detailed history
- Use toasts for immediate confirmations
- Use email for comprehensive information
- Use push for urgent, actionable items

## Channel selection rules

### When to use email
**Use email when**:
- Information requires persistent reference
- Content includes detailed instructions or data
- Users need to forward or share information
- Message isn't time-critical
- Rich formatting enhances understanding

**Don't use email when**:
- Action must be immediate
- Information becomes stale quickly
- User is actively in the product
- Message is purely transactional (consider SMS)

### When to use push notifications
**Use push when**:
- Time-sensitivity is critical
- User needs to return to the app
- Action required impacts ongoing work
- External events affect user's data

**Don't use push when**:
- Information is low-priority
- User is already active in app
- Message requires extended reading
- Notification is part of a high-frequency stream

### When to use SMS
**Use SMS when**:
- Delivery must be guaranteed
- User may not have app access
- Authentication or security is involved
- Time-criticality is extreme

**Don't use SMS when**:
- Message contains sensitive data
- Rich formatting is needed
- Cost of delivery outweighs value
- Email or push would suffice

### When to use in-app
**Use in-app when**:
- User is actively using the product
- Action can wait until next session
- Building notification history is valuable
- Guiding user through a flow

**Don't use in-app when**:
- User needs notification while away
- Information expires before next session
- Immediate attention required
- User isn't likely to check feed regularly

### When to use chat (Slack/Teams)
**Use chat when**:
- Team collaboration is core to the action
- Immediate team visibility is valuable
- Discussion may follow the notification
- Integration with team workflows matters

**Don't use chat when**:
- Information is personal/private
- Team coordination isn't required
- User isn't active on the platform
- Notification would create channel noise

## Timing and frequency rules

### Timing rules

**Immediate send (< 1 second)**:
- Authentication codes
- Security alerts
- Transaction confirmations
- Error notifications

**Short delay (1-5 minutes)**:
- Batch related activities
- Aggregate similar events
- Wait for user to complete flow

**Scheduled send**:
- Digest emails (daily/weekly)
- Reminder notifications
- Scheduled reports
- Timezone-optimized sends

**Conditional delay**:
- Quiet hours respect
- Don't send if user active in app
- Wait for higher-priority notification to send first
- Delay until user completes related action

### Frequency rules

**Per-event notifications**:
- Security alerts
- Payment/transaction confirmations
- Critical system events
- User-initiated actions

**Batched notifications**:
- Social interactions (likes, comments)
- Multiple updates to same object
- Activity summaries
- Non-urgent system events

**Digest format**:
- Daily/weekly summaries
- Low-priority updates
- Historical data
- Cross-product updates

**Frequency caps**:
- Maximum per day by category
- Maximum per week for promotional content
- Escalating delays (1min, 5min, 15min, 1hr, 24hr)
- User-configurable limits

## Preference management rules

### Required preferences

**Global controls**:
- Master on/off switch per channel
- Quiet hours configuration
- Frequency preferences
- Language/locale settings

**Category controls**:
- Transactional (limited opt-out)
- System/security (required)
- Product updates (full control)
- Marketing (full control)
- Social/engagement (full control)

**Channel controls**:
- Enable/disable per channel per category
- Fallback channel preference
- Delivery timing preferences
- Format preferences (digest vs. real-time)

### Preference hierarchy
```
Global OFF → No notifications
↓
Category OFF → No notifications in that category
↓
Channel OFF → No notifications on that channel
↓
Quiet Hours → Delay until appropriate time
↓
Frequency Caps → Batch or delay additional notifications
↓
Send notification
```

## Error handling rules

### Retry strategy
**Hard failures (don't retry)**:
- Invalid email/phone number
- Unsubscribed user
- Blocked/bounced address
- Permission denied

**Soft failures (retry with backoff)**:
- Rate limit hit
- Temporary provider outage
- Network timeout
- Queue overflow

**Retry pattern**:
```
Attempt 1: Immediate
Attempt 2: 1 minute later
Attempt 3: 5 minutes later
Attempt 4: 15 minutes later
Attempt 5: 1 hour later
Give up after 5 attempts
```

### Fallback strategies

**Channel fallback**:
```
Primary: Push notification
If fails: Send email
If that fails: Log error, don't spam user
```

**Content fallback**:
```
Try: Full rich content
If fails: Plain text version
If fails: Minimal essential info
```

**Provider fallback**:
```
Primary: Provider A
If unavailable: Provider B
If unavailable: Queue for later retry
```

## Testing requirements

### Before launch checklist

**Technical tests**:
- [ ] Test across all target channels
- [ ] Verify variable substitution
- [ ] Check link functionality
- [ ] Test with missing data/variables
- [ ] Verify preference respect
- [ ] Check timing/scheduling
- [ ] Test batching logic
- [ ] Verify fallback behavior

**Content tests**:
- [ ] Proofread all copy
- [ ] Verify tone and voice
- [ ] Check for typos/grammar
- [ ] Test localization (if applicable)
- [ ] Verify brand consistency
- [ ] Check CTA clarity
- [ ] Test with real data

**User experience tests**:
- [ ] Verify mobile rendering
- [ ] Check desktop display
- [ ] Test notification center integration
- [ ] Verify read/unread states
- [ ] Check action button functionality
- [ ] Test deep linking
- [ ] Verify opt-out functionality

**Integration tests**:
- [ ] Test with actual providers
- [ ] Verify analytics tracking
- [ ] Check error monitoring
- [ ] Test rate limiting
- [ ] Verify queue processing
- [ ] Check database updates
- [ ] Test concurrent notifications

## Monitoring and alerts

### Key metrics to monitor

**Delivery metrics**:
- Delivery rate by channel
- Time to delivery (p50, p95, p99)
- Failure rate by error type
- Queue depth and lag
- Provider response times

**Engagement metrics**:
- Open rate by notification type
- Click-through rate by CTA
- Time to first interaction
- Completion rate for actions
- Unsubscribe rate by category

**System health**:
- API response times
- Queue processing rate
- Database query performance
- Provider uptime
- Error rate by type

**User satisfaction**:
- Preference change frequency
- Opt-out reasons
- Support ticket volume
- User feedback scores
- Re-engagement after opt-out

### Alert thresholds

**Critical (page immediately)**:
- Delivery rate drops below 95%
- Queue depth exceeds 10,000 messages
- Provider completely unavailable
- Authentication failures spiking
- Critical notification fails

**Warning (alert during business hours)**:
- Delivery rate drops below 98%
- Engagement rate drops 20%+
- Unsubscribe rate increases 50%+
- Queue processing lag > 5 minutes
- Error rate exceeds 5%

**Info (daily digest)**:
- Delivery trends
- Engagement patterns
- Volume changes
- New failure types
- Performance improvements

## Security and privacy rules

### Data handling

**Never include in notifications**:
- Full credit card numbers
- Social security numbers
- Passwords or tokens
- Unencrypted sensitive data
- Personally identifiable information (beyond name/email)

**Always include**:
- Unsubscribe link (for marketing)
- Preference management link
- Privacy policy link
- Data handling disclosure
- Support contact

### Compliance requirements

**CAN-SPAM (email)**:
- Include physical address
- Honor opt-out within 10 days
- Clear identification of sender
- Honest subject lines
- Mark promotional content

**TCPA (SMS)**:
- Obtain explicit consent
- Provide opt-out instructions
- Honor opt-out immediately
- Keep records of consent
- Don't use auto-dialer for marketing

**GDPR (EU users)**:
- Obtain explicit consent
- Provide data access
- Enable data deletion
- Maintain consent records
- Allow consent withdrawal

**CCPA (California)**:
- Disclose data collection
- Enable data deletion
- Allow opt-out of sale
- Provide data access
- Maintain privacy policy

## Documentation requirements

### Required documentation

**System design**:
- Architecture diagram
- Channel flow charts
- Preference logic
- Retry strategies
- Fallback patterns

**Notification catalog**:
- Complete notification list
- Trigger conditions
- Target audience
- Channel used
- Frequency expectations

**Templates**:
- Template registry
- Variable definitions
- Localization keys
- Sample outputs
- Version history

**Runbooks**:
- Common failure modes
- Debugging procedures
- Provider escalation
- Manual interventions
- Recovery procedures

**Style guide**:
- Copy guidelines
- Channel specifications
- Brand requirements
- Tone and voice
- Common patterns

---



# Notification template examples

## Starter templates for common use cases

### New user signup (email)

```liquid
Subject: {{actor.name}} joined your {{workspace.name}} workspace

Hi {{user.name}},

{{actor.name}} ({{actor.email}}) just joined your workspace as {{actor.role}}.

{{#if pending_approval}}
This user is pending approval. You can:
[Approve Access] [Deny Access]
{{else}}
They now have access to:
- {{list_of_permissions}}
{{/if}}

Manage team permissions anytime in [workspace settings].
```

**When to use**: Team collaboration products, workspace management

**Key elements**:
- Clear identification of who joined
- Role and permissions context
- Conditional approval flow
- Link to management tools

---

### Payment received (SMS)

```
Payment confirmed: ${{amount}} from {{customer.name}} for Invoice #{{invoice.number}}. Balance: ${{remaining_balance}}
```

**When to use**: Payment processing, invoicing systems

**Key elements**:
- Transaction confirmation
- Specific amounts
- Reference numbers
- Remaining balance context

---

### Collaboration activity (in-app)

```liquid
{{actor.name}} {{action}} {{object.type}} "{{object.name}}"
{{#if comment}}"{{comment}}"{{/if}}
{{timestamp}}
```

**When to use**: Any collaborative product (docs, design, project management)

**Key elements**:
- Actor-action-object structure
- Optional comment/message
- Timestamp for context
- Scannable format

---

### System alert (push)

```
{{alert.severity}} alert: {{alert.title}}
{{alert.description}}
[View details] [Acknowledge]
```

**When to use**: DevOps tools, monitoring systems, critical alerts

**Key elements**:
- Severity level
- Clear title and description
- Multiple action options
- Urgency indicators

---

### Password reset (email)

```liquid
Subject: Reset your password

Hi {{user.name}},

We received a request to reset your password for {{app.name}}.

[Reset Password]

This link expires in {{expiry.hours}} hours.

If you didn't request this, you can safely ignore this email. Your password won't change until you create a new one via the link above.

For security, this link can only be used once.
```

**When to use**: Authentication flows, security events

**Key elements**:
- Clear purpose statement
- Prominent CTA
- Expiration information
- Security reassurance
- Single-use clarification

---

### Order confirmation (email)

```liquid
Subject: Order #{{order.number}} confirmed

Hi {{customer.name}},

Thanks for your order! We're preparing it for shipment.

**Order summary**
Order #{{order.number}}
Date: {{order.date}}

{% for item in order.items %}
- {{item.name}} ({{item.quantity}}) - {{item.price | currency}}
{% endfor %}

**Subtotal**: {{order.subtotal | currency}}
**Shipping**: {{order.shipping | currency}}
**Total**: {{order.total | currency}}

**Shipping to:**
{{shipping.address}}

Track your order: [link]
View full details: [link]

Questions? Reply to this email or visit our help center.
```

**When to use**: E-commerce, marketplaces, order processing

**Key elements**:
- Order reference number
- Itemized list
- Pricing breakdown
- Shipping details
- Action links
- Support information

---

### Weekly digest (email)

```liquid
Subject: Your weekly summary: {{stats.highlight}}

Hi {{user.name}},

Here's what happened in {{app.name}} this week.

**Activity**
- {{stats.actions}} actions completed
- {{stats.collaborators}} team members active
- {{stats.items}} new items created

**Top performing**
{{#each top_items}}
- {{this.name}}: {{this.metric}}
{{/each}}

**This week's insights**
{{#if insights}}
{{insights.message}}
{{/if}}

[View Full Dashboard]

---
Prefer daily summaries? [Update preferences]
```

**When to use**: Activity summaries, productivity tools, analytics platforms

**Key elements**:
- Timeframe clarity
- Key metrics upfront
- Personalized insights
- Dashboard access
- Preference management

---

### Mention notification (chat)

```
**{{actor.name}}** mentioned you in **{{context.location}}**

> {{message.preview}}

[View conversation] [Reply]
```

**When to use**: Collaboration tools, team chat, social features

**Key elements**:
- Who mentioned you
- Where it happened
- Message preview
- Quick action buttons

---

### Scheduled maintenance (multiple channels)

**Email version:**
```liquid
Subject: Scheduled maintenance: {{date}} at {{time}}

Hi {{user.name}},

We'll be performing scheduled maintenance on {{date}} from {{time_start}} to {{time_end}} {{timezone}}.

**What to expect:**
- {{app.name}} will be unavailable during this window
- All data is safe and will be preserved
- No action required on your part

**Why we're doing this:**
{{maintenance.reason}}

Questions? Our team is here to help: [contact support]

We appreciate your patience as we improve {{app.name}}.
```

**SMS Version:**
```
{{app.name}} maintenance {{date}} {{time_start}}-{{time_end}} {{timezone}}. Service will be unavailable. No action needed. Details: [link]
```

**When to use**: System maintenance, planned downtime

**Key elements**:
- Clear timeframe with timezone
- Expected impact
- Reassurance
- Contact information

---

### Trial ending (email)

```liquid
Subject: Your trial ends in {{days_remaining}} days

Hi {{user.name}},

Your {{app.name}} trial ends on {{trial_end_date}}.

**What you've accomplished:**
- {{stats.metric1}}: {{stats.value1}}
- {{stats.metric2}}: {{stats.value2}}
- {{stats.metric3}}: {{stats.value3}}

Continue your progress by upgrading to {{plan.name}}.

**{{plan.name}} includes:**
- {{feature.1}}
- {{feature.2}}
- {{feature.3}}

[Upgrade Now] [Compare Plans]

Questions about upgrading? [Schedule a call with our team]

Don't want to upgrade? Your account will automatically convert to our free plan on {{trial_end_date}}.
```

**When to use**: SaaS trials, freemium conversions

**Key elements**:
- Days remaining
- Value demonstration
- Plan benefits
- Multiple CTAs
- Fallback option

---

### Comment/reply (in-app)

```liquid
{{actor.name}} replied to your comment

"{{comment.text}}"

In: {{context.item_name}}
{{timestamp}}

[Reply] [View thread]
```

**When to use**: Discussion threads, document comments, feedback systems

**Key elements**:
- Clear action (replied)
- Comment preview
- Context/location
- Quick actions

---

### Feature announcement (email)

```liquid
Subject: New: {{feature.name}}

Hi {{user.name}},

We built something you asked for: {{feature.name}}.

**What it does:**
{{feature.description}}

**Why you'll love it:**
{{#each benefits}}
- {{this.benefit}}
{{/each}}

**How to use it:**
{{feature.instructions}}

[Try it now]

**Example:**
{{feature.example}}

We'd love to hear what you think. Reply to this email with feedback.
```

**When to use**: Product updates, feature launches

**Key elements**:
- Feature name and description
- Clear benefits
- Usage instructions
- Examples
- Feedback loop

---

### Failed payment (email + SMS)

**Email version:**
```liquid
Subject: Payment failed for {{subscription.name}}

Hi {{user.name}},

We couldn't process your payment for {{subscription.name}}.

**What happened:**
{{error.message}}

**What you need to do:**
Update your payment method to continue your subscription.

[Update Payment Method]

If you don't update your payment method by {{deadline}}, your account will be downgraded to the free plan.

**Need help?** Our team is here: [contact support]
```

**SMS Version:**
```
{{app.name}}: Payment failed for {{subscription.name}}. Update payment method to avoid service interruption: [link]
```

**When to use**: Subscription billing, payment processing

**Key elements**:
- Clear problem statement
- Specific error
- Action required
- Deadline
- Consequences
- Support access

## Template variables best practices

### Common variable patterns

**User context:**
```liquid
{{user.name}}
{{user.email}}
{{user.role}}
{{user.timezone}}
{{user.preferences.*}}
```

**Actor context:**
```liquid
{{actor.name}}
{{actor.avatar_url}}
{{actor.email}}
```

**Object context:**
```liquid
{{object.type}}
{{object.name}}
{{object.id}}
{{object.url}}
```

**Timestamp formatting:**
```liquid
{{timestamp}}  // "2 hours ago"
{{timestamp | date: "full"}}  // "January 23, 2026 at 2:30 PM"
{{timestamp | date: "short"}}  // "Jan 23"
```

**Conditional logic:**
```liquid
{{#if condition}}
  Show this content
{{else}}
  Show alternative
{{/if}}

{{#each items}}
  {{this.property}}
{{/each}}
```

## Fallback strategies

### Handle missing data
```liquid
{{user.name | default: "there"}}
{{object.name | default: "item"}}
{{stats.value | default: 0}}
```

### Graceful degradation
```liquid
{{#if user.avatar_url}}
  <img src="{{user.avatar_url}}" />
{{else}}
  <div class="avatar-fallback">{{user.initials}}</div>
{{/if}}
```

### Error states
```liquid
{{#if error}}
  <div class="error-message">
    {{error.friendly_message | default: "Something went wrong. Please try again."}}
  </div>
{{/if}}
```

---



# Transactional email best practices

## Deliverability best practices

### Use a subdomain
Send transactional emails from a subdomain to prevent damaging your primary domain's reputation. Always use different subdomains for transactional vs. marketing emails.

**Why it matters**: Marketing emails are more likely to be flagged as spam. Separating them protects your critical transactional messages.

**Avoid**: Look-a-like domains (spammers use these, and email providers penalize them)

**Domain warming**: Each new subdomain must be warmed up by slowly increasing sending volume over time.

### Don't use no-reply emails
No-reply emails signal one-way communication and decrease trust with mailbox providers. Receiving replies actually improves your domain health.

### Avoid link and open tracking when possible
While valuable for marketing emails, link tracking and open tracking can hurt deliverability for transactional emails like notifications and magic links if the link doesn't contain your domain.

### Keep emails small and accessible
- **Gmail size limit**: 102KB (content is clipped after this)
- **Include plain text version**: Ensures accessibility for all email clients
- **Minimize images**: Helps with both size and accessibility

### Maintain a clean email list
Only send to recipients who've requested to receive emails:
- Don't send to unsubscribers
- Remove non-engaged recipients
- Remove spam complaint addresses
- Set up automated workflows to track bounces (hard or soft) and remove those recipients

### Send consistently
Mailbox providers are suspicious of sudden volume changes. To send thousands of emails regularly:
- Warm up your domain by sending consistently ahead of time
- Avoid sudden spikes in volume
- Inconsistent sending leads to bounce rates and reputation damage

## Email template best practices

### Use componentized templates
Modern transactional email requires a componentized approach that mirrors frontend development best practices.

**Basic hierarchy:**
```html
<!-- Email Layout (the frame) -->
<html>
  <head>
    {{ styles }}
  </head>
  <body>
    {{ header_partial }}
    
    <div class="content">
      {{ content }}  <!-- Your template content goes here -->
    </div>
    
    {{ footer_partial }}
  </body>
</html>
```

**Individual template:**
```html
<!-- Password Reset Template -->
<h1>Reset your password</h1>
<p>Hi {{ user.name }},</p>
<p>Click the link below to reset your password:</p>
<a href="{{ reset_link }}" class="button button-primary">
  Reset Password
</a>
```

**Benefits:**
- **Consistency**: Update header once, it changes everywhere
- **Maintainability**: No hunting through 50 templates to update a logo
- **Flexibility**: Different layouts for different email types

### Build a partial system
Partials are reusable chunks of email content that can be included across multiple templates.

**Reusable UI component example:**
```html
<!-- _button.liquid partial -->
<table class="button-wrapper">
  <tr>
    <td class="button {{ variant | default: 'primary' }}">
      <a href="{{ url }}">{{ text }}</a>
    </td>
  </tr>
</table>

<!-- Usage in template -->
{% include '_button' url: product_url, text: "View Order", variant: "secondary" %}
```

**Dynamic content block example:**
```html
<!-- _order_summary.liquid partial -->
<div class="order-summary">
  <h3>Order #{{ order.number }}</h3>
  <ul class="item-list">
    {% for item in order.items %}
      <li>
        <span class="item-name">{{ item.name }}</span>
        <span class="item-quantity">× {{ item.quantity }}</span>
        <span class="item-price">{{ item.price | currency }}</span>
      </li>
    {% endfor %}
  </ul>
  <div class="order-total">
    Total: {{ order.total | currency }}
  </div>
</div>
```

## Localization best practices

### Use translation keys
Organize content into hierarchical JSON structures for easy language swapping.

**Translation files:**
```json
// translations/en.json
{
  "password_reset": {
    "subject": "Reset your password",
    "greeting": "Hi {{name}},",
    "body": "We received a request to reset your password.",
    "cta": "Reset Password",
    "expiry_warning": "This link expires in {{hours}} hours.",
    "footer": "If you didn't request this, please ignore this email."
  }
}

// translations/es.json
{
  "password_reset": {
    "subject": "Restablecer tu contraseña",
    "greeting": "Hola {{name}},",
    "body": "Recibimos una solicitud para restablecer tu contraseña.",
    "cta": "Restablecer Contraseña",
    "expiry_warning": "Este enlace expira en {{hours}} horas.",
    "footer": "Si no solicitaste esto, ignora este correo."
  }
}
```

**Template usage:**
```html
<h1>{{ "password_reset.subject" | t }}</h1>
<p>{{ "password_reset.greeting" | t: name: user.first_name }}</p>
<p>{{ "password_reset.body" | t }}</p>
<a href="{{ reset_url }}">
  {{ "password_reset.cta" | t }}
</a>
<p class="warning">
  {{ "password_reset.expiry_warning" | t: hours: 24 }}
</p>
```

## Dynamic content best practices

### Conditional logic
Adapt content based on user behavior and account status.

**Example:**
```html
{% if user.is_premium %}
  <div class="premium-banner">
    <h3>Thanks for being a Premium member!</h3>
    <p>You saved {{ order.premium_discount | currency }} on this order.</p>
  </div>
{% elsif user.trial_ending_soon %}
  <div class="trial-banner">
    <h3>Your trial ends in {{ user.trial_days_left }} days</h3>
    <a href="{{ upgrade_url }}">Upgrade to keep your benefits</a>
  </div>
{% endif %}

<!-- Dynamic CTAs based on user state -->
{% case user.onboarding_step %}
{% when 'profile_incomplete' %}
  <a href="{{ complete_profile_url }}" class="button">
    Complete Your Profile
  </a>
{% when 'payment_pending' %}
  <a href="{{ add_payment_url }}" class="button">
    Add Payment Method
  </a>
{% else %}
  <a href="{{ dashboard_url }}" class="button">
    Go to Dashboard
  </a>
{% endcase %}
```

### Usage statistics
Share relevant metrics and insights in transactional emails.

**Example:**
```html
<!-- Weekly summary email -->
<div class="usage-stats">
  <h2>Your week at a glance</h2>
  
  <div class="stat-grid">
    <div class="stat">
      <span class="value">{{ stats.tasks_completed }}</span>
      <span class="label">Tasks completed</span>
      <span class="change {{ stats.tasks_change_class }}">
        {{ stats.tasks_change }}% vs last week
      </span>
    </div>
    
    <div class="stat">
      <span class="value">{{ stats.time_saved | format_duration }}</span>
      <span class="label">Time saved</span>
    </div>
  </div>
  
  <!-- Personalized insight -->
  {% if stats.most_productive_day %}
    <p class="insight">
      💡 You're most productive on {{ stats.most_productive_day }}s. 
      Consider scheduling important work then!
    </p>
  {% endif %}
</div>
```

### Behavioral personalization
Use browsing history and user data for relevant recommendations.

**Example:**
```html
<!-- In an order confirmation email -->
{% if related_products.size > 0 %}
  <div class="recommendations">
    <h3>You might also like</h3>
    <div class="product-grid">
      {% for product in related_products limit: 3 %}
        <div class="product-card">
          <img src="{{ product.image_url }}" alt="{{ product.name }}">
          <h4>{{ product.name }}</h4>
          <p>{{ product.price | currency }}</p>
          
          <!-- Smart messaging based on user history -->
          {% if product.id in user.previously_viewed %}
            <span class="badge">Previously viewed</span>
          {% elsif product.discount > 0 %}
            <span class="badge">{{ product.discount }}% off</span>
          {% endif %}
        </div>
      {% endfor %}
    </div>
  </div>
{% endif %}
```

## Mobile optimization

### Design considerations
- Use single-column layouts
- Minimum button size: 44x44 pixels
- Minimum font size: 14px
- Keep images under 1MB
- Maintain 80:20 text-to-image ratio

### Testing requirements
- Test across major email clients (Gmail, Outlook, Apple Mail)
- Test on multiple device sizes
- Verify subject line and preview text truncation
- Check CTA button functionality
- Ensure images load properly

---



# Welcome email best practices

## Why send a welcome email?

Welcome emails are critical first touchpoints with new users:
- **74% of consumers** expect welcome emails immediately after signup
- Above-average open rates (typically 60%+ vs ~20% for standard emails)
- Can generate **10x more revenue** than standard promotional emails
- Set the foundation for product adoption and user engagement

## Elements of an effective welcome email

### Subject line
**Guidelines:**
- Keep it brief and contextual
- Focus on confirming the signup action
- Simple "Welcome to [Company]" works great

**Why simple works**: Users already expect this email. No need for clickbait—they'll open it.

### Preview text
**Guidelines:**
- Expand on your subject line with additional context
- Briefly explain what's inside the email
- Tell users what's in it for them
- Make it readable even if truncated

**Character limits:**
- Desktop: ~90 characters
- Mobile: ~35 characters

**Examples:**
```
👀 Review their feedback and approve changes directly from this email
⏳ You have 24 hours left to claim your early bird discount. Register now
💬 Sarah Chen and 2 others are waiting for your input on the roadmap
```

### Email body content
**Guidelines:**
- Lead with one clear benefit (not features)
- Use short paragraphs (2-3 sentences max)
- Use active CTAs that describe the outcome
  - Good: "Create your first workflow"
  - Bad: "Get started"
- Buttons usually outperform text links
- Maintain 80:20 text-to-image ratio for accessibility

**Mobile considerations:**
- Use single-column layouts
- Button sizes: minimum 44x44 pixels
- Font sizes: minimum 14px for mobile
- Images: stay under 1MB

## Welcome email patterns

### Pattern 1: Founder-led welcome
**When to use**: Building personal connection and trust
**Example structure**:
```
Personal greeting from founder
→ Core value proposition
→ 2-3 immediate action paths
→ Founder signature with photo
```

**What works**:
- Creates immediate connection
- Builds trust through transparency
- Demonstrates company values
- Humanizes the brand

### Pattern 2: Quick start guide
**When to use**: Complex products needing guidance
**Example structure**:
```
Welcoming header
→ 3-step action plan
→ Primary CTA (get started)
→ Secondary resources
```

**What works**:
- Removes ambiguity about next steps
- Provides clear learning path
- Reduces cognitive load
- Drives immediate action

### Pattern 3: Value-first approach
**When to use**: Products with clear, immediate benefits
**Example structure**:
```
Benefit statement
→ What you can do now
→ How to get more value
→ Support resources
```

**What works**:
- Focuses on outcomes, not features
- Demonstrates immediate value
- Provides progressive enhancement
- Shows commitment to success

### Pattern 4: Community introduction
**When to use**: Community-driven products
**Example structure**:
```
Welcome to the community
→ How the community works
→ Starting points/recommendations
→ Community guidelines
```

**What works**:
- Reduces intimidation
- Provides safe starting points
- Explains unique systems
- Builds sense of belonging

### Pattern 5: Resource hub
**When to use**: Multiple user types or use cases
**Example structure**:
```
Brief welcome
→ Multiple paths organized by user type
→ Interactive tour option
→ Free tools/resources
```

**What works**:
- Respects diverse user needs
- Allows self-directed exploration
- Provides comprehensive information
- Reduces support burden

## Timing best practices

### When to trigger
Send welcome emails **shortly after signup**, but consider these factors:

**Immediate send (within seconds):**
- Account verification emails
- Simple products with minimal onboarding
- SaaS tools with instant access

**Delayed send (after product interaction):**
- Products with guided onboarding flows
- Wait for user to interact with onboarding
- Complex products where in-app guidance comes first

**Why wait for interaction:**
- User is already engaged with product
- Can reference actual product actions
- Avoids redundant communication
- Can conditionally send based on completion

## Content best practices

### Lead with value, not features
**Bad example:**
```
Our platform has 50+ features including:
- Advanced analytics
- Real-time collaboration
- Custom integrations
```

**Good Example:**
```
Get your team aligned in minutes:
→ See what matters with instant insights
→ Work together in real-time
→ Connect the tools you already use
```

### Use concrete examples
**Bad example:**
```
Our tool helps you be more productive
```

**Good Example:**
```
Turn "Check if the report is ready" into:
- Automatic notifications when reports complete
- One-click access to the latest data
- Weekly summaries sent to your team
```

### Make CTAs outcome-focused
**Bad CTAs:**
- "Get Started"
- "Learn More"
- "Click Here"

**Good CTAs:**
- "Create your first workflow"
- "See your dashboard"
- "Import your team"
- "Start your first project"

### Address common objections
**Time concerns:**
```
"Just a few minutes a day" — Headspace
```

**Complexity concerns:**
```
"We'll guide you through it" — with step-by-step plan
```

**Value concerns:**
```
"See results in your first session" — with concrete example
```

## Design best practices

### Match product aesthetic
The email design should feel like an extension of your product:
- Use consistent brand colors
- Match typography
- Mirror UI patterns
- Maintain visual hierarchy

**Why it matters**: Familiarity reduces friction and builds trust

### Use visual hierarchy
**Priority order:**
1. Welcome message (largest, most prominent)
2. Primary value proposition
3. Main CTA (biggest button)
4. Supporting content
5. Secondary resources

### Incorporate social proof
**Examples:**
- User count: "Join 12 million users"
- Customer logos: Fortune 100 trust badges
- Testimonials: Brief user quotes
- Usage stats: "2 million workflows created"

**Placement**: After value prop, before CTAs

## Common mistakes to avoid

### Too much information
**Problem**: Overwhelming users with everything at once
**Solution**: Focus on one primary action and 2-3 supporting resources

### Feature dumping
**Problem**: Listing features without context
**Solution**: Connect each feature to a user benefit

### Multiple primary CTAs
**Problem**: Unclear what action to take first
**Solution**: One primary CTA, clear hierarchy for secondary actions

### Forgetting mobile
**Problem**: Email looks great on desktop but breaks on mobile
**Solution**: Always test on mobile devices, use responsive design

### No clear next step
**Problem**: User opens email but doesn't know what to do
**Solution**: One clear, prominent action users should take

## Testing checklist

Before sending welcome emails:

**Technical tests:**
- ✅ Test across email clients (Gmail, Outlook, Apple Mail)
- ✅ Verify mobile rendering
- ✅ Check link functionality
- ✅ Test personalization variables
- ✅ Verify unsubscribe link works

**Content tests:**
- ✅ Subject line clear and contextual
- ✅ Preview text adds value
- ✅ Main CTA prominent and outcome-focused
- ✅ Copy scans well (short paragraphs)
- ✅ Images load properly

**User experience tests:**
- ✅ Primary action obvious within 3 seconds
- ✅ Value proposition clear
- ✅ Works without images
- ✅ Accessible (screen reader friendly)
- ✅ Loads quickly

## Measurement and optimization

### Key metrics to track
**Immediate metrics:**
- Open rate (target: 60%+)
- Click-through rate (target: varies by industry)
- Time to open (target: within 1 hour)

**Engagement metrics:**
- Completion of suggested actions
- Return visits to product
- Feature adoption from welcome email

**Business metrics:**
- Activation rate
- Trial-to-paid conversion
- Long-term retention

### A/B test ideas
**Subject lines:**
- Company name vs. benefit-focused
- Length variations
- Personalization vs. generic

**CTAs:**
- Outcome-focused vs. generic
- Button text variations
- Number of CTAs

**Content:**
- Founder message vs. product focus
- Feature education vs. quick start
- Long vs. short format

---
