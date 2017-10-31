# Champion System Project Planning Document

## Proposed Workflow Organized by Priority

- Preliminary Steps (must be completed before starting dev)
  - Stories translated to proposed features
  - Effort and experience level estimates for features
  - Proposed timeline for MVP prototype
  - UI mock-ups/proposals
  - Proposed data schemas for any databases (or simply proposed data storage solutions)
  - Proposed categorization/matching strategies
- MVP: Working prototype with dummy resources and functionality to demo for NILC that meets some or all of the following in order of priority:
  - Publically available landing page
  - Users can identify who they are (immigrant, congressional rep staff, NILC staff, volunteer) 
  - Users are re-directed to appropriate landing page based on identification.
  - Proposed/dummy resources are displayed to correct users.
  - Users can interact with dummy resources and submit requests/volunteer offers.
  - Users receive a notification after submitting request
  - NILC staff user can view and interact with submitted requests/cases.
  - Volunteer lawyer can register with proposed intake form
  - Proposed categorization/matching strategies for cases w/ resources, NILC lawyers, and volunteer lawyers implemented.
  - Volunteer lawyers can receive notifications for matches
  - Volunteer lawyers can view and explore possible cases to volunteer for

## End Users

- Primary Users
  - Immigrants in Need of Legal Assistance
  - Congressional Rep Staff Member
  - NILC Staff Members
  - Volunteer Lawyers

## Stories

- Given an immigrant in need of legal assistance, when they seek assistance then they can visit a publically available interface for the Champion System.
- Given a congressional rep staff member, when they approach the NILC seeking assistance on behalf of a constituent, then they can visit a publically available interface for the Champion System.
- Given a lawyer interested in providing pro-bono services to the NILC, when they approach the NILC to offer services, then they can visit a publically available interface for the Champion System.
- Given a visitor to the publically available interface for the Champion System, when they visit the interface, then they are directed to the appropriate resources.
- Given a congressional staff member has visited the Champion System, when they select their category, then they must verify they are a congressional staff member.
- Given a congressional staff member has verified their status, when they access the Champion System, then they are provided with an intake form and basic resources on intake procedure.
- Given an immigrant in need of legal assitance and a publically available interface for the Champion System, when they visit the interface then they are provided with a set of instructions for requesting assistance.
- Given the person requesting assistance has read the instructions for requesting assistance, when they initiate the request process, then they are provided with a set of intake questions.
- Given the person requesting assistance has completed the intake questions, when they submit their request, they are provided with acknowledgment of the receipt of their intake information, a unique identifier for their case, and contact information for follow up.
- Given the submission of a request for assistance, when the case is received then a unique identifier for the case is generated and associated with the case.
- Given a successful receipt of a request for assistance, when it is received then it is categorized by type of request before storing.
- Given a successful reciept of a request for assistance, when it is received then it is summarized before storing.
- Given the submission of a request for assistance, when the case is received then it is stored for future reference.
- Given a new request has a unique identifier, category, and summary, when it is received by the Champion System then it is identified as an unprocessed task.
- Given a group of unprocessed tasks, when the task is analyzed then the appropriate response can be generated (e.g. resources sent to requester, NILC staff member notified, etc.)
- Given an NILC staff member, when they visit the Champion System, then they can verify their identify to access the data in the system.
- Give an NILC staff member has verified their identity, when they are logged in then they can view submitted cases, volunteer offers, and status of each.
