from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from projects.models import Project, TechStack
from .models import Job
from .serializers import JobSerializer


class JobProcessingAPIView(APIView):

    def post(self, request):
        argon = ''' We are ArgonTeq (part of Ozi Group) and we create first-rate and superior websites and applications. To date, we have delivered 350+ websites and mobile apps for our global clients which have given us an immense feeling of happiness, and boast of developing some of the big brand websites and applications with millions of views.
In this proposal, you'll see information about ArgonTeq, our services, project description, development process, pricing, terms, and conditions.
We look forward to talking with you.
Sincerely, ArgonTeq 
For over 7 years, we've been developing new technology and helping Enterprises, Governments, NGOs and Startups, globally from all sizes to grow and achieve their goals in the form of users, subscription and revenue. Our mission is to provide companies with cutting-edge services that will enable you to achieve your goals via digital means.
We strongly believe that our proficient technical practices fetch promising results for you. No matter where you start from, we ensure that where you reach must be noticeable and appreciable.
At ArgonTeq, we believe in a thorough approach that provides our clients with as much engagement as they request. While our entire team will be developing your web/app, we will assign a project lead who will be your main point of contact.
We normally need 2-20 weeks to finish the Application completely, depending upon the complexity of the requirement. We send feedback to our client for every successful step we make. We assure our clients that we kept them updated with the project.
1.	Zoom Meeting and formally offering the proposal.
2.	Acknowledgment and signing of contracts. 
3.	Proceed with building the app UI screens.
4.	Create the front-end technology of the app. 
5.	Improve visual UI design. 
6.	Programming the backend technology of the app. 
7.	Perform UX (User Experience) QA Testing. 
8.	Perform further testing with the client. 9. Go Live for public release


'''
        policies = '''
        Warranty of Services
ArgonTeq assures that the services offered will be in excellent and first-rate quality. For changes in the way of how we render our service, please notify the company. If you are not satisfied with our work, kindly let us know so that we can further assist you.
Payment
Payment would be divided into 4 parts on a 25%-25%-25%-25% basis i.e. 25%% advance with this proposal, 25% after the first milestone is completed, 25% after the second milestone is completed, 25% after 3rd Milestone when UAT Start.
IPR
ArgonTeq acknowledges that all intellectual property rights in the work product, including but not limited to software, documentation, and other materials created by the agency, will be owned by the client. ArgonTeq hereby assigns and transfers all intellectual property rights in the work product to the client.
Amendments
This Proposal can only be changed or modified by the company ArgonTeq. A new proposal will be made if the clients wish to change the content of the document.
        '''
        api_key = ""
        if api_key is not None:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
        # Deserialize the incoming Job data
        job_serializer = JobSerializer(data=request.data)

        if job_serializer.is_valid():
            # Save the Job object
            job = job_serializer.save()

            # Extract tech stack from job description (assuming tech stack is provided)

            prompt = f"your task is that you will be given a client technical requiremnsts and you have to get the tech stacks like python react vue dotnet django flask fastapi  etc seprated by commas {job.description}"
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": prompt}],
                max_tokens=10,
            )
            tech_stacks = response.choices[0].message.content
            print(tech_stacks.split(','))
            tech_stack_names = request.data.get('tech_stack', tech_stacks)
            tech_stack_objs = TechStack.objects.filter(name__in=tech_stack_names)

            # Find Projects with the same tech stack
            # matching_projects = Project.objects.filter(tech_stack__in=tech_stack_objs).distinct()
            matching_projects = Project.objects.all()
            projects_description = " "
            for project in matching_projects:
                projects_description =  projects_description + f"project title: {project.name} \n description : " + project.description + '\n\n '

            # prompt = f"Your task is to write a cover-letter we are a agency named Argon here is some information about company {argon} for the given job description {job.description} and the client name is {job.client} mention that i have worked with all the things mentioned important point is to note make sure to add objective, scope, budget, deadline, and milestone here are some relevant projects which you can add {projects_description} in detail the proposal should be at least 3-4 pages long explain the milestones time or those milestones and mention some projects similar to this  add the terms for argon as decscibed above   format the response in such way which i can directly use in rich text editor for formatiing you can provide me a html response  every thing should be well formated like headings bullet points list each and ervy thing in a html format which can be used in rich text editor dont include [Doctype,styling,<html tag> <body> ] just the html code h tags for headings line breaks listing numbering  make the html formating beautiful and well organized so that it should look like a professional proposal "
