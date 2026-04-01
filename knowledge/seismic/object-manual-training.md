# Object Manual Training

*Source: references/seismic learning/Object Manual Training.pdf*
*Pages: 100 | Characters: 74,925*

---

<!-- Page 1 -->
Object Manual Training
Overview of all of the key Objects in Salesforce, their purpose, child objects, record types and most used
fields.

---

<!-- Page 2 -->
Introduction
In this lesson, we will focus on key Salesforce objects. These objects play vital roles in
Sanguine's business model. By understanding their purpose and workflows, we can gain
insight into their diverse applications across various departments. Join us as we delve into
these essential Salesforce objects and explore their functionalities in detail.

---

<!-- Page 3 -->
Object Manual
Each Object SME Listed here.
Purpose of the object
List of record type(s) - please review this and ensure all record types are used
Purpose of Record Type(s) - listed in Object Manager
Defining Record Type
List of child objects and the use case of it
Most commonly used Fields (Use case) - this can be incorporated as you go
High level workflow within the object
which department(s) use the objects the most/ who creates them (include this as
applicable)
Lead
Purpose of the object: lead object is utilized to capture contact information regarding a
prospect as well as track activity defined as emails, phone calls, linkedin correspondence,
meetings, etc.
Record type:
Scientist - scientist working at pharmaceutical or biotech company

---

<!-- Page 4 -->
Academic Scientist - scientist working at academic institution such as a college, university
or research hospital
CGT Development - persona characterized by specific titles associated with cell & gene
therapy working at a company/within a department specializing in cell & gene therapy
Ex titles:
Process Development
Cell Therapy scientist
Clinical Development - member of the research team focused on clinical trial development/
work.
Diagnostic Scientist - a scientist who works at a diagnostic company
Manufacturing - individuals working at a CDMO
Other
Procurement & Outsourcing - a persona of individuals who focus on the procurement and
outsourcing of biospecimens and data for a research team
Child Objects
Incidence Checks: Incidence Checks are a way to track requests we get from leads or
contacts and assess the feasibility of that request. It is saved on the lead / contact so we
can see their previous requests and go back to them if something in our feasibility process
changes to accommodate their request
Campaign history: Shows us the first and last touch points of marketing campaigns, date,

---

<!-- Page 5 -->
lead source, medium, content, date and other details that led to lead creation in SFDC
Gong Conversations: Highlights recent Gong conversations from our sync
Lead History
Tracks lead creation, changes of lead ownership
Most commonly used Fields (Use case)
Name
Company
Title
Lead record type
Reporting matched account - The account the lead belongs to. This could be a child or
parent account. Leads are matched either manually or through the tool lean data which rev
ops manages
Last lead owner - in case the lead ownership has changed hands
Lead owner - who is responsible for engaging with the lead
Lead status
New
MQL

---

<!-- Page 6 -->
In Cadence
Working (trying to schedule a meeting/opportunity with)
Unqualified
Qualified
Qualified No Opp
Qualified with Opp (leads who we had a meeting with and were expecting an imminent
opportunity from)
Nurture
Cold
Bounced
Unqualified - DNQ
Disqualification reason - entered by SDR or AE
Competitor
Industry mismatch
Looking for courier service
Budget
Clinical trials

---

<!-- Page 7 -->
Patient inquiry
Advertisement
HR
Sample Use Purpose
Company Bad Fit
Does not use Patient Samples
Phone
Email
Address
Last activity by sales - pulled automatically
Matched account parent ID
Account owner
Website
Lead source - generated automatically, or manually updated depending on the way the
lead is identified
3rd party referral
AdWords

---

<!-- Page 8 -->
Chat
CSM Referral
Email
List Purchase
Lunch & Learn
Marketing List Purchase
On-Site Marketing
Paid Ad
Partner
PM Referral
Public Relations
Rocketseed
Sales Generated
Sales Referral
Sanguine Bio
Seminar

---

<!-- Page 9 -->
Survey
Tradeshow
Webinar
Website
Lead source detail - additional details
Source type: Identifies if this is Marketing Source Lead or Sales Source Lead
Original lead source: Tracks original source, even if it gets changed later. For example: a
lead may attend a Marketing webinar, but Sales could have sourced the opportunity from
an existing relationship. Both contribute to the opportunity.
Original lead source detail
Lead status change date
Prior lead status
Days in status - helps track how often the lead has moved between changes
Mql date: The date on which the leads get created in SFDC that come in through website
form submissions or through chat and learnmore
Sal date: When sales start their cadence for the marketing leads
Sql date: The date when a new opportunity is created out of a Marketing lead
Sold date

---

<!-- Page 10 -->
# of mqls: Number if leads that get created through website form submissions or through
chat and learnmore
MQL to SAL: Marketing Leads that get qualified for sales cadence
SAL to SQL: When the Marketing leads turn to an opportunity for new pipeline
High level workflow within the object
Lead to contact conversion with opportunity creation
Lead status changes:
Ex: lead MQLs and status of lead changes to MQL
Ex: lead converted to contact upon opp creation - status becomes qualified with
opportunity
Lead routing using lean data
Lead info pushing to secondary CRM (Salesloft currently, gong by eoq2)
Which department(s) use the objects the most/ who creates them
Sales: Sales primarily uses Leads to put into cadences to target them for meetings and
potential opportunities.
SDR
AE
Marketing: Marketing generates leads from campaigns, webinars, online sourcing etc. It is

---

<!-- Page 11 -->
important for them to track where our leads are coming from so they can better understand
where to spend their budget that will lend to the best results.
Sales: Sources leads through linkedin Sales Navigator, Lead IQ, Apollo and Zoom info.
Lead emails are cleansed for accuracy prior to being imported into the CRM. Lead info is
manually updated as we do not have a backend sync to enrich data.
Campaign
Patient Recruitment:
Purpose: Campaign object is utilized to track all patient recruitment campaigns entered into
our CRM with our patient recruitment vendors, NPOs, and online channels.
Record Types:
Parent - Condition level campaign. How much budget and spend we have for that specific
condition for the year.
Patient Marketing - Patient Recruitment vendor & online channel campaigns
NPO/Support - NPO/support group campaigns
Child Objects/Related List:
Campaign Hierarchy - all of the different vendors/channels we utilized to recruit patients
Expenditures - Budget we have for each study and cost we spent for each study
Most commonly used fields:
Campaign Name

---

<!-- Page 12 -->
Responses in Hierarchy - Number of signups
Actual cost in Hierarchy - Cost of the specific campaign
Start Date/End Date
Status
In Progress
Completed
Aborted
Planned
Budget Used %
Master Plan_A - MP Name
Workflow:
Campaigns are created and executed by the Patient Recruitment team to build a campaign
and target the correct channel (online vendors or NPO/PAG). A Salesforce campaign is
created before we launch the recruitment campaign with the vendor or NPO/PAG. Once the
campaign is launched, all departments will have visibility to see the total number of signups
and spend for each campaign.
Campaigns are created and executed on by Marketing and Patient Recruitment Marketing
teams to build a campaign and target the correct markets. They send out these campaigns
through Marketo, Salesforce, and our online vendors

---

<!-- Page 13 -->
Which department(s) use the objects the most/ who creates them: Campaigns are primarily
used by Marketing and Patient Recruitment Marketing to identify patients and new leads
coming in through various tactics
Account
Purpose of the object: Account objects are used to record current Sanguine customers and
all potential Sanguine customers in our addressable market. They contain information
about each account that is necessary for sales and marketing to generate revenue.
List of record type(s):
Parent Shell: Parent accounts act as a “catch-all” account for a company's different
geographic locations. Parent Shells are created for every single account record type
(Pharma & Biotech, CDMO, Research Institute, Diagnostic Companies).
Ex 1: locations: (e. g. Abbvie Chicago & Abbvie Boston roll-up to Abbvie Parent Shell)
Ex 2: companies subsidiaries (e. g. Genentech rolls up to Roche Parent Shell)
Pharma & Biotech: Pharmaceutical and biotechnology working on therapeutics (drugs) to
treat different diseases. Traditional Sanguine customers
CDMO: Contract Development and Manufacturing Organizations. These companies
manufacture drugs on a contract basis for pharma and biotech companies. Newer type of
Sanguine customer
Diagnostic Companies: Life science companies that develop diagnostics and medical
devices used to diagnose diseases. Newer type of Sanguine customer
Research Institutes: Life science research institutes that fall into one of these categories:

