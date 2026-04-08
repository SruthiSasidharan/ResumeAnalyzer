Assignment 2: First Review PPT
Content

0.1 Introduction
This project develops an **AI Career Guidance and Skill Gap Analyzer**, a web-based application that helps students and professionals understand how well their resume matches industry expectations. The system automates resume analysis, predicts suitable career roles, identifies missing skills for those roles, and recommends learning resources and job opportunities through a single dashboard. By reducing manual screening and scattered searching, the platform supports clearer career decisions and structured upskilling.

0.1.1 Problem Statement
[Define the real-world problem, its importance, and how your project addresses it.]
Students and working professionals often struggle to choose an appropriate career path and to identify the specific skills required for target job roles. Manual resume review and role-skill comparison is time-consuming, inconsistent, and depends heavily on subjective judgment. As a result, users may spend effort learning the wrong skills or applying for roles they are not yet prepared for.

This project addresses the problem by automatically extracting key information from resumes (skills, education, and experience), mapping the profile to industry-relevant job roles, detecting skill gaps against role requirements, and presenting targeted learning and job recommendations. The output is summarized through skill score and career readiness indicators to help users take corrective actions.

0.1.2 Abstract
The project entitled “Web-Based AI Career Guidance and Skill Gap Analyzer” is an online career guidance system whose primary objective is to provide intelligent, resume-driven career planning. The portal enables users to upload resumes in PDF or DOC/DOCX format, automatically extracts skills, education, and experience using NLP, predicts suitable career roles, and identifies missing skills by comparing the profile with role requirements. Based on the identified gaps, the system recommends curated learning resources and provides role-aligned job suggestions, with results displayed on a dashboard as a skill score and career readiness level. The application is implemented using Python with the Django framework, HTML and Bootstrap for the interface, and a database (SQLite with optional MySQL) for storing user analysis records and datasets.

0.2 Software Project Plan
[Provide project plan with timeline. You may include a Gantt chart.]
• Week 1–2: Requirement Gathering
• Week 3–4: System Analysis & Design
• Week 5–7: Coding
• Week 8: Testing
• Week 9–10: Implementation & Report

0.3 Software Requirements Specification (SRS)
0.3.1 Functional Requirements
• Add, update, delete records (Skills, Career Roles, Learning Resources, Job Listings) via admin
• Search functionality (filter job listings by role keyword; search skills/roles in admin)
• Report generation (resume analysis result page showing extracted skills, predicted roles, gaps, learning links, and job recommendations)
• Upload resume (PDF/DOC/DOCX) and store analysis results in database

0.3.2 Non-Functional Requirements
• Performance – fast response for dashboard views and job listing pages; reasonable analysis time for resume parsing
• Security – safe file upload handling, secret-key/API-key protection, and basic data protection
• Usability – user friendly interface with clear steps (upload → analyze → results → jobs)
• Scalability – future growth in roles, skills, learning resources, and support for external job APIs

3
0.4 System Analysis
Include Data Flow Diagram (DFD) or Use Case Diagram here.
dfd-placeholder.png