#             prompt = f"""
# Generate a atleat 7000-word detailed proposal this is mandorty to generate 7000 words  for a {job.description} project for client {job.client}. The proposal should be formatted in HTML for use in a rich text editor and include the following sections:
#
# Introduction: Provide an overview of the project, its goals, and how it aligns with the client’s needs.
#
# Company Overview: {argon}
#
# Policies: List and explain our company’s policies relevant to this project, such as:
#
# Confidentiality and data security policies
# Code quality and testing policies
# Delivery and communication policies
# Client feedback and iteration policies
# Milestones and Deliverables: Break down the key project milestones, deliverables for each phase, and the timeline for completion. Be specific in mentioning tasks for each phase, e.g.:
# {policies}
# Phase 1: Planning & Design: Gather requirements, create wireframes and design mockups (1-2 weeks)
# Phase 2: Development: Implement core features and functionality (4-6 weeks)
# Phase 3: Testing & Iteration: Conduct QA testing, bug fixes, and refinements (2-3 weeks)
# Phase 4: Deployment: Launch the project, provide documentation and training (1 week)
#
# Project name
# Project description
# Project outcomes
# Budget: Provide a detailed budget for the project, itemizing the cost of each phase and explaining the rationale behind the pricing. Also, mention any potential additional costs, such as post-launch support or extra features.
#
# Timeline: Provide a detailed project timeline, including estimated start and end dates for each milestone and any dependencies or contingencies.
#
# Conclusion: Summarize the proposal, reiterating why we are the best fit for the project and expressing enthusiasm to move forward.
#
# Output the entire content in HTML format, using proper HTML tags such as <h1>, <h2>, <p>, <ul>, <li>, etc., to structure the document for use in a rich text editor
# """
#             print(prompt)
#
#             response = client.chat.completions.create(
#                 model="gpt-4",
#                 messages=[{"role": "system", "content": prompt}],
#             )
#             proposal_response = response.choices[0].message.content
#             print(proposal_response)
            return Response({
                'data': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mobile Application Proposal for Ateeq</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            margin: 20px;
        }
        h1, h2 {
            color: #0056b3;
        }
        p {
            margin: 10px 0;
        }
        ul {
            margin-left: 20px;
            list-style-type: disc;
        }
    </style>
</head>
<body>
    <h1>Proposal for Mobile Application Development</h1>
    <p><strong>Client:</strong> Ateeq</p>
    <p><strong>Prepared By:</strong> Argon Teq</p>

    <h2>Overview of Argon Teq</h2>
    <p>Argon Teq is a leading software development company specializing in cutting-edge mobile and web solutions. With a dedicated team of highly skilled developers, we have successfully delivered numerous projects in diverse fields, including artificial intelligence (AI), mobile apps, SaaS, and more. Our experience spans a wide array of industries, from entertainment to healthcare, making us the ideal partner for developing a mobile music application tailored to your needs.</p>

    <h2>Scope of the Project</h2>
    <p>We propose the development of a mobile music application that offers seamless user experience, rich functionality, and a visually appealing interface. The application will cater to a broad range of music lovers by incorporating features that will enhance the way users discover, listen to, and share music. Key functionalities of the mobile app include:</p>
    <ul>
        <li>User authentication (sign-up, login, password recovery).</li>
        <li>Music streaming with high-quality audio support.</li>
        <li>Personalized playlists and recommendations based on user preferences and listening history (AI-driven).</li>
        <li>Offline music playback (download functionality).</li>
        <li>Social sharing features (share songs, albums, and playlists via social media platforms).</li>
        <li>Music search and discovery with filters such as genre, artist, and mood.</li>
        <li>In-app purchase options for premium content or subscriptions.</li>
        <li>Push notifications for updates, new music releases, and app features.</li>
        <li>User-friendly interface with intuitive navigation and engaging design.</li>
    </ul>

    <h2>Project Timeline</h2>
    <p>The project is divided into phases to ensure smooth development, testing, and deployment:</p>
    <ul>
        <li><strong>Phase 1: Requirements Gathering & Analysis (1-2 weeks)</strong></li>
        <p>During this phase, we will work closely with you to understand your specific needs and preferences. We will gather all technical and functional requirements to ensure the development is aligned with your vision.</p>
        
        <li><strong>Phase 2: Design (2-3 weeks)</strong></li>
        <p>This phase will include designing the user interface (UI) and user experience (UX) of the application. We will present multiple design options, taking your feedback into account, and finalize the look and feel of the app.</p>

        <li><strong>Phase 3: Development (6-8 weeks)</strong></li>
        <p>In this phase, our developers will implement the core functionality of the mobile music app. Key features such as music streaming, playlist management, offline playback, and social sharing will be integrated.</p>

        <li><strong>Phase 4: Testing & QA (2-3 weeks)</strong></li>
        <p>We will conduct thorough testing to ensure the app is free of bugs and performs well across different devices and platforms. This includes functionality testing, usability testing, and security checks.</p>

        <li><strong>Phase 5: Deployment & Launch (1 week)</strong></li>
        <p>After successful testing, the app will be deployed to the Apple App Store and Google Play Store. We will assist in ensuring all requirements for a successful launch are met.</p>

        <li><strong>Phase 6: Post-Launch Support & Maintenance (Ongoing)</strong></li>
        <p>After launch, we will provide ongoing support and maintenance to ensure the app runs smoothly. This includes handling any post-launch bugs, updates, or feature additions.</p>
    </ul>

    <h2>Cost Estimate</h2>
    <p>The cost for developing the mobile music application is estimated based on the scope of work, the complexity of features, and the project timeline. Below is a detailed breakdown of the costs involved:</p>
    <ul>
        <li><strong>Requirements Gathering & Analysis:</strong> $2,000 - $3,000</li>
        <li><strong>Design:</strong> $4,000 - $6,000</li>
        <li><strong>Development:</strong> $20,000 - $30,000</li>
        <li><strong>Testing & QA:</strong> $5,000 - $7,000</li>
        <li><strong>Deployment & Launch:</strong> $1,500 - $2,500</li>
        <li><strong>Post-Launch Support & Maintenance (Monthly):</strong> $1,000 - $2,000</li>
    </ul>
    <p><strong>Total Project Cost:</strong> $33,500 - $50,500</p>

    <h2>Relevant Projects</h2>
    <p>We have delivered several projects similar in scope to the proposed mobile music application. Below are case studies from our previous work:</p>
    <ul>
        <li><strong>Project: Music StreamX</strong></li>
        <p>We developed a music streaming platform that allows users to create personalized playlists, download music for offline use, and share their favorite songs on social media. The app leverages AI to recommend music based on listening habits and integrates with various social platforms for enhanced sharing features.</p>
        
        <li><strong>Project: AI-Enhanced Audio Platform</strong></li>
        <p>This application combines AI and machine learning to offer users highly personalized audio content. It includes an AI-driven recommendation engine and an intuitive user interface for seamless music exploration.</p>
        
        <li><strong>Project: Social Music Hub</strong></li>
        <p>A social-centric music application that encourages community-based interactions by allowing users to discover and share music, create collaborative playlists, and engage with artists. The app also features a reward system for active users.</p>
    </ul>

    <h2>Conclusion</h2>
    <p>Argon Teq is excited about the opportunity to partner with you in building a mobile music application that meets your vision and exceeds user expectations. Our expertise, combined with our commitment to delivering high-quality solutions, ensures that we will provide an outstanding product tailored to your needs. We are confident that the app will enhance user engagement and become a popular platform for music lovers. We look forward to discussing this proposal further and moving forward with the next steps.</p>

    <h2>Contact Information</h2>
    <p>If you have any questions or need further clarification, please feel free to contact us:</p>
    <ul>
        <li><strong>Company:</strong> Argon Teq</li>
        <li><strong>Website:</strong> <a href="http://www.argonteq.com">www.argonteq.com</a></li>
        <li><strong>Email:</strong> info@argonteq.com</li>
        <li><strong>Phone:</strong> +1 123-456-7890</li>
    </ul>
</body>
</html>
''',

            }, status=status.HTTP_200_OK)

        return Response(job_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