---

<!-- Page 14 -->
Hospitals, Non-profits, and academic research centers. Newer Sanguine customers with
typically lower budgets
Apheresis Clinic
CRO
Distributor
Business
Household
Individual
Payer
Patients
Non customers
Partners
Purpose of Record Type(s) - purpose is to understand differences in buying habits based
on account type, target new clients, product mix based on account type
Child Objects
Contact
Opportunity

---

<!-- Page 15 -->
Account plans
Most commonly used Fields (Use case)
Account Name
Parent Account Name (Links to associated Parent Record Type)
Account Owner
Account Priority
Strategic Active: LTV >$500K
Strategic Potential: LTV <$500K
Public Active: Account is publicly traded, historically has done business with Sanguine
Public Potential: Account is publicly traded, historically has not done business with
Sanguine
Private Active: Account is privately owned;, historically has done business with Sanguine
Private Potential: Account is privately owned;, historically has not done business with
Sanguine
Account Record Type (noted above)
Territory SDR
Project Lead Name

---

<!-- Page 16 -->
Phone
Website
Cell and Gene Therapy Company (checkbox, yes or no)
Area of Interest (therapeutic area)
LTV (historical sum of bookings)
Shipping address
Billing address
CDA on file (checkbox, yes or no)
MSA on file (checkbox, yes or no)
MSA net payment terms
High level workflow within the object
Account objects are created via account list pulls from sales/marketing. The goal here is to
add as many accounts as possible in our addressable market for marketing and sales
prospecting of new business. Product and Marketing makes the decision prior to uploading
new accounts in the CRM as to which account record type they best correspond to.
Once these accounts are pulled, they are assigned to an SDR and AE owner, who are
responsible for generating bookings from each individual account. Lead lists are also pulled
for each account object, and as opportunities are created, they are associated with the
correct Account in the CRM.

---

<!-- Page 17 -->
Which department(s) use the objects the most/ who creates them:
Sales and marketing create new account record types via Account list pulls (zoominfo or
other platforms), or as inbound opportunities from accounts that are not in the CRM
appear. Sales Primarily utilizes the Account Record type as they use this information for
territory planning and prospecting both new and existing clients. In addition, marketing
uses account record types for email blasts, google ads, and Account based marketing
(ABM). Finally, the project management & finance teams use these objects for invoicing
client projects. This Object is relevant to all of Sanguine to understand who our customers
are and who our potential customers are.
Contact (Commercial):
Purpose of the object: The purpose is to create records of contact information and persona
details for individuals who work at Sanguine customer accounts. Contacts are converted
from leads when an opportunity is created and associated with a lead
List of record type(s):
Scientist - a scientist working at a pharmaceutical or biotech company
Academic Scientist - a scientist working at an academic institution such as a college,
university or research hospital. Correspond to Research Institute account record type
CGT Development - persona characterized by specific titles associated with cell & gene
therapy working at a company/within a department specializing in cell & gene therapy
Ex titles:
Process Development

---

<!-- Page 18 -->
Cell Therapy scientist
Clinical Development - a member of the research team focused on clinical trial
development/work.
Diagnostic Scientist - a scientist who works at a diagnostic company. Corresponds directly
to account record type Diagnostic Company
Manufacturing - individuals working at a CDMO. Corresponds directly to account record
type CDMO
Other
Procurement & Outsourcing - a persona of individuals who focus on the procurement and
outsourcing of biospecimens and data for a research team
Purpose of Record Type(s) - listed in Object Manager
To define the various personas for Contacts
List of child objects and the use case of it
Incidence Checks: Incidence Checks are a way to track requests we get from leads or
contacts and assess the feasibility of that request. It is saved on the lead / contact so we
can see their previous requests and go back to them if something in our feasibility process
changes to accommodate their request
Health profile
Most commonly used Fields (Use case)
Name

---

<!-- Page 19 -->
Title
Account Name
Contact owner (AE or SDR)
Contact Record Type
Email Address
Phone
Mailing Address
Contact Stage
Number of Total Opportunities
Number of Closed Won Opportunities
Lead Source
Area of Interest (therapeutic area)
Product of interest (Leukopak, translational, onsite, etc. )
SAL Date - Sales Accepted Lead Date - Date a meeting is scheduled with a lead
SQL Date - Sales Qualified Lead Date- Date an opportunity is created and a lead is
converted to a contact
Original SQL date - first time SQL conversion takes place

---

<!-- Page 20 -->
Last Activity Date by Sales - The last date in which a member of the sales team (SDR or AE)
have interacted with the lead
High level workflow within the object
Lead objects are converted to contacts upon opportunity creation. All contacts in the CRM
must have an associated opportunity in order for the conversion to work, and Account
Executives or less commonly, SDRs, are the individuals converting leads from contacts
Which department(s) use the objects the most/ who creates them
Sales and marketing use contacts the most. For sales, contacts represent direct customers
who are leading the opportunity lifecycle from the client's side. In addition, contacts are
usually repeat buyers, so sales goes back to past contacts at various accounts for account
mining and to prevent churn.
Project management also uses contacts as the main POC, typically, for an ongoing study.
Unless otherwise state by sales, the PM team is setting up a kickoff call and acting as a
day to day POC for the contact on a given closed won opportunity
Opportunity
Purpose: Opportunity Object is utilized to track all opportunities entered into our CRM for
pipeline, bookings (closed-won) and lost opportunities (closed-lost). The opportunity
houses many child objects and workflow to provide as much information about the account
as possible. The Opportunity Object is a child object to the Account Object.
Opportunity Record Type(s)
Translational: All Standard Translational Studies

---

<!-- Page 21 -->
Change Order: Used to capture Change Orders to an existing Opportunity
Entered by PM/Feasibility after PC has been created
Clinical Trial: Clinical Trial Opportunities
Community Access Parent: Community Access Programs
Community Access - Related: Used for related Community Access Services Request
Opportunities, related to a Parent Community Access Opportunity.
Entered by PM
Inventory / Banked Samples: Inventory Orders (Mayo & San Diego)
Lab Services & Storage: Processing and sample storage
Leukopak - Healthy: Leukopak Studies for Healthy Leukopaks
Healthy Leuko - Related (used for orders under blanket healthy leukopak record type)
Leukopak - Diseased: Diseased Leukopaks
LeukoLot: PBMC vials of Leukopaks used for screening purposes
Leukopak - GMP
Leukopak - Mobilized
Onsite Record Types: Onsite Programs
Child Objects

---

<!-- Page 22 -->
Cohort - contains full study design detail by indication (more details in object)
Master Plan - associated with opportunity for projects that are closed won
Project Changes - any changes to the opportunity after it is closed won
Products - all the products on the opportunity for pricing purposes
Quotes - pricing and discount history on the quote, compiled of products
Approval History - tracking of the approval process in Stage 2
Notes & Attachments - where all relevant documentation is stored (attachments, proposal
drafts, sows)
NetSuite Financials - tracking of billing for closed won studies
I/E Criteria - details of inclusion / exclusion criteria
Most Common Fields
Stages: Stages represent the workflow of our Sales Process from Opportunity Entry and
detail gathering to Opportunity Closed - won or lost. Each Stage has various fields and
child objects (listed below) that need to be utilized to effectively enter the data we need to
review a deal
Stage 1: Information Gathering
Cohort Object: Purpose: Cohort contains all of the information that pulls from the Study
Request Form involving all details pertinent to the study design. Feasibility to update
further with the following information:

---

<!-- Page 23 -->
Study-specific assumptions (including assumptions for pricing)
Inclusion/Exclusion criteria
Biospecimen collection details
In-home processing details
Kitting details
Lab processing and testing details
Shipping details
Managed by Account Executive and Feasibility
Fields to fill out in Stage 1:
Close Date - when this is expected to close
Estimated study budget
Estimated timeline
Vendor Features they are most interested in
AOI (Area of Interest)
Product of Interest
Pain points - relevant to deal

---

<!-- Page 24 -->
Study Requirements - entered via cohort
Convert lead to Contact for the opportunity
Contact Roles:
Economic Buyer (Procurement/Contracts)
Business User (Sample user)
Decision Maker
Influencer (Opp contact, has influence on the deal moving forward)
Contacts are clients who have engaged with us on an opportunity
Managed by Account Executive and Feasibility
Stage 2: Feasibility Review
Approval workflow - ORT
Quote is created
Quote Purpose: Quote contains a compilation of all products associated with the
opportunity and study design for the opportunity price, including:
Product
Product Type
Study Setup

---

<!-- Page 25 -->
IRB Fees
Project Management and Support
Patient Access & Reservation
Data and Screening Services
Subject Reimbursement & Reservation
Kitting (Supplies and Services)
Home Visit Services
Shipping and Logistics
Pre-Analytical Lab Services
CLIA Analytical Services
Billing Cycle
Upfront
Per Visit
Manual
Monthly
Discount

---

<!-- Page 26 -->
Quantity
Total Price
Quotes are created and managed by Feasibility
Account Executives can create quotes and adjust quotes with Feasibility approval
Quote Stages and Workflows
Draft
Presented: AE has presented the proposal
In Review: Discount has been requested
Will go to AE leader, Feasibility leader and CEO to approve
Approved: Discount Approved
Rejected: Discount Rejected
Accepted: Create work order
Denied
Quality Check
Finalized: SOW Complete
Proposal Generation

---

<!-- Page 27 -->
Stage 3: Proposal Delivery - Feasibility has approved and created proposal
Fill in the following fields:
Adding proposal delivery date and check box so you know proposal has been delivered
and when
Obtain decision making process
Add/convert additional contacts
Update Budget
Price per sample→ update if client provides feedback
Estimated study budget→ update to marketing section if this has changed from SRF
Add objections, concerns, or other key details
Estimated Study Completion date (when the client needs all of the samples by)
Stage 4: Active Negotiation
Quote to “Presented”
Next Step
What is the purpose of the Lead object?
Lead object is utilized to capture contact information regarding a prospect as well as track
activity defined as emails, phone calls, linkedin correspondence, meetings, etc.

---

<!-- Page 28 -->
Keypoints
• Lead captures contact information for prospects
• Scientist, Academic Scientist, Clinical Development, and more record types
• Child Object: Incidence Checks, Campaign history, Gong Conversations
• Lead status, last activity, lead source, and more used fields
• Lead to contact conversion with opportunity creation workflow
• Sales, SDR, and Marketing departments use leads the most
• Campaigns object tracks patient recruitment campaigns
• Record Types: Parent, Patient Marketing, NPO/Support
• Campaign Hierarchy, Expenditures related list, and workflow overview
• Used by Marketing and Patient Recruitment Marketing teams
• Account records current and potential customers' information
• List of Record Types: Parent Shell, Pharma & Biotech, CDMO
• Contact, Opportunity, and Account plans are child objects
• Account Name, Account Owner, Account Priority, and more used fields
• Created via account list pulls, assigned to an SDR and AE
• Sales and marketing create new account record types
• Contact captures information for individuals at customer accounts
• Record Types: Scientist, Academic Scientist, CGT Development, and more
• Child Object: Incidence Checks, Health profile

---

<!-- Page 29 -->
• Name, Title, Contact owner, Email Address, and more used fields
• Converted from leads upon opportunity creation
• Primarily used by Sales and marketing
• Opportunity tracks pipeline, bookings, and lost opportunities
• Record Types: Translational, Change Order, Clinical Trial, and more
• Child Objects: Cohort, Master Plan, Project Changes, and more
• Stages, Cohort, and Quote purpose and stages
• Managed by Account Executive and Feasibility

---

<!-- Page 30 -->
Lead
Lead
1. Purpose of the object: lead object is utilized to capture contact information regarding
a prospect as well as track activity defined as emails, phone calls, linkedin
correspondence, meetings, etc.
a. Record type:
i. Scientist - scientist working at pharmaceutical or biotech company
ii. Academic Scientist - scientist working at academic institution such as a
college, university or research hospital
iii. CGT Development - persona characterized by specific titles associated with
cell & gene therapy working at a company/within a department specializing in
cell & gene therapy
i. Ex titles:
i. Process Development
ii. Cell Therapy scientist
iv. Clinical Development - member of the research team focused on clinical trial
development/work.
v. Diagnostic Scientist - a scientist who works at a diagnostic company

---

<!-- Page 31 -->
vi. Manufacturing - individuals working at a CDMO
vii. Other
viii. Procurement & Outsourcing - a persona of individuals who focus on the
procurement and outsourcing of biospecimens and data for a research team
2. Child Objects
a. Incidence Checks: Incidence Checks are a way to track requests we get from
leads or contacts and assess the feasibility of that request. It is saved on the lead /
contact so we can see their previous requests and go back to them if something in
our feasibility process changes to accommodate their request
b. Campaign history: Shows us the first and last touch points of marketing
campaigns, date, lead source, medium, content, date and other details that led to
lead creation in SFDC
c. Gong Conversations: Highlights recent Gong conversations from our sync
d. Lead History
i. Tracks lead creation, changes of lead ownership
3. Most commonly used Fields (Use case)
a. Name

---

<!-- Page 32 -->
b. Company
c. Title
d. Lead record type
e. Reporting matched account - The account the lead belongs to. This could be a
child or parent account. Leads are matched either manually or through the tool
lean data which rev ops manages
f. Last lead owner - in case the lead ownership has changed hands
g. Lead owner - who is responsible for engaging with the lead
h. Lead status
i. New
ii. MQL
iii. In Cadence
iv. Working (trying to schedule a meeting/opportunity with)
v. Unqualified

---

<!-- Page 33 -->
vi. Qualified
vii. Qualified No Opp
viii. Qualified with Opp (leads who we had a meeting with and were expecting an
imminent opportunity from)
ix. Nurture
x. Cold
xi. Bounced
xii. Unqualified - DNQ
i. Disqualification reason - entered by SDR or AE
i. Competitor
ii. Industry mismatch
iii. Looking for courier service
iv. Budget

---

<!-- Page 34 -->
v. Clinical trials
vi. Patient inquiry
vii. Advertisement
viii. HR
ix. Sample Use Purpose
x. Company Bad Fit
xi. Does not use Patient Samples
j. Phone
k. Email
l. Address
m. Last activity by sales - pulled automatically
n. Matched account parent ID
o. Account owner

---

<!-- Page 35 -->
p. Website
q. Lead source - generated automatically, or manually updated depending on the
way the lead is identified
i. 3rd party referral
ii. AdWords
iii. Chat
iv. CSM Referral
v. Email
vi. List Purchase
vii. Lunch & Learn
viii. Marketing List Purchase
ix. On-Site Marketing
x. Paid Ad
xi. Partner

---

<!-- Page 36 -->
xii. PM Referral
xiii. Public Relations
xiv. Rocketseed
xv. Sales Generated
xvi. Sales Referral
xvii. Sanguine Bio
xviii. Seminar
xix. Survey
xx. Tradeshow
xxi. Webinar
xxii. Website
r. Lead source detail - additional details
s. Source type: Identifies if this is Marketing Source Lead or Sales Source Lead

---

<!-- Page 37 -->
t. Original lead source: Tracks original source, even if it gets changed later. For
example: a lead may attend a Marketing webinar, but Sales could have sourced
the opportunity from an existing relationship. Both contribute to the opportunity.
u. Original lead source detail
v. Lead status change date
w. Prior lead status
x. Days in status - helps track how often the lead has moved between changes
y. Mql date: The date on which the leads get created in SFDC that come in through
website form submissions or through chat and learnmore
z. Sal date: When sales start their cadence for the marketing leads
aa. Sql date: The date when a new opportunity is created out of a Marketing lead
ab. Sold date
ac. # of mqls: Number if leads that get created through website form submissions or
through chat and learnmore
ad. MQL to SAL: Marketing Leads that get qualified for sales cadence

---

<!-- Page 38 -->
ae. SAL to SQL: When the Marketing leads turn to an opportunity for new pipeline
4. High level workflow within the object
a. Lead to contact conversion with opportunity creation
b. Lead status changes:
i. Ex: lead MQLs and status of lead changes to MQL
ii. Ex: lead converted to contact upon opp creation - status becomes qualified
with opportunity
c. Lead routing using lean data
d. Lead info pushing to secondary CRM (Salesloft currently, gong by eoq2)
5. Which department(s) use the objects the most/ who creates them
a. Sales: Sales primarily uses Leads to put into cadences to target them for meetings
and potential opportunities.
i. SDR
ii. AE
b. Marketing: Marketing generates leads from campaigns, webinars, online sourcing
etc. It is important for them to track where our leads are coming from so they can

---

<!-- Page 39 -->
better understand where to spend their budget that will lend to the best results.
c. Sales: Sources leads through linkedin Sales Navigator, Lead IQ, Apollo and Zoom
info. Lead emails are cleansed for accuracy prior to being imported into the CRM.
Lead info is manually updated as we do not have a backend sync to enrich data.

---

<!-- Page 40 -->
Campaign
Campaign
1. Purpose: Campaign object is utilized to track all patient recruitment campaigns
entered into our CRM with our patient recruitment vendors, NPOs, and online
channels.
a. Record Types:
i. Parent - Condition level campaign. How much budget and spend we have for
that specific condition for the year.
ii. Patient Marketing - Patient Recruitment vendor & online channel campaigns
iii. NPO/Support - NPO/support group campaigns
2. Child Objects/Related List:
a. Campaign Hierarchy - all of the different vendors/channels we utilized to recruit
patients
b. Expenditures - Budget we have for each study and cost we spent for each study
3. Most commonly used fields:
a. Campaign Name
b. Responses in Hierarchy - Number of signups

---

<!-- Page 41 -->
c. Actual cost in Hierarchy - Cost of the specific campaign
d. Start Date/End Date
e. Status
i. In Progress
ii. Completed
iii. Aborted
iv. Planned
f. Budget Used %
g. Master Plan_A - MP Name
4. Workflow:
a. Campaigns are created and executed by the Patient Recruitment team to build a
campaign and target the correct channel (online vendors or NPO/PAG). A
Salesforce campaign is created before we launch the recruitment campaign with
the vendor or NPO/PAG. Once the campaign is launched, all departments will have
visibility to see the total number of signups and spend for each campaign.
b. Campaigns are created and executed on by Marketing and Patient Recruitment

---

<!-- Page 42 -->
Marketing teams to build a campaign and target the correct markets. They send
out these campaigns through Marketo, Salesforce, and our online vendors
5. Which department(s) use the objects the most/ who creates them: Campaigns are
primarily used by Marketing and Patient Recruitment Marketing to identify patients and
new leads coming in through various tactics

---

<!-- Page 43 -->
Account
Account
1. Purpose of the object: Account objects are used to record current Sanguine
customers and all potential Sanguine customers in our addressable market. They
contain information about each account that is necessary for sales and marketing to
generate revenue.
• List of record type(s):
◦Parent Shell: Parent accounts act as a “catch-all” account for a company’s
different geographic locations. Parent Shells are created for every single
account record type (Pharma & Biotech, CDMO, Research Institute,
Diagnostic Companies).
▪Ex 1: locations: (e.g. Abbvie Chicago & Abbvie Boston roll-up to Abbvie
Parent Shell)
▪Ex 2: companies subsidiaries (e.g. Genentech rolls up to Roche Parent
Shell)
◦Pharma & Biotech: Pharmaceutical and biotechnology working on
therapeutics (drugs) to treat different diseases. Traditional Sanguine
customers
◦CDMO: Contract Development and Manufacturing Organizations. These
companies manufacture drugs on a contract basis for pharma and biotech

---

<!-- Page 44 -->
companies. Newer type of Sanguine customer
◦Diagnostic Companies: Life science companies that develop diagnostics and
medical devices used to diagnose diseases. Newer type of Sanguine
customer
◦Research Institutes: Life science research institutes that fall into one of these
categories: Hospitals, Non-profits, and academic research centers. Newer
Sanguine customers with typically lower budgets
◦Apheresis Clinic
◦CRO
◦Distributor
◦Business
◦Household
◦Individual
◦Payer
◦Patients

---

<!-- Page 45 -->
◦Non customers
◦Partners
• Purpose of Record Type(s) - purpose is to understand differences in buying habits
based on account type, target new clients, product mix based on account type
2. Child Objects
• Contact
• Opportunity
• Account plans
3. Most commonly used Fields (Use case)
• Account Name
• Parent Account Name (Links to associated Parent Record Type)
• Account Owner
• Account Priority
◦Strategic Active: LTV >$500K

---

<!-- Page 46 -->
◦Strategic Potential: LTV <$500K
◦Public Active: Account is publicly traded, historically has done business with
Sanguine
◦Public Potential: Account is publicly traded, historically has not done business
with Sanguine
◦Private Active: Account is privately owned;, historically has done business
with Sanguine
◦Private Potential: Account is privately owned;, historically has not done
business with Sanguine
• Account Record Type (noted above)
• Territory SDR
• Project Lead Name
• Phone
• Website
• Cell and Gene Therapy Company (checkbox, yes or no)

---

<!-- Page 47 -->
• Area of Interest (therapeutic area)
• LTV (historical sum of bookings)
• Shipping address
• Billing address
• CDA on file (checkbox, yes or no)
• MSA on file (checkbox, yes or no)
• MSA net payment terms
4. High level workflow within the object
• Account objects are created via account list pulls from sales/marketing. The goal
here is to add as many accounts as possible in our addressable market for
marketing and sales prospecting of new business. Product and Marketing makes
the decision prior to uploading new accounts in the CRM as to which account
record type they best correspond to.
• Once these accounts are pulled, they are assigned to an SDR and AE owner, who
are responsible for generating bookings from each individual account. Lead lists
are also pulled for each account object, and as opportunities are created, they are
associated with the correct Account in the CRM.

---

<!-- Page 48 -->
5. Which department(s) use the objects the most/ who creates them:
• Sales and marketing create new account record types via Account list pulls
(zoominfo or other platforms), or as inbound opportunities from accounts that are
not in the CRM appear. Sales Primarily utilizes the Account Record type as they
use this information for territory planning and prospecting both new and existing
clients. In addition, marketing uses account record types for email blasts, google
ads, and Account based marketing (ABM). Finally, the project management &
finance teams use these objects for invoicing client projects. This Object is
relevant to all of Sanguine to understand who our customers are and who our
potential customers are.

---

<!-- Page 49 -->
Opportunity
Opportunity
1. Purpose: Opportunity Object is utilized to track all opportunities entered into our CRM
for pipeline, bookings (closed-won) and lost opportunities (closed-lost). The
opportunity houses many child objects and workflow to provide as much information
about the account as possible. The Opportunity Object is a child object to the Account
Object.
a. Opportunity Record Type(s)
• Translational: All Standard Translational Studies
• Change Order: Used to capture Change Orders to an existing Opportunity
• Entered by PM/Feasibility after PC has been created
• Clinical Trial: Clinical Trial Opportunities
• Community Access Parent: Community Access Programs
• Community Access - Related: Used for related Community Access Services Request
Opportunities, related to a Parent Community Access Opportunity.
◦Entered by PM

---

<!-- Page 50 -->
• Inventory / Banked Samples: Inventory Orders (Mayo & San Diego)
• Lab Services & Storage: Processing and sample storage
• Leukopak - Healthy: Leukopak Studies for Healthy Leukopaks
• Healthy Leuko - Related (used for orders under blanket healthy leukopak record type)
• Leukopak - Diseased: Diseased Leukopaks
• LeukoLot: PBMC vials of Leukopaks used for screening purposes
• Leukopak - GMP
• Leukopak - Mobilized
• Onsite Record Types: Onsite Programs
1. Child Objects
a. Cohort - contains full study design detail by indication (more details in object)
b. Master Plan - associated with opportunity for projects that are closed won
c. Project Changes - any changes to the opportunity after it is closed won

---

<!-- Page 51 -->
d. Products - all the products on the opportunity for pricing purposes
e. Quotes - pricing and discount history on the quote, compiled of products
f. Approval History - tracking of the approval process in Stage 2
g. Notes & Attachments - where all relevant documentation is stored (attachments,
proposal drafts, sows)
h. NetSuite Financials - tracking of billing for closed won studies
i. I/E Criteria - details of inclusion / exclusion criteria
2. Most Common Fields
a. Stages: Stages represent the workflow of our Sales Process from Opportunity
Entry and detail gathering to Opportunity Closed - won or lost. Each Stage has
various fields and child objects (listed below) that need to be utilized to effectively
enter the data we need to review a deal
• Stage 1: Information Gathering
◦Cohort Object: Purpose: Cohort contains all of the information that pulls from the
Study Request Form involving all details pertinent to the study design. Feasibility
to update further with the following information:
▪Study-specific assumptions (including assumptions for pricing)

---

<!-- Page 52 -->
▪Inclusion/Exclusion criteria
▪Biospecimen collection details
▪In-home processing details
▪Kitting details
▪Lab processing and testing details
▪Shipping details
◦Managed by Account Executive and Feasibility
◦Fields to fill out in Stage 1:
▪Close Date - when this is expected to close
▪Estimated study budget
▪Estimated timeline
▪Vendor Features they are most interested in
▪AOI (Area of Interest)

---

<!-- Page 53 -->
▪Product of Interest
▪Pain points - relevant to deal
▪Study Requirements - entered via cohort
◦Convert lead to Contact for the opportunity
▪Contact Roles:
▪Economic Buyer (Procurement/Contracts)
▪Business User (Sample user)
▪Decision Maker
▪Influencer (Opp contact, has influence on the deal moving forward)
▪Contacts are clients who have engaged with us on an opportunity
▪Managed by Account Executive and Feasibility
• Stage 2: Feasibility Review
◦Approval workflow - ORT
◦Quote is created

---

<!-- Page 54 -->
◦Quote Purpose: Quote contains a compilation of all products associated with the
opportunity and study design for the opportunity price, including:
▪Product
▪Product Type
▪Study Setup
▪IRB Fees
▪Project Management and Support
▪Patient Access & Reservation
▪Data and Screening Services
▪Subject Reimbursement & Reservation
▪Kitting (Supplies and Services)
▪Home Visit Services
▪Shipping and Logistics
▪Pre-Analytical Lab Services

---

<!-- Page 55 -->
▪CLIA Analytical Services
▪Billing Cycle
▪Upfront
▪Per Visit
▪Manual
▪Monthly
▪Discount
▪Quantity
▪Total Price
• Quotes are created and managed by Feasibility
◦Account Executives can create quotes and adjust quotes with Feasibility approval
• Quote Stages and Workflows
◦Draft

---

<!-- Page 56 -->
◦Presented: AE has presented the proposal
◦In Review: Discount has been requested
▪Will go to AE leader, Feasibility leader and CEO to approve
◦Approved: Discount Approved
◦Rejected: Discount Rejected
◦Accepted: Create work order
◦Denied
◦Quality Check
◦Finalized: SOW Complete
• Proposal Generation
• Stage 3: Proposal Delivery - Feasibility has approved and created proposal
◦Fill in the following fields:
◦Adding proposal delivery date and check box so you know proposal has been
delivered and when

---

<!-- Page 57 -->
◦Obtain decision making process
◦Add/convert additional contacts
◦Update Budget
▪Price per sample→ update if client provides feedback
▪Estimated study budget→ update to marketing section if this has changed
from SRF
◦Add objections, concerns, or other key details
◦Estimated Study Completion date (when the client needs all of the samples by)
• Stage 4: Active Negotiation
◦Quote to “Presented”
◦Next Step
• Stage 5: Verbal Award
◦Scientific Approval
◦Internal Approval
• Stage 6: Closed Won

---

<!-- Page 58 -->
◦PO # field must be completed to move opp to Stage 6
◦PO Received Date (only if PO has been received)
◦Sync Final Quote
▪This syncs the quote products to the products on the opportunity, overrides
them and applies proper discounts
◦Final signed proposal, PO uploaded to Notes/Attachments
• Stage 6: Closed Lost
◦Reasons lost
▪Sales - Price / Budget
▪Sales - Competitor
▪Sales - Project canceled/on hold
▪Sales - Poor Fit / Qualification
▪Feasibility - Couldn’t accommodate client timeline
▪Feasibility - I/E too stringent

---

<!-- Page 59 -->
▪Feasibility - No access to population
▪Feasibility - Duplicate Opportunity (Doesn’t impact Win Rate)
• Notes & Attachments:
◦Study Request Form automatically attaches here
◦Proposal Attachments (all versions) - uploaded by the person who creates it
◦PO documentation
◦SOW documentation
◦Other relevant documentation to the opportunity (Protocols, Patient-facing
documentation)
1. High level workflow within the object
• Opportunities can be entered through the following ways:
◦Study Request Form (SRF) based on the record type
◦Entered Manually through Salesforce

---

<!-- Page 60 -->
◦Clone an older opportunity and edit accordingly
1. Used by:
a. Opportunities are used by Sales to capture all opportunity information and reflect
on past history of studies for better insight into future deals, Feasibility to review
and approve or reject opportunities based on feasibility status, Project
Management to review all details of the study and create master plans, Marketing
to track opportunities generated from their campaign efforts

---

<!-- Page 61 -->
Cohort
• Purpose: Cohort contains all of the information that pulls from the Study Request
Form involving all details pertinent to the study design. Feasibility to update further
with the following information:
◦Study-specific assumptions (including assumptions for pricing)
◦Inclusion/Exclusion criteria
◦Biospecimen collection details
◦In-home processing details
◦Kitting details
◦Lab processing and testing details
◦Shipping details
• Managed by Account Executive and Feasibility
• Fields to fill out in Stage 1:
◦Close Date - when this is expected to close
◦Estimated study budget

---

<!-- Page 62 -->
◦Estimated timeline
◦Vendor Features they are most interested in
◦AOI (Area of Interest)
◦Product of Interest
◦Pain points - relevant to deal
◦Study Requirements - entered via cohort

---

<!-- Page 63 -->
Quote
• Quote
• Purpose: Quote contains a compilation of all products associated with the opportunity
and study design for the opportunity price, including:
•
◦Product
◦Product Type
▪Study Setup
▪IRB Fees
▪Project Management and Support
▪Patient Access & Reservation
▪Data and Screening Services
▪Subject Reimbursement & Reservation
▪Kitting (Supplies and Services)
▪Home Visit Services

---

<!-- Page 64 -->
▪Shipping and Logistics
▪Pre-Analytical Lab Services
▪CLIA Analytical Services
◦Billing Cycle
▪Upfront
▪Per Visit
▪Manual
▪Monthly
◦Discount
◦Quantity
◦Total Price
• Quotes are created and managed by Feasibility
◦Account Executives can create quotes and adjust quotes with Feasibility approval

---

<!-- Page 65 -->
• Quote Stages and Workflows
◦Draft
◦Presented: AE has presented the proposal
◦In Review: Discount has been requested
▪Will go to AE leader, Feasibility leader and CEO to approve
◦Approved: Discount Approved
◦Rejected: Discount Rejected
◦Accepted: Create work order
◦Denied
◦Quality Check
◦Finalized: SOW Complete

---

<!-- Page 66 -->
Contact: Commercial
Contact
1. Purpose of the object: The purpose is to create records of contact information and
persona details for individuals who work at Sanguine customer accounts. Contacts are
converted from leads when an opportunity is created and associated with a lead
a. List of record type(s):
i. Scientist - a scientist working at a pharmaceutical or biotech company
ii. Academic Scientist - a scientist working at an academic institution such as a
college, university or research hospital. Correspond to Research Institute
account record type
iii. CGT Development - persona characterized by specific titles associated with
cell & gene therapy working at a company/within a department specializing in
cell & gene therapy
i. Ex titles:
i. Process Development
ii. Cell Therapy scientist
iv. Clinical Development - a member of the research team focused on clinical trial
development/work.

---

<!-- Page 67 -->
v. Diagnostic Scientist - a scientist who works at a diagnostic company.
Corresponds directly to account record type Diagnostic Company
vi. Manufacturing - individuals working at a CDMO. Corresponds directly to
account record type CDMO
vii. Other
viii. Procurement & Outsourcing - a persona of individuals who focus on the
procurement and outsourcing of biospecimens and data for a research team
b. Purpose of Record Type(s) - listed in Object Manager
i. To define the various personas for Contacts
2. List of child objects and the use case of it
a. Incidence Checks: Incidence Checks are a way to track requests we get from
leads or contacts and assess the feasibility of that request. It is saved on the lead /
contact so we can see their previous requests and go back to them if something in
our feasibility process changes to accommodate their request
b. Health profile
3. Most commonly used Fields (Use case)
a. Name

---

<!-- Page 68 -->
b. Title
c. Account Name
d. Contact owner (AE or SDR)
e. Contact Record Type
f. Email Address
g. Phone
h. Mailing Address
i. Contact Stage
j. Number of Total Opportunities
k. Number of Closed Won Opportunities
l. Lead Source
m. Area of Interest (therapeutic area)
n. Product of interest (Leukopak, translational, onsite, etc.)

---

<!-- Page 69 -->
o. SAL Date - Sales Accepted Lead Date - Date a meeting is scheduled with a lead
p. SQL Date - Sales Qualified Lead Date- Date an opportunity is created and a lead is
converted to a contact
q. Original SQL date - first time SQL conversion takes place
r. Last Activity Date by Sales - The last date in which a member of the sales team
(SDR or AE) have interacted with the lead
4. High level workflow within the object
a. Lead objects are converted to contacts upon opportunity creation. All contacts in
the CRM must have an associated opportunity in order for the conversion to work,
and Account Executives or less commonly, SDRs, are the individuals converting
leads from contacts
5. Which department(s) use the objects the most/ who creates them
a. Sales and marketing use contacts the most. For sales, contacts represent direct
customers who are leading the opportunity lifecycle from the client’s side. In
addition, contacts are usually repeat buyers, so sales goes back to past contacts
at various accounts for account mining and to prevent churn.
b. Project management also uses contacts as the main POC, typically, for an ongoing
study. Unless otherwise state by sales, the PM team is setting up a kickoff call and
acting as a day to day POC for the contact on a given closed won opportunity

---

<!-- Page 70 -->
Contacts: Patient
Contacts:
RecordTypeName: Patient
1. Purpose: The contact page (CP) for patient record types houses the main contact and
demographic information for a donor (Name, DOB, Address, Phone number, Email,
Ethnicity, Sex Assigned at Birth, Gender identity, Diagnosis). A contact page is the
main hub for a donor and is generated when they sign up with Sanguine online. Once
this occurs, the contact page and a single health profile are generated with a unique
participant identification number that is also linked on the contact page and health
profile. Additional health profiles can be created that are unique to each study master
plan. The created contact page will house the initial diagnosis and demographic
information that the donor signs up with and is where donors are contacted through.
2. Child Objects:
a. Contact History:
i. Shows the contact history information: Marks the date, time, user, and action
that was performed on the contact page.
b. Cases:
i. Houses the reported cases associated with the donor.
c. Health Profiles:
i. Section of the CP that contains links to all the health profiles for a donor.

---

<!-- Page 71 -->
d. Conditions:
i. Section of the CP that contains all the associated “Condition” pages for a
donor.
i. Condition Pages: Pages within a health profile that house more specific
information about a diagnosis that the donor reports. This may contain
age at diagnosis, severity, modified SLEDAI scores, comorbidities,
medications, method of diagnosis, etc.
e. Lab Results:
i. Contains any laboratory data that is returned after research testing (this does
not include medical record data). This is only uploaded on request for studies.
f. Collections:
i. Contains any specimen order (SO) associated with a donor.
i. Specimen Order: A unique number assigned to a health profile that
contains information for kitting. It is linked on the health profile and then
to the contact page.
g. Campaign History:
i. Contains information about any campaign (recruitment) that a donor signed up
through.
h. Google Docs, Notes, & Attachments:
i. Contains any signed medical record authorization form, and informed consent

---

<!-- Page 72 -->
form. (uploaded by the RC)
i. Activity History:
i. Contains information about contact attempts with the donor. (Call log, email
log).
j. Specimen Orders (Contact):
i. A second location to house the specimen order information.
k. EHR Patients:
i. Contains the medical record information that is collected through XCures- this
is a new platform to collect medical records digitally and is being fully
implemented for all studies in Q22024. This section will begin to accumulate
data that can be reported on.
3. Main Fields:
a. Requested Volume (mL): contains the “Total Volume (mL) from the past 6 weeks:”
This field contains the blood volume donation details. Every time a donor
participates, the requested blood volume from the health profile and the
appointment date are translated onto this section of the CP to give a running
history of donations and blood volumes. The “Total Volume (mL) from the past 6
weeks:” sums up the blood volume from all donations in the past 6 weeks and
research coordinators (RC)s monitor this field for protocol purposes. (Total blood
volume allowed within a 6-week span is specified in protocols).

---

<!-- Page 73 -->
b. Contact Information: Contact information contains the donors full legal name, their
primary diagnosis, diagnosis history (any diagnosis that was saved on the CP in
the past), blood volume limit (maximum amount of blood they can donate within a
6-week span), patient identification number (Patient_ID_New), phone numbers,
email address, mailing address, date of birth (DOB), ethnicity, sex assigned at
birth, gender identity.
i. This section is commonly used during screens by the RC. IT also contains the
patient's status which identifies if they are “Active”- can be contacted for a
study or may be unreachable or no longer interested in being contacted. If a
donor status is anything but “Active”, they will typically not be contacted for a
research study.
c. System Information: Shows you the created by date, time, and employee name,
and the last modified by date, time, and employee name.
4. Workflow:
a. When a donor signs up with Sanguine, a contact page is created that collects the
information the research coordinator needs to reach out to them.
b. When an RC is creating reports to pull in potentially eligible donors, the RC will
refer to the CP to review all donor information before making an outreach.
c. The RC calls the donor from the CP and reviews that information with them as the
first part of the screen.
Usage: Patient Operations uses the contact page to review donor information, confirm
identity, create reports for eligibility by pulling donor age, address, status, diagnosis, sex

---

<!-- Page 74 -->
assigned at birth, and/or ethnicity. Blood volume is tracked on the contact page and it
houses all the different health profiles that are linked to a master plan. This is an essential
hub for the RCs, because an RC can view if a donor is being enrolled in another study and
therefore needs to delay contact for their own study.
What information does the contact page for patient record types house?
The contact page for patient record types houses the main contact and demographic
information for a donor (Name, DOB, Address, Phone number, Email, Ethnicity, Sex Assigned
at Birth, Gender identity, Diagnosis).
Keypoints
• The main hub for donor information
• Linked to unique participant identification number
• Contains contact history, cases, health profiles, conditions
• Includes lab results, collections, campaign history, and Google Docs
• Holds details of specimen orders and EHR patients section
• Displays medical record information collected through XCures
• Tracks blood volume and patient's status information
• Used for creating reports for eligibility and reviewing donor information

---

<!-- Page 75 -->
Master Plan
1. Purpose: The Master Plan serves to operationalize a cohort/study, by housing specific
details, such as I/E criteria, scheduling restrictions, and collection requirements. If
changes are made during the course of the study, these changes are made on the
Master Plan, such that it reflects the current requirements. The Master Plan also
aggregates real-time records of associated screening and collections for the study/
cohort.
a. Record types: The Master Plan object does not utilize different record types at the
moment
2. Child objects:
1. Study specific DNQ Questions: These are the questions that disqualify patients from
the study (DNQ = Does Not Qualify)
2. I/E Criteria: I/E criteria records automatically pull from the linked cohort and reflect the
I/E requirements for the Master Plan
3. Study-Specific Questions: SSQ records are questions formulated to reflect the I/E
criteria, and are utilized by the RC team to screen subjects via the associated health
profiles
4. Health Profiles: Health profiles are linked to the Master Plan to reflect that the RC team

---

<!-- Page 76 -->
is attempting to screen a particular subject for this cohort/study.
5. Collections: Collection records reflect specific supplies/tubes that are being requested
for the study/cohort, the processing requirements (if any), and the shipping
temperature and speed. These records also become associated with specific site
codes, which reflect the exact destination of each collection, as well as collection
products (B2C products), that indicate the specific tube/supply (e.g. 10mL K2EDTA).
6. Cohorts: Cohorts are linked to a Master Plan to indicate which cohort from the
opportunity is being represented by the Master Plan. The linking of a Cohort also
allows for the auto-pull of I/E records to the Master Plan.
7. Project Changes: Project changes associated with Master Plans track timeline change
requests that go through an approval process and will automatically update the
working ops deadline. This allows us to create an audit trail of timeline changes, as
well as pull and evaluate any metrics associated with timeline changes.
8. Purchase Orders: The purchase orders (specimen orders) associated with a Master
Plan reflect collection visits that were previously, or are currently, scheduled on study/
cohort.
9. Cases: Cases associated with a Master Plan are cases that are related to either
specific specimen orders on that Master Plan or that Master Plan itself.
3. Most commonly used fields:
1. Status

---

<!-- Page 77 -->
a. In Study Start-Up
b. In process - screening only
c. In process
d. Collection complete
e. Complete
f. Incomplete
g. On Hold
2. Working ops deadline for this MP (Based on Proposal Timeline)
3. Collection Details fields: collection requirements, estimated visit duration
4. Scheduling Notes fields: scheduling restrictions, maximum number of samples per day,
maximum number of samples per week, Blackout dates
4. High level workflow:
• Opportunity hits stage 6

---

<!-- Page 78 -->
• PM assigned to the opportunity reviews the cohort(s) and opportunity details, and
creates the Master Plan(s) to operationalize the project (typically 1 cohort = 1 Master
Plan)
• PM holds an internal training on the Master Plan to train the operations team on the
project requirements
5. Departments that use the object the most:
1. The PM team creates and manages the Master Plan
2. Other departments that utilize the Master Plan
a. Patient operations - RCs review the Master Plan to understand study details,
screening, consenting, and medical record requirements, and to link health profiles
to Master Plans to assign subjects to the cohort/project
b. Field operations - OCs review the Master Plan to understand the scheduling and
collection requirements and restrictions. OSs review the Master Plan to
understand the phlebotomy and collection requirements.
c. Medical records - MRCs review the Master Plan to understand the medical record
requirements
d. Patient recruitment - the patient recruitment team reviews the Master Plan to
understand I/E requirements for recruitment purposes

---

<!-- Page 79 -->
e. Supply chain - the supply chain team uses the Master Plan to understand the
collection, shipping, and kitting requirements
f. Account Executives - to check the status of study progress
What details does the Master Plan house and why?
The Master Plan serves to operationalize a cohort/study, by housing specific details, such as
I/E criteria, scheduling restrictions, and collection requirements. If changes are made during
the course of the study, these changes are made on the Master Plan, such that it reflects the
current requirements. The Master Plan also aggregates real-time records of associated
screening and collections for the study/cohort.
Keypoints
• Master Plan operationalizes study details
• Aggregates real-time screening and collections records
• Study-specific DNQ questions disqualify patients
• I/E criteria reflect requirements for the Master Plan
• Health profiles indicate screening for a particular subject
• Collections reflect specific supplies and tubes for study
• Cohorts are linked to indicate represented cohort
• Purchase orders reflect scheduled collection visits
• Most commonly used fields: status, collection details, scheduling notes

---

<!-- Page 80 -->
• High level workflow: opportunity stage 6, PM creates Master Plan
• Departments using the object: PM team, patient operations, field operations, medical
records, patient recruitment, supply chain, account executives

---

<!-- Page 81 -->
Health Profile (HP)
1. Purpose: The health profile houses all health related donor data (not including medical
records) and is where information obtained during the research coordinator (RC) phone
screen is recorded. The data recorded in the health profile includes any conditions that
a participant has been diagnosed with or any medications that they are currently
taking. All study specific answers (client requested) can also be found within the health
profile object. A participant can have a number of health profiles attached to their
contact and each is unique to a master plan.
2. Record types- Record types differ in the fields that they contain so they can be more
specific to their use case. Sangre Master Copy and Apheresis record types contain a
majority of the same fields but have some differences based on what is necessary for
apheresis studies vs. translational, onsite, clinical trial studies.
a. Sangre Master Copy- This record type is used for translational, onsite, and clinical
trials. It contains more general fields to be applicable to all these study types.
b. Apheresis- This record type is used for apheresis master plans. It contains fields
applicable to apheresis donations.
3. Main Fields:
a. Health Profile Details: This area contains the most amount of information about the
status of the donor in the donation process.
i. It contains all the contact page demographic information (ethnicity, age, sex,

---

<!-- Page 82 -->
address information, name, participant identification number (Actual Patient
ID), diagnosis).
ii. The “status” gives the status of the donor in the specific master plan
donations process.
i. The “secondary status” gives additional information for the RC on the
status of the donor in the donation process.
iii. The “Master Plan” links the master plan (study) that the health profile is being
used to screen for. This link is the most important aspect of the health profile
because it is how the project management team tracks the progress of the
study.
iv. Contains information about the RC who completed the screen, when the
screen was completed, and a “CRC Notes” section which is used by the RC
to note any contact attempts or general updates.
v. The “Requested Volume (mL)” contains the blood volume that will be drawn
for the study and carries over onto the CP (described in CP section).
vi. Additional boxes are located in this section that are linked to automations.
These are used to assist in preventing deviations.
b. Document Retrieval: This section outlines the required informed consent form
version, and medical record status for the research study

---

<!-- Page 83 -->
i. An RC will update this section to notate to the medical record coordinators
that a medical record request is required for this donor. The date of signature
of the medical record authorization form is entered here, and the RC will note
when the diagnosis for the study is confirmed in the medical record.
ii. An RC will update this section to note the informed consent version and date
of signature that is required for the study and has been signed by the donor.
c. Medical Record Retrieval: This section of the HP is owned by the medical record
coordinators (MRCs). It is an area that contains status updates about the medical
record request process.
i. The MRCs will update this section to indicate the status of the medical record
request. It also contains a status for the medical record summary and
redacted medical record summary request. These are created from the
original donor medical records to be provided to clients.
d. Standard Questions: This section houses the protocol-related inclusion/exclusion
questions (SAN-BB-02) and a section for the donors weight, height, BMI.
e. General Health: This section houses the majority of the donor's health information.
It is split up into different areas of health conditions (eg. allergies, autoimmune,
hematologic)
i. This area is used during screening to select each health condition that a donor
reports during screening. It is updated if additional health conditions are
discovered during the medical record review.

---

<!-- Page 84 -->
ii. This area is vital to reporting on donor eligibility as these fields are used in
reports to see how many, and which donors are associated with which health
conditions.
f. Condition Specific Information: This is a section of the HP that was created for a
clinical trial. It may be updated in the future to reflect more specific condition
information for high priority studies
g. Social Habits: This section houses information about a donor's tobacco, caffeine,
alcohol, and recreational drug use.
h. Physician Info: This section houses the primary and secondary physician
information of the donor.
i. Apheresis: Includes the apheresis site name and leukopak delivery speed.
j. System Information: Contains the donor name (patient name), user who created
the HP, last modified date, and SSDNQ Check (this is a check-box to override an
automation)
4. Child Objects:
a. Study-Specific Answers: This section houses the client-specific questions that are
associated with each master plan. They are created when a master plan is
connected to the HP. The RC will complete these questions during screening.

---

<!-- Page 85 -->
b. Study Specific DNQ Answers: This section houses the disqualification reason for a
study. It is set up in a way that requires the RC to select a general reason and then
enter the specific reason in an open text field (can be provided to the client).
c. Conditions: This field is created for the MP condition that a donor is diagnosed
with.
i. This field creates different entries depending on the condition selected and
gives more information about the diagnosis (age at diagnosis, severity,
modified SLEDAI scores, comorbidities, medications, method of diagnosis,
etc.)
d. Lab Results: Contains any laboratory data that is returned after research testing
(this does not include medical record data). This is only uploaded on request for
studies.
e. Specimen Orders (Health Profile): This section is created by the operations
coordinators when a donor is scheduled for a study.
i. A unique number assigned to a health profile that contains information for
kitting. It is linked on the health profile and then to the contact page.
f. Google Docs, Notes, & Attachments:
i. Contains any signed medical record authorization form, and informed consent
form specific to the master plan associated with the HP (uploaded by the RC).
g. Activity History: Section of the HP where emails or calls can be logged (these are
logged on the CP regardless of this section).

---

<!-- Page 86 -->
h. Health Profile History: Contains information on the date, time, user, and action that
was taken (any changes to the HP are logged here).
5. Workflow:
a. RC finds a potentially eligible donor for a study: the RC will create (by cloning the
most recent HP) a new HP. All the existing data from the most recent screen will
be carried over to the new HP. The new HP will be linked to the master plan and
any client-specific questions will be carried onto it.
b. The RC will use the HP to prompt them for what standard questions they need to
ask the donor during the screen, and what client-specific questions are required.
c. The HP is updated while the RC is on the phone and that information is reviewed
to determine eligibility.
d. The HP statuses determine where the donor falls within the eligibility process.
i. The HP is used as a main hub for the medical record coordinators to retrieve
information needed to request medical records
ii. The HP is used as the main hub for specimen orders (SO)s used by the
operation coordinators.
6. Usage: Health Profiles are primarily used by the Patient Operations team. Research
coordinators screen patients and fill in the patient data accordingly. It is used by the
medical record coordinators to retrieve information for requesting medical records. It is
used by the operation coordinators to schedule participants for studies and to create

---

<!-- Page 87 -->
the SOs that are used for studies.
What is the purpose of the health profile?
The health profile houses all health related donor data (not including medical records) and is
where information obtained during the research coordinator (RC) phone screen is recorded.
Keypoints
• Health profile records donor health data
• Record types differ in fields based on use case
• Health Profile Details contains demographic information
• Document Retrieval for informed consent and medical records
• General Health section houses donor's health information
• Apheresis section includes apheresis site name and delivery speed
• Health Profiles are used by the Patient Operations team
• Used to schedule participants for studies and create SOs

---

<!-- Page 88 -->
Case
Case
1. Purpose: The case object serves as a record to house all details associated with an
issue that arises at any point from the sales process to study completion. An issue for
the purposes of case reporting is defined as any time something does not go as
expected or intended, and can range from very minor to very severe. Data from case
logging can be reviewed to understand overall trends in the types and severity of
issues we see, as well as the root causes of issues. Cases can be linked to the parent
objects (opportunity, master plan, specimen order)
1. Record types: The only record type we are currently using as of March 2024 is
Sanguine Case Report
1. Child objects:
• Open activities: task records are assigned to cases, as needed, to indicate that
relevant stakeholder representatives are required to review and sign off on cases
1. Most commonly used fields:
All fields in the case object are used, but important fields to manage in the case object
include:

---

<!-- Page 89 -->
1. Date issue addressed
2. Status
a. New- Indicates a case has been created but potentially not yet reviewed
b. Resolved - indicate that a solution has been identified
c. Pending Stakeholder Review - trigger assignment of Salesforce ‘tasks’ to the
parties involved in the issue and/or relevant stakeholders. Indicates that review,
input, additional information, and/or approval may be required prior to submitting
to QA for review, and potentially to come to a resolution
d. Pending QA Review - all assigned parties have reviewed, provided input or
information (as needed), and approved the case
e. Closed - indicate that the case has been reviewed by the QA team, and that there
are no additional case documentation action items outstanding.
f. On hold - additional information or documentation is required prior to marking the
case as closed
3. Description
4. Issue being reported
5. Sub-issue list

---

<!-- Page 90 -->
6. When issue was caught
7. End result
8. Lev 1 - Responsible Party
9. Lev 2 - Responsible Party
10. Lev 3 - Responsible Party
11. Risk Rating(QA only)
12. QA Input
4. High level workflow:
• An issue is flagged by any member of the sales or operations team, typically in Slack or
Salesforce
• A PM team member associated with the relevant project or account will log the case
within Salesforce
• The PM team member will push the case out to stakeholders for review and also mark
the case as ‘resolution in progress’ when appropriate, to log the date the issue was
addressed

---

<!-- Page 91 -->
• When all stakeholders have reviewed and signed off on the case, QA will be
responsible for assigning a risk rating and closing the case out
5. Departments that use the object the most:
Case records are logged by the PM team, but reviewed by stakeholder representatives and
QA

---

<!-- Page 92 -->
Specimen Order
Specimen Order
1. Purpose: The purpose of the Specimen order is for us to track visit completion in one
object. The Specimen order houses the Study information, Donor information,
Phlebotomist assigned, Kit information, and status of completion. We are able to easily
track what number of visits have been completed or incompleted in order to complete
a study. Specimen Order is a child object on the Master Plan
2. Child Objects
a. Purchase order lines- the purchase order lines just pull the collection line items
from the Master plan
b. Smartsheet report items- used as a connector for Smartsheets
3. Most commonly used fields:
• All fields in the Specimen order are used, but important fields to manage in the
Specimen order include:
• Specimen Order Name
• Master Plan
• Health Profile

---

<!-- Page 93 -->
• Status
• Draft- This status is used when the Specimen order has been created and the
job has been dispatched
• Ordered-This status automatically populates once the job has been accepted
by the phlebotomist
• Pending/in transit- This status is not currently being used by my department
• Processing- This status is not currently being used by my department
• Complete- This status is automatically updated when the job is completed in
Skedulo.
• Discard- This status is used when a specimen order is duplicated and is not
being used
• Incomplete- This status is used when any error has occurred and the
specimen is not viable for example shipping delay, Sample error, blood
volumes not met etc
• Rescheduling- This status is used when we have to reschedule an
appointment and we will be using the same specimen order and kit.
• Originated from split- This status is used when the clients blood volume has
not been met and we are splitting the original specimen order and creating a

---

<!-- Page 94 -->
new one to ship the specimens to the San Diego lab for inventory banking.
• Sample Destination
• CT Payer Card #
• Lab A,B,C Fedex Tracking
• Speciality Courier Tracking if applicable
• Patient Date of Birth
• Opportunity Record Type
• This pulls the study type from the Master plan ie Translational, Clinical trial,
Onsite, Community access etc…
• Specimen order completed date
• Reason for status
• Phlebotomist Compensation
• Order Time

---

<!-- Page 95 -->
• Ordered By
• Sanguine Point of Contact (Operations Specialist)
• Patient Advocate (Phlebotomist assigned)
• Primary Payment Structure
• Metropolitan Region
• Mobile Staff Availability Notes
• HP Date & Time put in RTBS
• Requested Volume
• Kit Status
• Kit Notes
• Kit Made
• Ship to Phleb Tracking
• Ship to Patient Tracking

---

<!-- Page 96 -->
• Saturday delivery label required
• Materials Printed date/by
• Kit assembled date/by
• Kit QC date/by
• Sangre Draw Information
• Study ID
• Status
• Appointment Date/Time
• Patient ID
• Patient Age
• Patient Sex
• Patient First and Last name
• Diagnosis from HP

---

<!-- Page 97 -->
• Diagnosis from MP
• Donor Ethnicity
• Patient Demographics
• Patient email
• Assigned Patient Advocate
• Patient Advocate phone number
• Patient Advocate email
• Post Visit Information
• CT Payer Card
• Amount Paid
• Date of payment
4. High level workflow:
• Specimen orders are created once a donor is placed into a Ready to be scheduled

---

<!-- Page 98 -->
status
• The Operations Coordinator will create a Specimen order and a Job in Salesforce to
dispatch to the patient advocate (phlebotomist)
• The Supply chain team will see the specimen order and will then build the kit based on
the Master Plan attached to the Specimen order and then ship the kit directly to the
phlebotomist and potentially the donor if a donor kit is also needed for collections.
• Once the phlebotomist receives the kit the Operations Specialist will review the visit
guide with the phlebotomist to ensure that they have all required supplies and fully
comprehend the procedures required.
• Day of the appointment the phlebotomist will utilize the Skedulo and the Specimen
order to obtain donor information to complete ID verification and to complete the
required requisition forms.
• Once the visit is completed and shipped the phlebotomist will complete the job in
Skedulo and the Status of the specimen order will automatically update to a completed
status.
• Within 24 hours of the completed visit the donor will receive their pay via the CT Payer
number.
5. Departments that use the Specimen Order the most:

---

<!-- Page 99 -->
• Specimen orders are used the most by the Field Operations team which includes
Scheduling Operations, Supply Chain, and Visit/Phleb Operations. The Project
Management team also uses them to track study completion.

---

<!-- Page 100 -->
Conclusion
In this lesson, we delved into the essential Salesforce objects: understanding their specific
roles and functionalities. These objects play vital roles in managing operations from leads
to opportunities to study execution and issue tracking across different departments. By
exploring their details, we gained valuable insight into their diverse applications and how
they contribute to streamlined operations within an organization.